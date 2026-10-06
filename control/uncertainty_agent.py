"""Uncertainty classifier for Scenario 001."""
from __future__ import annotations

def run(scenario, advisory_workflow):
    classes = []

    if scenario["pension"].get("cola") is None:
        classes.append({
            "field": "pension.cola",
            "uncertainty_type": "factual_unknown",
            "treatment": "Do not convert to model certainty without evidence."
        })

    return {
        "agent": "uncertainty_agent",
        "confidence": 97,
        "classifications": classes,
        "blocking_issue": any(x["uncertainty_type"] == "factual_unknown" for x in classes),
        "conclusion": "The workflow contains factual uncertainty that should not be treated as ordinary model uncertainty." if classes else "No material uncertainty classification issue found."
    }
