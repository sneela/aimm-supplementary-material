"""
Validate Output Schema for AIMM

This module defines the expected output schema for the AIMM framework.
It provides structural validation to ensure that outputs conform to the
required format and boundary constraints.

Note: This script performs schema and sanity checking only. Risk scoring logic,
thresholding heuristics, and signal weighting are handled elsewhere in the pipeline.
"""

from datetime import datetime
from typing import List

# Valid risk level categories
VALID_RISK_LEVELS = {"low", "medium", "high"}

# Common signal types that may contribute to risk assessment
# (This is not prescriptive; actual signals depend on the model)
COMMON_SIGNAL_TYPES = {
    "social_sentiment",
    "market_volatility",
    "trading_volume",
    "microstructure",
    "news_sentiment",
    "temporal_pattern",
}


def validate_output_schema(result: dict) -> None:
    """
    Validate that a result dictionary conforms to the expected AIMM output schema.
    
    Performs the following checks:
    1. All required fields are present
    2. risk_score is a float within [0, 1]
    3. risk_level is a valid category (low/medium/high)
    4. evaluation_date is a valid ISO 8601 date string
    5. contributing_signal_types is a list of non-empty strings
    
    Parameters
    ----------
    result : dict
        A dictionary representing a single output sample with required fields.
        
    Raises
    ------
    AssertionError
        If any required field is missing, has an incorrect type, or violates
        sanity bounds.
        
    Examples
    --------
    >>> synthetic_output = {
    ...     "risk_score": 0.72,
    ...     "risk_level": "medium",
    ...     "evaluation_date": "2025-12-28",
    ...     "contributing_signal_types": ["social_sentiment", "market_volatility"]
    ... }
    >>> validate_output_schema(synthetic_output)
    """
    
    required_fields = {
        "risk_score",
        "risk_level",
        "evaluation_date",
        "contributing_signal_types",
    }
    
    # Check that all required fields are present
    missing_fields = required_fields - set(result.keys())
    assert not missing_fields, (
        f"Missing required fields: {missing_fields}"
    )
    
    # Validate risk_score
    risk_score = result["risk_score"]
    assert isinstance(risk_score, (int, float)) and not isinstance(
        risk_score, bool
    ), (
        f"Field 'risk_score' must be numeric, got {type(risk_score).__name__}"
    )
    assert 0 <= risk_score <= 1, (
        f"Field 'risk_score' must be in [0, 1], got {risk_score}"
    )
    
    # Validate risk_level
    risk_level = result["risk_level"]
    assert isinstance(risk_level, str), (
        f"Field 'risk_level' must be a string, got {type(risk_level).__name__}"
    )
    assert risk_level.lower() in VALID_RISK_LEVELS, (
        f"Field 'risk_level' must be one of {VALID_RISK_LEVELS}, got '{risk_level}'"
    )
    
    # Validate evaluation_date (ISO 8601 format check)
    evaluation_date = result["evaluation_date"]
    assert isinstance(evaluation_date, str), (
        f"Field 'evaluation_date' must be a string, got {type(evaluation_date).__name__}"
    )
    try:
        datetime.fromisoformat(evaluation_date)
    except ValueError:
        raise AssertionError(
            f"Field 'evaluation_date' must be valid ISO 8601 format "
            f"(YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS), got '{evaluation_date}'"
        )
    
    # Validate contributing_signal_types
    signal_types = result["contributing_signal_types"]
    assert isinstance(signal_types, list), (
        f"Field 'contributing_signal_types' must be a list, "
        f"got {type(signal_types).__name__}"
    )
    assert len(signal_types) > 0, (
        "Field 'contributing_signal_types' must contain at least one signal type"
    )
    for signal_type in signal_types:
        assert isinstance(signal_type, str), (
            f"Each signal type must be a string, got {type(signal_type).__name__}"
        )
        assert len(signal_type) > 0, (
            "Signal types must be non-empty strings"
        )
    
    print(
        f"✓ Output schema validation passed for result with "
        f"risk_score={risk_score} and {len(signal_types)} contributing signals"
    )


if __name__ == "__main__":
    # Minimal synthetic output for demonstration
    # All values are purely synthetic and do not represent real risk assessments
    synthetic_output_1 = {
        "risk_score": 0.72,
        "risk_level": "medium",
        "evaluation_date": "2025-12-28",
        "contributing_signal_types": ["social_sentiment", "market_volatility"],
    }
    
    print("Validating synthetic output sample against AIMM output schema...\n")
    try:
        validate_output_schema(synthetic_output_1)
        print("Sample validation successful.\n")
    except AssertionError as e:
        print(f"Validation failed: {e}\n")
    
    # Example: Low risk output
    print("="*70)
    print("Validating low-risk synthetic output...\n")
    
    synthetic_output_2 = {
        "risk_score": 0.18,
        "risk_level": "low",
        "evaluation_date": "2025-12-27T14:30:00",
        "contributing_signal_types": ["market_volatility"],
    }
    
    try:
        validate_output_schema(synthetic_output_2)
        print("Sample validation successful.\n")
    except AssertionError as e:
        print(f"Validation failed: {e}\n")
    
    # Example: High risk output
    print("="*70)
    print("Validating high-risk synthetic output...\n")
    
    synthetic_output_3 = {
        "risk_score": 0.91,
        "risk_level": "high",
        "evaluation_date": "2025-12-26",
        "contributing_signal_types": [
            "social_sentiment",
            "trading_volume",
            "news_sentiment",
            "microstructure",
        ],
    }
    
    try:
        validate_output_schema(synthetic_output_3)
        print("Sample validation successful.\n")
    except AssertionError as e:
        print(f"Validation failed: {e}\n")
    
    # Example: Demonstrate validation failure with out-of-bounds risk_score
    print("="*70)
    print("Demonstrating validation failure (risk_score out of bounds)...\n")
    
    invalid_output_1 = synthetic_output_1.copy()
    invalid_output_1["risk_score"] = 1.5
    
    try:
        validate_output_schema(invalid_output_1)
    except AssertionError as e:
        print(f"Expected validation error: {e}\n")
    
    # Example: Demonstrate validation failure with invalid risk_level
    print("="*70)
    print("Demonstrating validation failure (invalid risk_level)...\n")
    
    invalid_output_2 = synthetic_output_1.copy()
    invalid_output_2["risk_level"] = "extreme"
    
    try:
        validate_output_schema(invalid_output_2)
    except AssertionError as e:
        print(f"Expected validation error: {e}\n")
    
    # Example: Demonstrate validation failure with malformed date
    print("="*70)
    print("Demonstrating validation failure (invalid date format)...\n")
    
    invalid_output_3 = synthetic_output_1.copy()
    invalid_output_3["evaluation_date"] = "12/28/2025"
    
    try:
        validate_output_schema(invalid_output_3)
    except AssertionError as e:
        print(f"Expected validation error: {e}\n")
    
    # Example: Demonstrate validation failure with empty signal types
    print("="*70)
    print("Demonstrating validation failure (empty signal types)...\n")
    
    invalid_output_4 = synthetic_output_1.copy()
    invalid_output_4["contributing_signal_types"] = []
    
    try:
        validate_output_schema(invalid_output_4)
    except AssertionError as e:
        print(f"Expected validation error: {e}\n")
