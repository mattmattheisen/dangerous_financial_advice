# Advisory agents

This directory contains the recommendation-producing side of the experiment.

The advisory workflow is intentionally separated into specialized roles so the project can observe where assumptions enter, how they propagate, and whether later agents challenge or merely inherit them.

Planned modules:

- `intake_agent.py`
- `financial_planning_agent.py`
- `portfolio_agent.py`
- `retirement_agent.py`
- `tax_agent.py`
- `risk_agent.py`
- `synthesis_agent.py`

Each agent should expose its assumptions, inputs, outputs, confidence, and unresolved questions rather than returning only prose.
