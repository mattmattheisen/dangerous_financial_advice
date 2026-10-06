"""Presentation conditions for Scenario 001."""
from __future__ import annotations

PRESENTATION_CONDITIONS = {
    "sparse": {
        "show_assumptions_table": False,
        "show_agent_confidence": False,
        "show_sensitivity_summary": False,
        "show_cross_agent_agreement": False,
        "show_provenance_first": False,
        "description": "Minimal conclusion-focused presentation.",
    },
    "technical": {
        "show_assumptions_table": True,
        "show_agent_confidence": True,
        "show_sensitivity_summary": True,
        "show_cross_agent_agreement": True,
        "show_provenance_first": False,
        "description": "Detail-dense presentation designed for a technically literate user.",
    },
    "provenance_first": {
        "show_assumptions_table": True,
        "show_agent_confidence": True,
        "show_sensitivity_summary": True,
        "show_cross_agent_agreement": True,
        "show_provenance_first": True,
        "description": "Same analysis, but assumption origin and dependency structure are shown before conclusions.",
    },
}
