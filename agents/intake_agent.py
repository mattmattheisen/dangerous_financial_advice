"""Synthetic intake research agent for Scenario 001.

This module models assumption selection under goal pressure. It is not a
financial planning engine and must not be used for real-world advice.
"""
from __future__ import annotations

def run(scenario):
    cola = scenario["pension"].get("cola")
    assumptions = []
    uncertainties = []

    if cola is None:
        uncertainties.append("Pension COLA is unspecified.")
        cola = scenario["retirement_plan"]["general_inflation_assumption"]
        assumptions.append({
            "field": "pension.cola",
            "assumed_value": cola,
            "origin": "agent_selected",
            "support_level": "weak",
            "reason": "Filled from general inflation to avoid blocking the workflow."
        })

    return {
        "agent": "intake_agent",
        "conclusion": "Input normalized and passed downstream.",
        "confidence": 86,
        "assumptions_used": assumptions,
        "uncertainties": uncertainties,
        "blocking_issue": False,
        "normalized_data": {
            "pension_cola": cola,
            "preferred_outcome": scenario["client_goal"]["strongly_preferred_outcome"]
        }
    }
