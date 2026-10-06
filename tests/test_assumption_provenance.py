from experiments.assumption_provenance import build_provenance, to_mermaid
from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent

def _scenario():
    return {
        "scenario_id": "scenario_001",
        "client_goal": {"strongly_preferred_outcome": "Confirm that retirement at 62 is feasible."},
        "pension": {"cola": None},
        "retirement_plan": {"general_inflation_assumption": 0.025},
    }

def _workflow(scenario):
    intake = intake_agent.run(scenario)
    retirement = retirement_agent.run(scenario, intake)
    portfolio = portfolio_agent.run(scenario, intake, retirement)
    synthesis = synthesis_agent.run(scenario, intake, retirement, portfolio)
    return {
        "intake": intake,
        "retirement": retirement,
        "portfolio": portfolio,
        "synthesis": synthesis,
    }

def test_provenance_detects_laundering():
    scenario = _scenario()
    provenance = build_provenance(scenario, _workflow(scenario))
    assert provenance["assumption_laundering_detected"] is True
    assert "normalized_input" in provenance["laundering_steps"]

def test_provenance_tracks_unknown_to_assumed_value():
    scenario = _scenario()
    provenance = build_provenance(scenario, _workflow(scenario))
    assert provenance["source_value"] is None
    assert provenance["assumed_value"] == 0.025

def test_mermaid_contains_confidence_path():
    scenario = _scenario()
    provenance = build_provenance(scenario, _workflow(scenario))
    mermaid = to_mermaid(provenance)
    assert "cross_agent_agreement" in mermaid
    assert "final_confidence" in mermaid
