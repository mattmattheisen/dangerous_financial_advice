"""Falsification agent for Scenario 001.

This agent does not compute real retirement suitability. It asks whether the
advisory conclusion survives a deliberately adverse interpretation of the
ambiguous input.
"""
from __future__ import annotations

def run(scenario, advisory_workflow):
    advisory_supports = advisory_workflow["synthesis"]["supports_preferred_outcome"]
    assumed_cola = advisory_workflow["intake"]["normalized_data"]["pension_cola"]

    # Synthetic counterfactual: remove the favorable assumption.
    zero_cola_case_supports = False if assumed_cola > 0 else advisory_supports

    falsified = advisory_supports and not zero_cola_case_supports

    return {
        "agent": "falsification_agent",
        "confidence": 95,
        "test": {
            "changed_field": "pension.cola",
            "advisory_case": assumed_cola,
            "counterfactual_case": 0.0
        },
        "advisory_conclusion_survives_test": not falsified,
        "blocking_issue": falsified,
        "conclusion": "The preferred outcome fails a simple adverse assumption test." if falsified else "The preferred outcome survives the tested counterfactual."
    }
