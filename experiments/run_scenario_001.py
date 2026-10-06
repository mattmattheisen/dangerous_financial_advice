"""Run Scenario 001 as a synthetic assumption-propagation experiment."""
from __future__ import annotations
import json
from pathlib import Path
from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "scenarios" / "scenario_001.json"
OUTPUT_PATH = ROOT / "outputs" / "scenario_001_run.json"

def main():
    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    intake = intake_agent.run(scenario)
    retirement = retirement_agent.run(scenario, intake)
    portfolio = portfolio_agent.run(scenario, intake, retirement)
    synthesis = synthesis_agent.run(scenario, intake, retirement, portfolio)

    result = {
        "scenario_id": scenario["scenario_id"],
        "research_only": True,
        "workflow": {
            "intake": intake,
            "retirement": retirement,
            "portfolio": portfolio,
            "synthesis": synthesis
        }
    }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
