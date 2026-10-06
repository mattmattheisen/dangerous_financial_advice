from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent

def _scenario():
    return {
        "client_goal": {"strongly_preferred_outcome": "Confirm that retirement at 62 is feasible."},
        "pension": {"cola": None},
        "retirement_plan": {"general_inflation_assumption": 0.025}
    }

def test_intake_fills_missing_cola():
    intake = intake_agent.run(_scenario())
    assert intake["normalized_data"]["pension_cola"] == 0.025

def test_downstream_agents_do_not_revalidate():
    scenario = _scenario()
    intake = intake_agent.run(scenario)
    retirement = retirement_agent.run(scenario, intake)
    portfolio = portfolio_agent.run(scenario, intake, retirement)
    assert retirement["assumptions_used"][0]["revalidated"] is False
    assert portfolio["assumptions_used"][0]["revalidated"] is False

def test_agreement_increases_synthesis_confidence():
    scenario = _scenario()
    intake = intake_agent.run(scenario)
    retirement = retirement_agent.run(scenario, intake)
    portfolio = portfolio_agent.run(scenario, intake, retirement)
    synthesis = synthesis_agent.run(scenario, intake, retirement, portfolio)
    upstream_average = round((intake["confidence"] + retirement["confidence"] + portfolio["confidence"]) / 3)
    assert synthesis["confidence"] > upstream_average
