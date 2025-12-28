"""
Validate Input Feature Schema for AIMM

This module defines the expected input feature schema for the AIMM framework.
It provides structural validation to ensure that input data conforms to the
required format before being passed to downstream processing stages.

Note: This script performs schema validation only. Feature engineering,
computation, and derivation are handled elsewhere in the pipeline.
"""

# Define expected input features grouped by domain
# Social Media Features
SOCIAL_FEATURES = {
    "reddit_sentiment_score": "float",
    "twitter_sentiment_score": "float",
    "stocktwits_sentiment_score": "float",
    "social_volume_normalized": "float",
}

# Market Data Features
MARKET_FEATURES = {
    "open_price": "float",
    "high_price": "float",
    "low_price": "float",
    "close_price": "float",
    "volume": "int",
    "price_range": "float",
}

# Microstructure Features
MICROSTRUCTURE_FEATURES = {
    "bid_ask_spread": "float",
    "trades_count": "int",
    "large_trade_indicator": "bool",
}

# News and External Features
NEWS_FEATURES = {
    "news_sentiment_score": "float",
    "news_volume": "int",
}

# Temporal Features
TEMPORAL_FEATURES = {
    "day_of_week": "int",
    "is_trading_day": "bool",
}

# Consolidated required features dictionary
REQUIRED_FEATURES = {
    **SOCIAL_FEATURES,
    **MARKET_FEATURES,
    **MICROSTRUCTURE_FEATURES,
    **NEWS_FEATURES,
    **TEMPORAL_FEATURES,
}


def validate_input_schema(sample: dict) -> None:
    """
    Validate that a sample dictionary conforms to the expected AIMM input schema.
    
    Performs two checks:
    1. All required features are present
    2. Each feature has the correct type
    
    Parameters
    ----------
    sample : dict
        A dictionary representing a single input sample with feature names as keys.
        
    Raises
    ------
    AssertionError
        If any required feature is missing or has an incorrect type.
        
    Examples
    --------
    >>> synthetic_sample = {
    ...     "reddit_sentiment_score": 0.45,
    ...     "twitter_sentiment_score": 0.52,
    ...     "open_price": 145.30,
    ...     "volume": 1000000,
    ...     # ... other features
    ... }
    >>> validate_input_schema(synthetic_sample)
    """
    
    # Check that all required features are present
    missing_features = set(REQUIRED_FEATURES.keys()) - set(sample.keys())
    assert not missing_features, (
        f"Missing required features: {missing_features}"
    )
    
    # Check that each feature has the correct type
    for feature_name, expected_type in REQUIRED_FEATURES.items():
        feature_value = sample[feature_name]
        
        if expected_type == "float":
            assert isinstance(feature_value, (int, float)) and not isinstance(
                feature_value, bool
            ), (
                f"Feature '{feature_name}' expected type float, "
                f"got {type(feature_value).__name__} with value {feature_value}"
            )
        elif expected_type == "int":
            assert isinstance(feature_value, int) and not isinstance(
                feature_value, bool
            ), (
                f"Feature '{feature_name}' expected type int, "
                f"got {type(feature_value).__name__} with value {feature_value}"
            )
        elif expected_type == "bool":
            assert isinstance(feature_value, bool), (
                f"Feature '{feature_name}' expected type bool, "
                f"got {type(feature_value).__name__} with value {feature_value}"
            )
        else:
            raise ValueError(
                f"Unknown expected type '{expected_type}' for feature '{feature_name}'"
            )
    
    print(f"✓ Schema validation passed for sample with {len(sample)} features")


if __name__ == "__main__":
    # Minimal synthetic sample for demonstration
    # All values are purely synthetic and do not represent real market conditions
    minimal_synthetic_sample = {
        # Social Media Features
        "reddit_sentiment_score": 0.45,
        "twitter_sentiment_score": 0.52,
        "stocktwits_sentiment_score": 0.38,
        "social_volume_normalized": 0.75,
        # Market Data Features
        "open_price": 145.30,
        "high_price": 147.50,
        "low_price": 144.80,
        "close_price": 146.25,
        "volume": 2500000,
        "price_range": 2.70,
        # Microstructure Features
        "bid_ask_spread": 0.05,
        "trades_count": 12500,
        "large_trade_indicator": False,
        # News and External Features
        "news_sentiment_score": 0.55,
        "news_volume": 23,
        # Temporal Features
        "day_of_week": 2,  # Wednesday
        "is_trading_day": True,
    }
    
    print("Validating minimal synthetic sample against AIMM input schema...\n")
    try:
        validate_input_schema(minimal_synthetic_sample)
        print("\nSample validation successful.")
    except AssertionError as e:
        print(f"\nValidation failed: {e}")
    
    # Example: Demonstrate validation failure with missing feature
    print("\n" + "="*70)
    print("Demonstrating validation failure (missing feature)...\n")
    
    incomplete_sample = minimal_synthetic_sample.copy()
    del incomplete_sample["close_price"]
    
    try:
        validate_input_schema(incomplete_sample)
    except AssertionError as e:
        print(f"Expected validation error: {e}")
    
    # Example: Demonstrate validation failure with wrong type
    print("\n" + "="*70)
    print("Demonstrating validation failure (wrong type)...\n")
    
    wrong_type_sample = minimal_synthetic_sample.copy()
    wrong_type_sample["volume"] = 2500000.5  # Should be int, not float
    
    try:
        validate_input_schema(wrong_type_sample)
    except AssertionError as e:
        print(f"Expected validation error: {e}")
