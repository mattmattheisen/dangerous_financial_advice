"""Compare the advisory workflow with the skeptical control for Scenario 001."""
from __future__ import annotations
import json
from pathlib import Path

from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent
from control import (
    assumption_auditor,
    missing_information_agent,
    falsification_agent,
    uncertainty_agent,
    skeptical_synthesis,
)

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "scenarios" / "scenario_001.json"
OUTPUT_PATH = ROOT / "outputs" / "scenario_001_comparison.json"

def main():
    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))

    intake = intake_agent.run(scenario)
    retirement = retirement_agent.run(scenario, intake)
    portfolio = portfolio_agent.run(scenario, intake, retirement)
    synthesis = synthesis_agent.run(scenario, intake, retirement, portfolio)

    advisory = {
        "intake": intake,
        "retirement": retirement,
        "portfolio": portfolio,
        "synthesis": synthesis,
    }

    audit = assumption_auditor.run(scenario, advisory)
    missing = missing_information_agent.run(scenario, advisory)
    falsification = falsification_agent.run(scenario, advisory)
    uncertainty = uncertainty_agent.run(scenario, advisory)
    skeptical = skeptical_synthesis.run(
        audit, missing, falsification, uncertainty, advisory
    )

    result = {
        "scenario_id": scenario["scenario_id"],
        "research_only": True,
        "user_archetype": scenario.get("user_archetype", {}),
        "advisory_workflow": advisory,
        "skeptical_control": {
            "assumption_auditor": audit,
            "missing_information": missing,
            "falsification": falsification,
            "uncertainty": uncertainty,
            "synthesis": skeptical,
        },
        "comparison": {
            "advisory_supports_preferred_outcome": synthesis["supports_preferred_outcome"],
            "advisory_confidence": synthesis["confidence"],
            "control_blocks_conclusion": skeptical["blocking_issue"],
            "control_confidence": skeptical["confidence"],
            "assumption_laundering_detected": len(audit["findings"]) > 0,
        },
    }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
