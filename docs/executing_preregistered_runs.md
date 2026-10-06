# Executing the Preregistered Scenario 001 Runs

Scenario 001 is frozen.

The next phase uses real LLM calls rather than the deterministic research simulator.

## Before the first run

Two environment variables are required:

`OPENAI_API_KEY`

and

`EXPERIMENT_MODEL`

The first time the runner executes, it creates:

`preregistration/model_lock.json`

After that file exists, the runner refuses to execute Scenario 001 with a different model.

This prevents model selection from becoming a post-hoc tuning variable.

## Install

From the repository root:

```bash
python -m pip install -r requirements.txt
```

## Execute one run first

```bash
python -m experiments.preregistered_llm_runner --run-id N01
```

This is not a pilot to tune prompts. It is the first observation in the frozen experiment.

## Score the run

```bash
python -m experiments.score_preregistered_run N01
```

The raw response remains preserved in:

`outputs/raw_runs/N01.json`

The automated score is stored separately so manual audit remains possible.

## Continue by condition

Example:

```bash
python -m experiments.preregistered_llm_runner --condition neutral --limit 19
```

Then repeat for outcome_pressure, skeptical_control, and ground_truth.

## Important evidence rule

Raw outputs are the primary record. Automated scoring can be wrong.

If scoring is later improved, raw model responses must remain unchanged and any scoring-method change must be versioned separately.

## Credential rule

API credentials must never be committed to GitHub.
