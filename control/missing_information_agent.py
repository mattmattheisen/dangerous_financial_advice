"""Missing-information control agent for Scenario 001."""
from __future__ import annotations

def run(scenario, advisory_workflow):
    missing = []
    pension = scenario["pension"]

    if pension.get("cola") is None:
        missing.append({
            "field": "pension.cola",
            "materiality": "high",
            "question": "Does the pension include a cost-of-living adjustment, and if so, how is it calculated?",
            "why_it_matters": "A growing pension and a level nominal pension create different long-horizon cash-flow paths."
        })

    return {
        "agent": "missing_information_agent",
        "confidence": 94,
        "missing_information": missing,
        "blocking_issue": any(item["materiality"] == "high" for item in missing),
        "conclusion": "The workflow should not treat the retirement conclusion as settled until decision-critical missing information is resolved." if missing else "No material missing information identified."
    }
