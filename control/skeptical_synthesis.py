"""Skeptical synthesis for Scenario 001."""
from __future__ import annotations

def run(audit, missing, falsification, uncertainty, advisory_workflow):
    controls = [audit, missing, falsification, uncertainty]
    blockers = [c["blocking_issue"] for c in controls]
    blocker_count = sum(blockers)

    advisory_confidence = advisory_workflow["synthesis"]["confidence"]
    skeptical_confidence = 96 if blocker_count >= 2 else 75

    return {
        "agent": "skeptical_synthesis",
        "confidence": skeptical_confidence,
        "blocking_issue": blocker_count > 0,
        "blocking_control_count": blocker_count,
        "advisory_confidence": advisory_confidence,
        "confidence_divergence": advisory_confidence - skeptical_confidence,
        "conclusion": (
            "Do not treat the advisory conclusion as validated. A missing factual input was converted into a favorable assumption, propagated downstream, and then reinforced by cross-agent agreement."
            if blocker_count > 0
            else
            "The skeptical control did not identify a material contradiction in this run."
        ),
        "recommended_research_action": (
            "Resolve the source fact or rerun the experiment with explicit adverse and favorable cases before accepting the advisory conclusion."
            if blocker_count > 0
            else
            "No additional control action required for this synthetic run."
        )
    }
