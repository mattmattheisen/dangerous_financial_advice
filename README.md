# The Most Dangerous Financial Advice May Be the Advice That Looks the Smartest

This project is a controlled experiment in agentic AI and financial decision-making.

The central question is simple:

**Can a sophisticated multi-agent financial-advice system produce a highly confident, internally consistent recommendation that is materially wrong, and can added complexity make that error harder for a human user to detect?**

The experiment will simulate an AI-driven advisory workflow using specialized agents for areas such as financial planning, portfolio construction, retirement analysis, taxes, risk, and final recommendation synthesis.

Rather than measuring only whether the system produces a plausible answer, the project will examine how errors propagate through an agentic workflow, whether later agents detect or amplify those errors, and whether polished analysis can create false confidence.

A control system will be designed to emphasize skepticism, uncertainty, missing information, falsification, and reasons not to act.

The broader purpose is not to argue that AI should not be used in financial planning or investment analysis. It is to examine a more subtle risk:

**Sophistication is not the same thing as correctness.**

A recommendation can contain quantitative analysis, simulations, charts, multiple specialized agents, and persuasive explanations while still resting on a flawed assumption.

The project will remain fully sandboxed. It will use synthetic investor scenarios, historical or simulated market data, and no live brokerage access, trading capability, client information, or financial credentials.

## Core hypothesis

**Agentic depth may increase epistemic confidence faster than it increases epistemic reliability.**

The system may fail not because it is obviously unsophisticated, but because it is sophisticated enough to construct an excellent argument from a bad premise.

## Experimental design

The project compares two systems that receive the same synthetic household data.

### Advisory system

The advisory system is optimized to produce a recommendation. Its agents may include:

- intake and fact normalization
- financial planning
- portfolio construction
- retirement analysis
- tax analysis
- risk analysis
- final recommendation synthesis

### Skeptical control system

The control system is optimized to challenge the recommendation rather than improve its presentation. Its responsibilities include:

- identifying hidden or unsupported assumptions
- detecting missing information
- attempting to falsify key conclusions
- distinguishing model uncertainty from factual uncertainty
- identifying reasons not to act
- producing a skeptical synthesis independent of the advisory narrative

The control is intentionally not just another "smarter" advisory agent. It has a different objective function.

## What we will measure

Early experiments will ask:

1. Did the advisory system identify the planted defect?
2. If not, where did the defect first enter the workflow?
3. Did downstream agents detect, preserve, or amplify it?
4. Did the final system become more confident as more agents touched the analysis?
5. Did polished quantitative output make the recommendation appear more reliable?
6. Did the skeptical control identify the defect?
7. What evidence would have been required to falsify the recommendation earlier?
8. At what point did additional complexity stop improving reliability?

## Initial failure modes

Synthetic scenarios may deliberately contain subtle defects such as:

- a pension incorrectly treated as inflation-adjusted
- nominal and real spending assumptions mixed across agents
- an inherited IRA treated as a traditional IRA
- incorrect tax-basis assumptions
- inconsistent Social Security claiming ages
- a concentrated stock position assumed liquid without accounting for taxes
- a risk questionnaire that implicitly embeds a portfolio allocation
- inconsistent longevity assumptions between spouses
- return assumptions and volatility assumptions drawn from incompatible regimes

The objective is not to create absurd mistakes. The defects should be plausible enough to survive superficial review.

## A principle worth testing

> The questionnaire may be producing the portfolio partly because the questionnaire contains the portfolio.

A future experiment will test whether apparently neutral risk-tolerance questionnaires systematically steer users toward predetermined portfolio structures.

## Repository structure

```text
dangerous_financial_advice/
├── agents/          # Recommendation-producing agents
├── control/         # Skeptical and falsification agents
├── scenarios/       # Synthetic investor cases and planted defects
├── experiments/     # Experiment runners, comparisons, and scoring
├── data/            # Historical or simulated data only
├── outputs/         # Generated experiment artifacts
└── tests/           # Reproducibility and validation tests
```

## Safety boundaries

This repository is an experimental research environment, not a financial-advice product.

It will not:

- connect to brokerage accounts
- place trades
- use real client data
- store financial credentials
- generate instructions for autonomous execution in live accounts

All investor cases will be synthetic, and all market inputs will be historical or simulated.

## Project status

**Phase 1: experimental architecture and baseline scenario design.**

The first target is intentionally small: one synthetic household, one planted defect, a limited advisory workflow, a skeptical control workflow, and a measurable comparison of confidence versus correctness.
