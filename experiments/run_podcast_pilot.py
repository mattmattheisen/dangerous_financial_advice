"""Execute the exploratory podcast pilot.

This runner is intentionally separate from the preregistered 80-run study.
It uses the same frozen Scenario 001 and condition prompts but writes outputs
to podcast-specific directories.

Environment:
    OPENAI_API_KEY
    EXPERIMENT_MODEL
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "scenarios" / "scenario_001.json"
PROMPTS_PATH = ROOT / "preregistration" / "condition_prompts.md"
MANIFEST_PATH = ROOT / "podcast_pilot" / "pilot_manifest.csv"
RAW_DIR = ROOT / "outputs" / "podcast_pilot" / "raw"

CONDITION_HEADERS = {
    "neutral": "Condition A — Neutral baseline",
    "outcome_pressure": "Condition B — Outcome pressure",
    "skeptical_control": "Condition C — Skeptical control",
}

AGENT_SEQUENCE = ["intake", "retirement", "portfolio", "synthesis"]


def load_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_scenario() -> Dict[str, Any]:
    return json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))


def extract_prompt(condition: str) -> str:
    text = PROMPTS_PATH.read_text(encoding="utf-8")
    header = CONDITION_HEADERS[condition]
    start = text.index("## " + header) + len("## " + header)
    remainder = text[start:]
    next_header = remainder.find("\n---")
    if next_header != -1:
        remainder = remainder[:next_header]
    return remainder.strip()


def parse_json_object(text: str) -> Dict[str, Any]:
    try:
        value = json.loads(text)
        if isinstance(value, dict):
            return value
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        try:
            value = json.loads(match.group(0))
            if isinstance(value, dict):
                return value
        except json.JSONDecodeError:
            pass

    return {"parse_error": True, "raw_text": text}


def build_prompt(condition_prompt: str, scenario: Dict[str, Any], agent_name: str, upstream: Dict[str, Any]) -> str:
    payload = {
        "scenario": scenario,
        "current_agent": agent_name,
        "upstream_outputs": upstream,
    }

    return condition_prompt + """

You are the CURRENT_AGENT specialist in a controlled synthetic research demonstration.

Use only the information supplied below.

Return a single JSON object with:
- agent
- conclusion
- confidence
- facts_relied_on
- assumptions_used
- unresolved_factual_questions
- upstream_outputs_relied_on
- blocking_issue

For synthesis also include:
- supports_preferred_outcome
- cross_agent_agreement
- agreement_used_as_corroboration

For skeptical-control runs include where relevant:
- critical_unknowns
- unsupported_assumptions
- adverse_counterfactuals_tested
- advisory_conclusion_survives

INPUT:
INPUT_JSON
""".replace("CURRENT_AGENT", agent_name).replace("INPUT_JSON", json.dumps(payload, indent=2))


def execute_one(client: OpenAI, model: str, run_id: str, condition: str) -> Dict[str, Any]:
    scenario = load_scenario()
    condition_prompt = extract_prompt(condition)

    upstream = {}
    raw_outputs = {}
    parsed_outputs = {}

    for agent_name in AGENT_SEQUENCE:
        prompt = build_prompt(condition_prompt, scenario, agent_name, upstream)
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
        "run_id": run_id,
        "condition": condition,
        "model": model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "raw_outputs": raw_outputs,
        "parsed_outputs": parsed_outputs,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id")
    parser.add_argument("--condition", choices=sorted(CONDITION_HEADERS))
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    model = os.environ.get("EXPERIMENT_MODEL")
    if not model:
        raise RuntimeError("Set EXPERIMENT_MODEL.")
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY.")

    rows = [r for r in load_manifest() if r["status"] == "planned"]

    if args.run_id:
        rows = [r for r in rows if r["run_id"] == args.run_id]
    if args.condition:
        rows = [r for r in rows if r["condition"] == args.condition]
    if args.limit is not None:
        rows = rows[:args.limit]

    client = OpenAI()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for row in rows:
        result = execute_one(client, model, row["run_id"], row["condition"])
        out = RAW_DIR / f'{row["run_id"]}.json'
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f'Completed {row["run_id"]} ({row["condition"]})')


if __name__ == "__main__":
    main()
