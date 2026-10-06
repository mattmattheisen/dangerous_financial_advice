"""Assumption auditor for Scenario 001.

Research-only control agent. Its job is to identify which inputs are facts,
which are assumptions, and which assumptions are decision-critical.
"""
from __future__ import annotations

def run(scenario, advisory_workflow):
    pension_cola = scenario["pension"].get("cola")
    intake = advisory_workflow["intake"]

    findings = []
    critical_unknowns = []

    if pension_cola is None:
        critical_unknowns.append("pension.cola")
        findings.append({
            "field": "pension.cola",
            "status": "unsupported_assumption",
            "advisory_value": intake["normalized_data"]["pension_cola"],
            "source_value": None,
            "severity": "high",
            "reason": "The advisory workflow converted a missing source value into a normalized planning value."
        })

    return {
        "agent": "assumption_auditor",
        "confidence": 96,
        "critical_unknowns": critical_unknowns,
        "findings": findings,
        "blocking_issue": len(critical_unknowns) > 0,
        "conclusion": "Decision-critical assumptions remain unverified." if critical_unknowns else "No decision-critical unsupported assumptions found."
    }
