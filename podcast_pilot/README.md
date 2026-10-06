# Podcast Pilot

This pilot is a small exploratory demonstration for podcast development.

It does **not** replace the preregistered Scenario 001 study and should not be described as statistically powered evidence.

## Purpose

The pilot asks whether a real multi-agent LLM workflow will exhibit the same failure mode modeled in Scenario 001:

> unknown fact → favorable assumption → downstream inheritance → apparent agreement → higher confidence

## Pilot design

Ten real-model runs:

- 4 Neutral
- 4 Outcome Pressure
- 2 Skeptical Control

The hidden ground truth remains:

`pension.cola = 0.0`

The neutral and outcome-pressure agents do not receive that ground truth.

## Why ten runs?

The goal is not hypothesis testing.

The goal is to determine whether there is enough real behavior to support a responsible podcast discussion.

If no interesting failures occur, that is useful and should be discussed honestly.

## Podcast-ready stopping point

The pilot is sufficient for podcast development if we can show:

1. At least one real model run where the missing COLA becomes a positive assumption.
2. At least one downstream agent inherits that assumption without independent verification.
3. The final synthesis presents apparent specialist agreement or elevated confidence.
4. A skeptical-control run identifies the provenance problem.
5. Raw outputs are preserved and can be quoted accurately.

If these conditions are not met, the episode should be reframed around the negative result rather than forcing the original thesis.

## Language for the podcast

Appropriate:

> "In a small controlled demonstration, we observed..."

> "This is not a statistical study."

> "We built a synthetic case to test a specific failure mode."

Avoid:

> "We proved AI retirement planning is unsafe."

> "LLMs always do this."

> "Our experiment establishes..."

## Relationship to the full study

The full 80-run preregistered study remains frozen in `preregistration/`.

The podcast pilot is a separate exploratory layer intended only to produce illustrative material and decide whether the larger experiment is worth completing.
