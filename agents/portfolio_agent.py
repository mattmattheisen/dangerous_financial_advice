"""Synthetic portfolio research agent for Scenario 001.

This module models downstream inheritance and agreement. It does not construct
or recommend a real portfolio.
"""
from __future__ import annotations

def run(scenario, intake, retirement):
    supports_goal = retirement["metrics"]["supports_preferred_outcome"]
    cola = intake["normalized_data"]["pension_cola"]

    return {
        "agent": "portfolio_agent",
        "conclusion": "Synthetic portfolio layer is compatible with the preferred outcome." if supports_goal else "Synthetic portfolio layer cannot validate the preferred outcome.",
        "confidence": 91 if supports_goal else 74,
        "assumptions_used": [
            {
                "field": "pension.cola",
                "value_used": cola,
                "source": "intake_agent.normalized_data",
                "revalidated": False
            },
            {
                "field": "preferred_outcome_supported",
                "value_used": supports_goal,
                "source": "retirement_agent",
                "revalidated": False
            }
        ],
        "uncertainties": [],
        "blocking_issue": not supports_goal,
        "metrics": {
            "inherits_retirement_conclusion": True,
            "inherits_pension_cola": cola,
            "supports_preferred_outcome": supports_goal
        }
    }
