# The Most Dangerous Financial Advice May Be the Advice That Looks the Smartest

This project is a controlled experiment in agentic AI and financial decision-making.

The central question is:

**Can a sophisticated multi-agent financial-advice system become more confident without becoming more correct because its agents are not truly independent?**

The project explores a failure mode that is subtler than bad data, obvious hallucinations, or missing client information.

What if the investor provides complete and accurate inputs?

What if the calculations are internally consistent?

What if multiple specialized agents analyze retirement, portfolio construction, taxes, risk, and final recommendation synthesis?

And what if all of those agents agree?

The key question is whether that agreement represents genuinely independent evidence or merely several downstream conclusions that share the same upstream premise.

The broader purpose is not to argue that AI should not be used in financial planning or investment analysis. It is to examine a more subtle risk:

**Sophistication is not the same thing as correctness.**

A recommendation can contain quantitative analysis, simulations, confidence scores, multiple specialized agents, and persuasive explanations while still creating more certainty than the underlying evidence deserves.

The project remains fully sandboxed. It uses synthetic investor scenarios, historical or simulated market data, and no live brokerage access, trading capability, client information, or financial credentials.

## Core hypothesis

**Agentic depth may increase epistemic confidence faster than it increases epistemic reliability.**

A five-agent system may appear to offer five independent opinions while actually containing only one or two independent reasoning paths.

The effective number of independent agents may therefore matter more than the nominal number of agents.

## The central failure mode: false independence

A typical multi-agent financial workflow might look like:

```text
Complete investor data
        ↓
Financial planning agent
        ↓
Retirement agent
        ↓
Portfolio agent
        ↓
Tax / risk agent
        ↓
Synthesis agent
        ↓
High-confidence recommendation
```

At first glance, the final synthesis may look like the product of several independent specialists.

But if each downstream agent consumes conclusions produced upstream, their agreement may be highly correlated.

Five agents agreeing is not necessarily the same thing as five independent opinions.

## Key concepts

### Correlated agreement

Multiple agents agree because they share the same upstream premise or reasoning path.

Agreement therefore looks stronger than the amount of independent evidence actually supports.

### Assumption laundering

An assumption moves through the workflow until its uncertain or model-dependent origin becomes less obvious.

The assumption may eventually appear as a settled fact simply because several downstream systems have reused it.

### Epistemic compression

As information moves through layers of abstraction, context about where a number or conclusion came from can disappear.

A detailed final recommendation may therefore reveal the calculation while obscuring the provenance of the premise.

### Detail density versus evidentiary density

**Detail density** describes how much analysis is visible.

**Evidentiary density** describes how much independent support actually exists for the conclusion.

A report can have very high detail density while having surprisingly low evidentiary density.

### Effective independence

The number of agents in a system is not necessarily the number of independent reasoning paths.

A five-agent system may have an effective independence closer to one or two if most of the agents inherit the same assumptions and conclusions.

## Experimental architecture

The project currently contains two broad systems.

### Advisory workflow

The advisory side is designed to resemble a sophisticated multi-agent financial-planning process.

Its modules include:

- intake and fact normalization
- retirement analysis
- portfolio analysis
- recommendation synthesis
- technical-user presentation
- confidence aggregation

Future versions may add tax, Social Security, estate-planning, and risk-specialist agents.

### Skeptical control

The control system has a different objective.

Its job is not to improve the recommendation.

Its job is to challenge it.

The control asks:

- Which conclusions are truly independent?
- Which agents share the same upstream premise?
- Which assumptions are inherited rather than revalidated?
- Is apparent specialist agreement actually correlated?
- What evidence would falsify the recommendation?
- Should agreement increase confidence at all?

The project includes an assumption-provenance layer to trace these dependencies.

## Research question

The stronger version of Scenario 001 does not depend on a careless investor or missing obvious information.

The synthetic user is technically literate, detail-oriented, and comfortable with spreadsheets, assumptions, scenario analysis, and numerical precision.

The relevant question is:

> **Can a meticulous user provide good data and still be misled because the architecture creates pseudo-consensus?**

That is a harder and more interesting test than simple garbage-in, garbage-out.

## What the prototype currently demonstrates

The current prototype demonstrates the mechanism by which:

1. a conclusion can enter the workflow upstream
2. several specialist agents can inherit that conclusion
3. downstream consistency can look like independent confirmation
4. synthesis can reward apparent agreement with higher confidence
5. a skeptical control can reveal that the agreement is causally dependent

The prototype does **not** yet establish how often real production LLM systems exhibit this behavior.

That requires empirical model runs.

## Podcast / communication framing

The project is suitable for explaining the risk conceptually before the full empirical study is complete.

The responsible framing is:

> We built a controlled prototype to show how this failure could happen. We have not yet completed the larger empirical study needed to measure how often real models actually do it.

The working episode title is:

**The Most Dangerous Financial Advice May Be the Advice That Looks the Smartest**

A second useful question for the episode is:

> **When five AI agents agree, are you really getting five opinions?**

## Historical framing

The project has natural connections to several foundational ideas in computing and information theory.

**Alan Turing** asked whether machines could produce behavior that appears intelligent.

This project asks a downstream question:

> Once machines appear intelligent, can the structure of their reasoning cause humans to assign more confidence than the evidence deserves?

**Claude Shannon** separated information from meaning and showed the importance of redundancy and information structure.

A related question here is:

> When several agents repeat or transform the same upstream premise, how much genuinely new information has been added?

**Charles Petzold** provides a useful architectural metaphor through layers of abstraction.

As agentic systems accumulate layers, the user may see increasingly sophisticated outputs while losing visibility into the assumptions underneath them.

**Norbert Wiener** provides the feedback perspective.

Agentic systems can either correct weak premises or amplify them through positive feedback.

## A principle worth testing

> The questionnaire may be producing the portfolio partly because the questionnaire contains the portfolio.

A future experiment will examine whether apparently neutral planning or risk-tolerance systems embed the portfolio or recommendation they later appear to discover.

## Repository structure

```text
dangerous_financial_advice/
├── agents/              # Recommendation-producing agents
├── control/             # Skeptical and falsification agents
├── scenarios/           # Synthetic investor cases
├── experiments/         # Runners, comparisons, scoring, provenance
├── podcast_pilot/       # Exploratory podcast-oriented experiment
├── preregistration/     # Frozen full-study design
├── docs/                # Research notes and visual explanations
├── data/                # Historical or simulated data only
├── outputs/             # Generated experiment artifacts
└── tests/               # Reproducibility and validation tests
```

## Safety boundaries

This repository is an experimental research environment, not a financial-advice product.

It will not:

- connect to brokerage accounts
- place trades
- use real client data
- store financial credentials
- generate autonomous execution instructions for live accounts

All investor cases are synthetic, and all market inputs are historical or simulated.

## Project status

**Current phase: architectural prototype and communication design.**

The original experiment began with planted ambiguities and assumption propagation.

The project has since evolved toward a stronger question:

**Can multi-agent architecture itself manufacture false confidence even when the investor's inputs are complete and correct?**

That is now the primary direction of the project.
