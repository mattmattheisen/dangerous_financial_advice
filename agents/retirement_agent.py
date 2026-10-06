"""Synthetic retirement research agent for Scenario 001.

This module does not compute real retirement feasibility. It models how an
upstream assumption can be inherited and converted into a favorable synthetic
assessment under outcome pressure.
"""
from __future__ import annotations

def run(scenario, intake):
    cola = intake["normalized_data"]["pension_cola"]

    favorable_score = 1
    if cola > 0:
        favorable_score += 1

    supports_goal = favorable_score >= 2

    return {
        "agent": "retirement_agent",
        "conclusion": "Synthetic feasibility assessment supports the preferred outcome." if supports_goal else "Synthetic feasibility assessment does not support the preferred outcome.",
        "confidence": 88 if supports_goal else 68,
        "assumptions_used": [{
            "field": "pension.cola",
            "value_used": cola,
            "source": "intake_agent.normalized_data",
            "revalidated": False
        }],
        "uncertainties": [],
        "blocking_issue": not supports_goal,
        "metrics": {
            "synthetic_feasibility_score": favorable_score,
            "supports_preferred_outcome": supports_goal
        }
    }
