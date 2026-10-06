"""Generate Scenario 001 assumption provenance artifacts."""
from __future__ import annotations

import json
from pathlib import Path

from agents import intake_agent, retirement_agent, portfolio_agent, synthesis_agent
from experiments.assumption_provenance import build_provenance, to_mermaid

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "scenarios" / "scenario_001.json"
JSON_OUTPUT = ROOT / "outputs" / "scenario_001_provenance.json"
MD_OUTPUT = ROOT / "outputs" / "scenario_001_provenance.md"


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

    provenance = build_provenance(scenario, advisory)
    mermaid = to_mermaid(provenance)

    JSON_OUTPUT.write_text(json.dumps(provenance, indent=2), encoding="utf-8")

    markdown = f"""# Scenario 001 Assumption Provenance

This artifact tracks the pension COLA assumption through the synthetic advisory workflow.

## Provenance graph

```mermaid
{mermaid}
```

## Interpretation

The source record does not specify a pension COLA.

The intake agent resolves that missing fact by assuming the plan's general inflation rate. The value then stops behaving like an open question and starts behaving like a normalized input.

The retirement layer inherits the value without revalidation. The portfolio layer then inherits the retirement conclusion. The synthesis layer interprets downstream consistency as cross-agent agreement and uses that agreement to increase confidence.

The apparent corroboration is therefore not independent evidence. It is correlated evidence descending from one unsupported assumption.

## Research question

**At what point does an assumption stop looking like an assumption to the human reader?**

That transition is the core object of study in Scenario 001.
"""
    MD_OUTPUT.write_text(markdown, encoding="utf-8")

    print(json.dumps(provenance, indent=2))
    print(f"\nWrote {JSON_OUTPUT}")
    print(f"Wrote {MD_OUTPUT}")


if __name__ == "__main__":
    main()
