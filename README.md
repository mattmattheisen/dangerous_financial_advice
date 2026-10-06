# The Most Dangerous Financial Advice May Be the Advice That Looks the Smartest

This project began with a simple concern about the way people are starting to use large language models for financial decisions.

The obvious failure mode is easy to imagine: bad data goes in, a model hallucinates a fact, or a user forgets an important detail and gets a bad answer. That is not the problem I am most interested in.

The harder problem is what happens when the inputs are good, the analysis is detailed, the system uses several specialized agents, and the final recommendation still deserves less confidence than it appears to.

The central question is:

**Can a multi-agent financial-planning system become more confident without becoming more correct because its agents are not truly independent?**

A typical agentic workflow might divide the problem among separate systems for intake, retirement, portfolio construction, taxes, risk, and final synthesis. At first glance, that looks like multiple specialists checking one another's work. But if those agents consume the same upstream assumptions, inherit one another's conclusions, or rely on the same planning baseline, their agreement may be highly correlated.

Five agents agreeing is not necessarily the same thing as five independent opinions.

That distinction is the core of this project.

The prototype in this repository is designed to make that dependency structure visible. It includes a synthetic retirement-planning workflow, a skeptical control system, an assumption-provenance layer, and a presentation layer that deliberately looks like the sort of polished technical analysis a careful investor might trust.

The point is not to show that AI is bad at arithmetic. The point is to examine whether architecture itself can manufacture confidence.

## The problem

Suppose a planning agent establishes a sustainable spending figure. The retirement agent accepts it. The portfolio agent uses the retirement conclusion. The tax agent works from the projected withdrawal path. The risk agent evaluates the resulting portfolio. A synthesis agent then sees several specialists in agreement and increases its confidence.

Nothing in that chain requires anyone to make an obvious mistake.

The problem is that the apparent agreement may not be independent. Several conclusions may simply be descendants of the same premise.

This creates what I call **correlated agreement**: multiple agents appear to confirm a recommendation even though they share the same upstream reasoning path.

It can also create **assumption laundering**. An assumption enters the workflow in one form, is normalized into a planning input, then gets reused downstream until its original status becomes less obvious.

A related problem is **epistemic compression**. As information passes through layers of abstraction, context about where a number or conclusion came from can disappear. By the time the final report is produced, the user may see a clean recommendation, several confidence scores, and apparent specialist consensus without seeing how much of that consensus depends on the same ancestor premise.

This is why the project distinguishes between **detail density** and **evidentiary density**.

A report can contain a great deal of analysis without containing a great deal of independent evidence.

## What I built

The repository contains a synthetic multi-agent advisory workflow with separate modules for intake, retirement analysis, portfolio analysis, and recommendation synthesis. There is also a skeptical-control system whose job is not to improve the recommendation but to challenge it.

The control asks different questions:

Which conclusions are actually independent? Which agents share the same upstream premise? Which assumptions are inherited rather than revalidated? Does apparent agreement deserve to increase confidence? What would falsify the recommendation?

The project also includes a provenance layer that traces how a premise moves through the system. That matters because a recommendation can be mathematically transparent while remaining epistemically opaque.

You can show every calculation and still fail to show where the calculation got its authority.

The current prototype demonstrates the mechanism. It does not yet establish how often production LLM systems behave this way. That would require a larger empirical study using real model runs.

For that reason, the responsible claim is modest:

> We built a controlled prototype showing how multi-agent financial analysis can create false confidence when several agents are not truly independent.

That is enough to make the failure mode worth studying.

## Why this matters for sophisticated users

The user I care about is not the person who forgets to enter the pension or cannot read a brokerage statement.

It is the engineer with the spreadsheet.

The physician who tracks every assumption.

The programmer who wants to see the model.

The retiree who enters every account, every cash flow, every tax assumption, and every planning constraint.

That user may reasonably trust a system more when it shows its work, exposes assumptions, runs multiple specialist agents, and produces internally consistent results.

But internal consistency is not the same thing as independent verification.

A system can be extremely detailed and still be epistemically narrow.

That is the uncomfortable part.

## The historical thread

There is a useful connection here to several older ideas in computing.

Alan Turing asked whether a machine could produce behavior that appeared intelligent. This project asks a downstream question: once machines look intelligent, do we assign more confidence than the evidence deserves?

Claude Shannon is even closer to the problem. Information can be transmitted, transformed, compressed, and repeated without becoming more meaningful or more true. In a multi-agent system, repeated conclusions may create redundancy rather than new evidence.

Charles Petzold provides the architectural metaphor. Layers of abstraction make complex systems usable, but they can also hide what sits underneath them. Agentic systems have the same problem. The higher the stack becomes, the easier it is to lose sight of the original premise.

Norbert Wiener adds the feedback problem. Feedback can correct error, but it can also amplify it. A weak premise passed through several agreeing agents can become more persuasive simply because the system is reinforcing itself.

The question is therefore not just how many agents a system has.

It is how many independent reasoning paths it actually contains.

## Current direction

The first version of the project used planted ambiguities such as missing pension details to study assumption propagation. That was useful for building the architecture, but it is not the strongest version of the problem.

The project has since moved toward a harder question:

**Can the system create false confidence even when the investor's inputs are complete and correct?**

That is now the main direction of the work.

The repository is fully sandboxed. It uses synthetic investor scenarios and historical or simulated data only. There is no brokerage access, no trading capability, no client information, and no financial credentials.

The working title for the broader idea is the same as the title of this repository:

**The Most Dangerous Financial Advice May Be the Advice That Looks the Smartest.**

And the question underneath it is simpler:

**When five AI agents agree, are you really getting five opinions?**
