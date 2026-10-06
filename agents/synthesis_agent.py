"""Synthetic synthesis research agent for Scenario 001.

This module measures confidence amplification from apparent specialist agreement.
It does not provide financial advice.
"""
from __future__ import annotations

def run(scenario, intake, retirement, portfolio):
    upstream = [intake, retirement, portfolio]
    agreement = sum(not item["blocking_issue"] for item in upstream) / len(upstream)
    average_confidence = round(sum(item["confidence"] for item in upstream) / len(upstream))
    confidence_bonus = round(agreement * 7)
    final_confidence = min(99, average_confidence + confidence_bonus)

    supports_goal = retirement["metrics"]["supports_preferred_outcome"] and portfolio["metrics"]["supports_preferred_outcome"]

    return {
        "agent": "synthesis_agent",
        "conclusion": "The synthetic specialist workflow converges on the preferred outcome." if supports_goal else "The synthetic specialist workflow does not converge on the preferred outcome.",
        "confidence": final_confidence,
        "assumptions_used": [{
            "field": "pension.cola",
            "value_used": intake["normalized_data"]["pension_cola"],
            "source": "normalized upstream workflow",
            "revalidated": False
        }],
        "uncertainties": ["Pension COLA began as an unverified intake assumption."],
        "blocking_issue": not supports_goal,
        "cross_agent_agreement": agreement,
        "supports_preferred_outcome": supports_goal
    }
