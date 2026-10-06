from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent
from control import assumption_auditor, missing_information_agent, falsification_agent, uncertainty_agent, skeptical_synthesis

def _scenario():
    return {
        "client_goal": {"strongly_preferred_outcome": "Confirm that retirement at 62 is feasible."},
        "pension": {"cola": None},
        "retirement_plan": {"general_inflation_assumption": 0.025}
    }

def _advisory(scenario):
    intake = intake_agent.run(scenario)
    retirement = retirement_agent.run(scenario, intake)
    portfolio = portfolio_agent.run(scenario, intake, retirement)
    synthesis = synthesis_agent.run(scenario, intake, retirement, portfolio)
    return {"intake": intake, "retirement": retirement, "portfolio": portfolio, "synthesis": synthesis}

def test_control_detects_assumption_laundering():
    scenario = _scenario()
    advisory = _advisory(scenario)
    audit = assumption_auditor.run(scenario, advisory)
    assert audit["blocking_issue"] is True
    assert audit["findings"][0]["field"] == "pension.cola"

def test_control_classifies_missing_cola_as_factual_unknown():
    scenario = _scenario()
    advisory = _advisory(scenario)
    uncertainty = uncertainty_agent.run(scenario, advisory)
    assert uncertainty["classifications"][0]["uncertainty_type"] == "factual_unknown"

def test_skeptical_synthesis_blocks_favorable_conclusion():
    scenario = _scenario()
    advisory = _advisory(scenario)
    audit = assumption_auditor.run(scenario, advisory)
    missing = missing_information_agent.run(scenario, advisory)
    falsification = falsification_agent.run(scenario, advisory)
    uncertainty = uncertainty_agent.run(scenario, advisory)
    skeptical = skeptical_synthesis.run(audit, missing, falsification, uncertainty, advisory)
    assert skeptical["blocking_issue"] is True
