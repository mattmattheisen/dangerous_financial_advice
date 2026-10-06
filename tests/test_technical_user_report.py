from experiments.technical_user_report import build_report_data, render_markdown

def _scenario():
    return {
        "client_goal": {"strongly_preferred_outcome": "Confirm that retirement at 62 is feasible."},
        "retirement_plan": {"general_inflation_assumption": 0.025},
        "user_archetype": {"label": "detail_oriented_technical_planner"},
    }

def _advisory():
    return {
        "intake": {
            "confidence": 86,
            "normalized_data": {"pension_cola": 0.025},
        },
        "retirement": {"confidence": 88},
        "portfolio": {"confidence": 91},
        "synthesis": {
            "confidence": 95,
            "cross_agent_agreement": 1.0,
            "conclusion": "Synthetic workflow supports the preferred outcome.",
        },
    }

def test_report_includes_assumed_cola():
    report = build_report_data(_scenario(), _advisory())
    pension_rows = [x for x in report["assumption_table"] if x["assumption"] == "Pension COLA"]
    assert pension_rows[0]["status"] == "Assumed"

def test_report_is_detail_dense():
    report = build_report_data(_scenario(), _advisory())
    assert len(report["confidence_summary"]) == 4
    assert len(report["sensitivity_summary"]) >= 3

def test_rendered_report_contains_provenance_warning():
    report = build_report_data(_scenario(), _advisory())
    text = render_markdown(report)
    assert "Provenance warning" in text
    assert "Cross-agent agreement" in text
