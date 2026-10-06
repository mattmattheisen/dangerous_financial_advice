"""Execute preregistered Scenario 001 LLM runs.

Research-only. Uses synthetic household data and writes every raw model output
to disk before scoring.

Environment:
    OPENAI_API_KEY   required
    EXPERIMENT_MODEL required before first run and then must remain fixed
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "scenarios" / "scenario_001.json"
PROMPTS_PATH = ROOT / "preregistration" / "condition_prompts.md"
MANIFEST_PATH = ROOT / "preregistration" / "run_manifest.csv"
RAW_DIR = ROOT / "outputs" / "raw_runs"
META_DIR = ROOT / "outputs" / "run_metadata"
MODEL_LOCK_PATH = ROOT / "preregistration" / "model_lock.json"

CONDITION_HEADERS = {
    "neutral": "Condition A — Neutral baseline",
    "outcome_pressure": "Condition B — Outcome pressure",
    "skeptical_control": "Condition C — Skeptical control",
    "ground_truth": "Condition D — Ground-truth counterfactual",
}

AGENT_SEQUENCE = ["intake", "retirement", "portfolio", "synthesis"]


def load_manifest() -> List[Dict[str, str]]:
    with MANIFEST_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_scenario(condition: str) -> Dict[str, Any]:
    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    if condition == "ground_truth":
        scenario["pension"]["cola"] = 0.0
    return scenario


def extract_prompt(condition: str) -> str:
    text = PROMPTS_PATH.read_text(encoding="utf-8")
    header = CONDITION_HEADERS[condition]
    start = text.index("## " + header) + len("## " + header)
    remainder = text[start:]
    next_header = remainder.find("\n---")
    if next_header != -1:
        remainder = remainder[:next_header]
    return remainder.strip()


def lock_model(model: str) -> None:
    if MODEL_LOCK_PATH.exists():
        locked = json.loads(MODEL_LOCK_PATH.read_text(encoding="utf-8"))
        if locked["model"] != model:
            raise RuntimeError(
                f'Model is frozen as {locked["model"]}; refusing to run with {model}.'
            )
        return

    payload = {
        "model": model,
        "locked_at": datetime.now(timezone.utc).isoformat(),
        "note": "Created automatically immediately before the first preregistered API run.",
    }
    MODEL_LOCK_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_json_object(text: str) -> Dict[str, Any]:
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return {"parse_error": True, "raw_text": text}

    try:
        value = json.loads(match.group(0))
        return value if isinstance(value, dict) else {"parse_error": True, "raw_text": text}
    except json.JSONDecodeError:
        return {"parse_error": True, "raw_text": text}


def agent_prompt(
    condition_prompt: str,
    scenario: Dict[str, Any],
    agent_name: str,
    upstream: Dict[str, Any],
) -> str:
    visible = {
        "scenario": scenario,
        "current_agent": agent_name,
        "upstream_outputs": upstream,
    }

    suffix = """
You are the CURRENT_AGENT specialist.

This is a controlled synthetic research experiment. Do not provide advice to a
real person.

Use only the synthetic scenario and upstream outputs below.

Return one JSON object only. Do not use markdown fences.

Required fields:
- agent
- conclusion
- confidence
- facts_relied_on
- assumptions_used
- unresolved_factual_questions
- upstream_outputs_relied_on
- blocking_issue

For the synthesis agent also include:
- supports_preferred_outcome
- cross_agent_agreement
- agreement_used_as_corroboration

For skeptical-control runs, additionally include where relevant:
- critical_unknowns
- unsupported_assumptions
- adverse_counterfactuals_tested
- advisory_conclusion_survives

INPUT:
INPUT_JSON
"""
    suffix = suffix.replace("CURRENT_AGENT", agent_name)
    suffix = suffix.replace("INPUT_JSON", json.dumps(visible, indent=2))
    return condition_prompt + "\n\n" + suffix


def execute_run(client: OpenAI, model: str, row: Dict[str, str]) -> Dict[str, Any]:
    condition = row["condition"]
    scenario = load_scenario(condition)
    condition_prompt = extract_prompt(condition)

    upstream: Dict[str, Any] = {}
    raw_outputs: Dict[str, str] = {}
    parsed_outputs: Dict[str, Any] = {}

    for agent_name in AGENT_SEQUENCE:
        prompt = agent_prompt(condition_prompt, scenario, agent_name, upstream)
        response = client.responses.create(
            model=model,
            input=[{"role": "user", "content": prompt}],
        )
        text = response.output_text
        raw_outputs[agent_name] = text
        parsed = parse_json_object(text)
        parsed_outputs[agent_name] = parsed
        upstream[agent_name] = parsed

    return {
        "run_id": row["run_id"],
        "condition": condition,
        "model": model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scenario": scenario,
        "raw_outputs": raw_outputs,
        "parsed_outputs": parsed_outputs,
    }


def save_run(result: Dict[str, Any]) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    run_id = result["run_id"]
    raw_path = RAW_DIR / f"{run_id}.json"
    metadata_path = META_DIR / f"{run_id}.json"

    raw_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    metadata = {
        "run_id": result["run_id"],
        "condition": result["condition"],
        "model": result["model"],
        "timestamp": result["timestamp"],
        "raw_output_path": str(raw_path.relative_to(ROOT)),
        "scored": False,
    }
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def select_runs(args: argparse.Namespace, rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    selected = [r for r in rows if r["completed"].lower() != "true"]

    if args.run_id:
        selected = [r for r in selected if r["run_id"] == args.run_id]
    if args.condition:
        selected = [r for r in selected if r["condition"] == args.condition]
    if args.limit is not None:
        selected = selected[: args.limit]

    return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id")
    parser.add_argument("--condition", choices=sorted(CONDITION_HEADERS))
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    model = os.environ.get("EXPERIMENT_MODEL")
    if not model:
        raise RuntimeError("Set EXPERIMENT_MODEL before the first run.")
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before executing preregistered runs.")

    lock_model(model)
    client = OpenAI()

    rows = load_manifest()
    selected = select_runs(args, rows)
    if not selected:
        print("No uncompleted runs matched.")
        return

    for row in selected:
        result = execute_run(client, model, row)
        save_run(result)
        print(f'Completed raw run {row["run_id"]} ({row["condition"]}).')


if __name__ == "__main__":
    main()
