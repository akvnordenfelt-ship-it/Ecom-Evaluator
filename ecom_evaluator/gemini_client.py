"""Backward-compatible alias — evaluation engine is Anthropic-only."""

from ecom_evaluator.evaluation_engine import (
    build_input_context,
    parse_json_phase,
    run_phase_with_retries,
    run_product_evaluation,
    run_shark_tank_analysis,
)

__all__ = [
    "build_input_context",
    "parse_json_phase",
    "run_phase_with_retries",
    "run_product_evaluation",
    "run_shark_tank_analysis",
]
