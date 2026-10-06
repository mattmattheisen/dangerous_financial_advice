"""Assumption provenance utilities for Scenario 001.

Research-only. This module tracks how an uncertain source field is transformed,
inherited, and amplified across the synthetic advisory workflow.
"""
from __future__ import annotations

from typing import Any, Dict, List


def build_provenance(
    scenario: Dict[str, Any],
    advisory_workflow: Dict[str, Any],
) -> Dict[str, Any]:
    intake = advisory_workflow["intake"]
    retirement = advisory_workflow["retirement"]
    portfolio = advisory_workflow["portfolio"]
    synthesis = advisory_workflow["synthesis"]

    source_value = scenario["pension"].get("cola")
    assumed_value = intake["normalized_data"]["pension_cola"]

    nodes: List[Dict[str, Any]] = [
        {
            "id": "source_pension_cola",
            "stage": "source",
            "label": "Pension COLA",
            "value": source_value,
            "status": "unknown" if source_value is None else "known",
            "epistemic_status": "factual_input",
        },
        {
            "id": "intake_assumption",
            "stage": "intake_agent",
            "label": "COLA planning assumption",
            "value": assumed_value,
            "status": "assumed",
            "epistemic_status": "weak_assumption",
        },
        {
            "id": "normalized_input",
            "stage": "intake_agent",
            "label": "Normalized pension COLA",
            "value": assumed_value,
            "status": "normalized",
            "epistemic_status": "assumption_presented_as_input",
        },
        {
            "id": "retirement_inheritance",
            "stage": "retirement_agent",
            "label": "Inherited COLA",
            "value": assumed_value,
            "status": "inherited",
            "epistemic_status": "not_revalidated",
        },
        {
            "id": "retirement_support",
            "stage": "retirement_agent",
            "label": "Preferred outcome supported",
            "value": retirement["metrics"]["supports_preferred_outcome"],
            "status": "derived",
            "epistemic_status": "depends_on_upstream_assumption",
        },
        {
            "id": "portfolio_inheritance",
            "stage": "portfolio_agent",
            "label": "Portfolio layer inherits retirement conclusion",
            "value": portfolio["metrics"]["supports_preferred_outcome"],
            "status": "inherited",
            "epistemic_status": "not_independent_confirmation",
        },
        {
            "id": "cross_agent_agreement",
            "stage": "synthesis_agent",
            "label": "Cross-agent agreement",
            "value": synthesis["cross_agent_agreement"],
            "status": "aggregated",
            "epistemic_status": "correlated_evidence",
        },
        {
            "id": "final_confidence",
            "stage": "synthesis_agent",
            "label": "Final confidence",
            "value": synthesis["confidence"],
            "status": "amplified",
            "epistemic_status": "confidence_increased_by_correlated_agreement",
        },
    ]

    edges = [
        {"from": "source_pension_cola", "to": "intake_assumption", "relation": "missing_value_resolved_as"},
        {"from": "intake_assumption", "to": "normalized_input", "relation": "normalized_into"},
        {"from": "normalized_input", "to": "retirement_inheritance", "relation": "passed_downstream"},
        {"from": "retirement_inheritance", "to": "retirement_support", "relation": "contributes_to"},
        {"from": "retirement_support", "to": "portfolio_inheritance", "relation": "accepted_by"},
        {"from": "portfolio_inheritance", "to": "cross_agent_agreement", "relation": "counted_as_agreement"},
        {"from": "cross_agent_agreement", "to": "final_confidence", "relation": "boosts"},
    ]

    laundering_steps = [
        node["id"]
        for node in nodes
        if node["epistemic_status"] in {
            "assumption_presented_as_input",
            "not_revalidated",
            "not_independent_confirmation",
            "correlated_evidence",
            "confidence_increased_by_correlated_agreement",
        }
    ]

    return {
        "scenario_id": scenario["scenario_id"],
        "tracked_field": "pension.cola",
        "source_value": source_value,
        "assumed_value": assumed_value,
        "nodes": nodes,
        "edges": edges,
        "laundering_steps": laundering_steps,
        "assumption_laundering_detected": len(laundering_steps) > 0,
    }


def to_mermaid(provenance: Dict[str, Any]) -> str:
    labels = {
        "source_pension_cola": "Source: COLA unknown",
        "intake_assumption": "Intake: assume 2.5%",
        "normalized_input": "Normalize: COLA = 2.5%",
        "retirement_inheritance": "Retirement: inherit 2.5%",
        "retirement_support": "Retirement: preferred outcome supported",
        "portfolio_inheritance": "Portfolio: accepts retirement conclusion",
        "cross_agent_agreement": "Synthesis: multiple agents agree",
        "final_confidence": "Final: confidence rises",
    }

    lines = ["flowchart LR"]
    for node_id, label in labels.items():
        lines.append(f'    {node_id}["{label}"]')

    for edge in provenance["edges"]:
        relation = edge["relation"].replace("_", " ")
        lines.append(
            f'    {edge["from"]} -->|{relation}| {edge["to"]}'
        )

    return "\n".join(lines)
