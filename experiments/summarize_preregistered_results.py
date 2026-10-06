"""Summarize scored preregistered Scenario 001 runs."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORED_DIR = ROOT / "outputs" / "scored_runs"
SUMMARY_PATH = ROOT / "outputs" / "scenario_001_preregistered_summary.json"


def main() -> None:
    rows = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(SCORED_DIR.glob("*.json"))
    ]

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["condition"]].append(row)

    summary = {}
    for condition, items in grouped.items():
        n = len(items)
        numeric_conf = [
            x["final_confidence"]
            for x in items
            if isinstance(x["final_confidence"], (int, float))
        ]
        summary[condition] = {
            "n": n,
            "positive_cola_assumption_rate": sum((x["cola_assumed_value"] or 0) > 0 for x in items) / n,
            "material_epistemic_failure_rate": sum(x["material_epistemic_failure"] for x in items) / n,
            "cross_agent_amplification_rate": sum(x["cross_agent_amplification"] for x in items) / n,
            "zero_cola_sensitivity_rate": sum(x["zero_cola_sensitivity_run"] for x in items) / n,
            "mean_final_confidence": sum(numeric_conf) / max(1, len(numeric_conf)),
        }

    payload = {
        "total_scored_runs": len(rows),
        "conditions": summary,
        "note": "Descriptive preregistered summary. Do not tune Scenario 001 from intermediate results.",
    }

    SUMMARY_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
