"""Generate the polished technical-user artifact for Scenario 001."""
from __future__ import annotations

import json
from pathlib import Path

from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent
from experiments.technical_user_report import build_report_data, render_markdown

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "scenarios" / "scenario_001.json"
OUTPUT_PATH = ROOT / "outputs" / "scenario_001_technical_report.md"
JSON_OUTPUT_PATH = ROOT / "outputs" / "scenario_001_technical_report.json"


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

    report = build_report_data(scenario, advisory)

    JSON_OUTPUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    OUTPUT_PATH.write_text(render_markdown(report), encoding="utf-8")

    print(render_markdown(report))


if __name__ == "__main__":
    main()
