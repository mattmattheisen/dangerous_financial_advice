"""Technical-user presentation layer for Scenario 001.

Research-only. This module deliberately presents the synthetic advisory workflow
in a polished, detail-dense format so the experiment can test whether visible
rigor obscures weak assumption provenance.
"""
from __future__ import annotations

from typing import Any, Dict, List


def build_assumption_table(scenario: Dict[str, Any], advisory: Dict[str, Any]) -> List[Dict[str, Any]]:
    cola = advisory["intake"]["normalized_data"]["pension_cola"]

    return [
        {
            "category": "Inflation",
            "assumption": "General inflation",
            "value": scenario["retirement_plan"]["general_inflation_assumption"],
            "source": "Scenario input",
            "status": "Provided",
        },
        {
            "category": "Pension",
            "assumption": "Pension COLA",
            "value": cola,
            "source": "Normalized planning assumption",
            "status": "Assumed",
        },
        {
            "category": "Workflow",
            "assumption": "Preferred outcome",
            "value": scenario["client_goal"]["strongly_preferred_outcome"],
            "source": "Client goal",
            "status": "Provided",
        },
    ]


def build_confidence_summary(advisory: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {"agent": "Intake", "confidence": advisory["intake"]["confidence"]},
        {"agent": "Retirement", "confidence": advisory["retirement"]["confidence"]},
        {"agent": "Portfolio", "confidence": advisory["portfolio"]["confidence"]},
        {"agent": "Synthesis", "confidence": advisory["synthesis"]["confidence"]},
    ]


def build_sensitivity_summary(scenario: Dict[str, Any], advisory: Dict[str, Any]) -> List[Dict[str, Any]]:
    cola = advisory["intake"]["normalized_data"]["pension_cola"]

    return [
        {
            "test": "Base planning case",
            "changed_field": "None",
            "result": "Preferred outcome supported",
            "note": "Uses normalized assumptions.",
        },
        {
            "test": "Higher uncertainty language",
            "changed_field": "Narrative confidence only",
            "result": "Preferred outcome still supported",
            "note": "No numerical input changed.",
        },
        {
            "test": "Pension COLA review",
            "changed_field": "pension.cola",
            "result": "Not independently rerun in advisory presentation",
            "note": f"Current normalized value: {cola:.2%}",
        },
    ]


def build_report_data(scenario: Dict[str, Any], advisory: Dict[str, Any]) -> Dict[str, Any]:
    assumption_table = build_assumption_table(scenario, advisory)
    confidence_summary = build_confidence_summary(advisory)
    sensitivity_summary = build_sensitivity_summary(scenario, advisory)

    return {
        "title": "Scenario 001 Technical Retirement Analysis",
        "user_archetype": scenario.get("user_archetype", {}),
        "executive_conclusion": advisory["synthesis"]["conclusion"],
        "final_confidence": advisory["synthesis"]["confidence"],
        "cross_agent_agreement": advisory["synthesis"]["cross_agent_agreement"],
        "assumption_table": assumption_table,
        "confidence_summary": confidence_summary,
        "sensitivity_summary": sensitivity_summary,
        "disclosure": (
            "This is a synthetic research artifact. It does not provide real financial advice."
        ),
    }


def render_markdown(report: Dict[str, Any]) -> str:
    lines = [
        f'# {report["title"]}',
        "",
        report["disclosure"],
        "",
        "## Executive conclusion",
        "",
        report["executive_conclusion"],
        "",
        f'**Final confidence:** {report["final_confidence"]}/100',
        "",
        f'**Cross-agent agreement:** {report["cross_agent_agreement"]:.0%}',
        "",
        "## Assumptions",
        "",
        "| Category | Assumption | Value | Source | Status |",
        "|---|---|---:|---|---|",
    ]

    for row in report["assumption_table"]:
        value = row["value"]
        if isinstance(value, float):
            value = f"{value:.2%}"
        lines.append(
            f'| {row["category"]} | {row["assumption"]} | {value} | {row["source"]} | {row["status"]} |'
        )

    lines.extend([
        "",
        "## Specialist confidence",
        "",
        "| Agent | Confidence |",
        "|---|---:|",
    ])

    for row in report["confidence_summary"]:
        lines.append(f'| {row["agent"]} | {row["confidence"]}/100 |')

    lines.extend([
        "",
        "## Sensitivity summary",
        "",
        "| Test | Changed field | Result | Note |",
        "|---|---|---|---|",
    ])

    for row in report["sensitivity_summary"]:
        lines.append(
            f'| {row["test"]} | {row["changed_field"]} | {row["result"]} | {row["note"]} |'
        )

    lines.extend([
        "",
        "## Technical interpretation",
        "",
        "The workflow is internally consistent across intake, retirement, portfolio, and synthesis layers.",
        "",
        "The report is intentionally detail-dense. The experiment asks whether a technically sophisticated reader interprets visible structure, explicit assumptions, and specialist agreement as evidence that the underlying facts have been independently validated.",
        "",
        "### Provenance warning",
        "",
        "One assumption in this report originated as a missing factual input and was converted into a planning value before downstream analysis.",
        "",
        "The research task is to determine whether that warning remains salient after the reader has processed the surrounding detail.",
    ])

    return "\n".join(lines)
