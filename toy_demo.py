"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  ILLUSTRATIVE DEMONSTRATION ONLY                                          ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║                                                                           ║
║  This script is entirely synthetic and illustrative.                      ║
║  It DOES NOT represent the AIMM model, feature engineering, or any       ║
║  real risk computation logic.                                            ║
║                                                                           ║
║  Purpose: Demonstrate the schema validation pipeline using toy data.     ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Toy Demonstration Workflow

This module illustrates how synthetic data flows through the AIMM input and
output validation schemas. All data is randomly generated and has no connection
to real market conditions, real features, or real risk assessment.

The workflow:
1. Generate random synthetic input features
2. Perform a trivial operation (averaging) to produce a fake risk score
3. Assign an illustrative risk level based on simple bins
4. Validate against the defined schemas
5. Display results

This is a learning aid only.
"""

import random
from datetime import datetime
from validate_inputs import validate_input_schema, REQUIRED_FEATURES
from validate_outputs import validate_output_schema


def generate_random_synthetic_inputs() -> dict:
    """
    Generate completely random synthetic input features.
    
    All values are randomly sampled and have no relationship to real
    market data, sentiment analysis, or any actual computation.
    
    Returns
    -------
    dict
        A dictionary with all required input features populated with random values.
    """
    synthetic_sample = {}
    
    # Social Media Features (random floats in [0, 1])
    synthetic_sample["reddit_sentiment_score"] = random.uniform(0, 1)
    synthetic_sample["twitter_sentiment_score"] = random.uniform(0, 1)
    synthetic_sample["stocktwits_sentiment_score"] = random.uniform(0, 1)
    synthetic_sample["social_volume_normalized"] = random.uniform(0, 1)
    
    # Market Data Features (random but with plausible ranges)
    base_price = random.uniform(50, 200)
    synthetic_sample["open_price"] = base_price
    synthetic_sample["high_price"] = base_price * random.uniform(1.0, 1.05)
    synthetic_sample["low_price"] = base_price * random.uniform(0.95, 1.0)
    synthetic_sample["close_price"] = base_price * random.uniform(0.98, 1.02)
    synthetic_sample["volume"] = random.randint(500000, 5000000)
    synthetic_sample["price_range"] = (
        synthetic_sample["high_price"] - synthetic_sample["low_price"]
    )
    
    # Microstructure Features
    synthetic_sample["bid_ask_spread"] = random.uniform(0.01, 0.5)
    synthetic_sample["trades_count"] = random.randint(5000, 50000)
    synthetic_sample["large_trade_indicator"] = random.choice([True, False])
    
    # News and External Features
    synthetic_sample["news_sentiment_score"] = random.uniform(0, 1)
    synthetic_sample["news_volume"] = random.randint(5, 100)
    
    # Temporal Features
    synthetic_sample["day_of_week"] = random.randint(0, 6)
    synthetic_sample["is_trading_day"] = random.choice([True, False])
    
    return synthetic_sample


def compute_illustrative_risk_score(synthetic_inputs: dict) -> float:
    """
    Compute a fake risk score using a trivial operation.
    
    This is NOT how AIMM computes risk. This is merely averaging a subset
    of random inputs with additional noise. It serves no predictive purpose.
    
    Parameters
    ----------
    synthetic_inputs : dict
        Dictionary of synthetic input features
        
    Returns
    -------
    float
        A "risk score" in [0, 1] produced by averaging + random noise
    """
    # Average some arbitrary features (no semantic meaning)
    selected_values = [
        synthetic_inputs["reddit_sentiment_score"],
        synthetic_inputs["twitter_sentiment_score"],
        synthetic_inputs["social_volume_normalized"],
        synthetic_inputs["news_sentiment_score"],
    ]
    
    base_score = sum(selected_values) / len(selected_values)
    
    # Add random noise to show that this is purely synthetic
    noise = random.uniform(-0.1, 0.1)
    final_score = base_score + noise
    
    # Clip to [0, 1]
    return max(0.0, min(1.0, final_score))


def assign_illustrative_risk_level(risk_score: float) -> str:
    """
    Assign a risk level based on simple illustrative bins.
    
    This uses arbitrary thresholds for demonstration purposes only.
    It has no relationship to actual risk assessment.
    
    Parameters
    ----------
    risk_score : float
        A score in [0, 1]
        
    Returns
    -------
    str
        One of: "low", "medium", "high"
    """
    if risk_score < 0.33:
        return "low"
    elif risk_score < 0.67:
        return "medium"
    else:
        return "high"


def run_toy_demo():
    """
    Run the complete toy demonstration workflow.
    
    1. Generate synthetic inputs
    2. Validate input schema
    3. Compute fake risk score
    4. Assign illustrative risk level
    5. Validate output schema
    6. Display results
    """
    
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  AIMM Toy Demonstration - Synthetic Data Workflow".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Step 1: Generate synthetic inputs
    print("STEP 1: Generate Random Synthetic Input Features")
    print("-" * 78)
    
    synthetic_inputs = generate_random_synthetic_inputs()
    
    print(f"Generated {len(synthetic_inputs)} synthetic input features:")
    print(f"  - Social: reddit, twitter, stocktwits, social_volume")
    print(f"  - Market: price levels (open/high/low/close), volume, spread")
    print(f"  - Microstructure: bid_ask_spread, trades_count, large_trade_indicator")
    print(f"  - News: sentiment, volume")
    print(f"  - Temporal: day_of_week, is_trading_day")
    print()
    
    # Step 2: Validate input schema
    print("STEP 2: Validate Input Schema")
    print("-" * 78)
    
    try:
        validate_input_schema(synthetic_inputs)
        print()
    except AssertionError as e:
        print(f"ERROR: {e}\n")
        return
    
    # Step 3: Compute fake risk score
    print("STEP 3: Compute Illustrative Risk Score (Trivial Operation)")
    print("-" * 78)
    
    risk_score = compute_illustrative_risk_score(synthetic_inputs)
    print(f"Risk Score (from averaging 4 random features + noise): {risk_score:.4f}")
    print()
    
    # Step 4: Assign illustrative risk level
    print("STEP 4: Assign Illustrative Risk Level")
    print("-" * 78)
    
    risk_level = assign_illustrative_risk_level(risk_score)
    print(f"Risk Level (from arbitrary bins): {risk_level.upper()}")
    print("  (low < 0.33, medium < 0.67, high >= 0.67)")
    print()
    
    # Step 5: Construct output and validate
    print("STEP 5: Construct Output and Validate Schema")
    print("-" * 78)
    
    today = datetime.now().date().isoformat()
    
    synthetic_output = {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "evaluation_date": today,
        "contributing_signal_types": [
            "reddit_sentiment",
            "twitter_sentiment",
            "social_volume",
            "news_sentiment",
        ],
    }
    
    try:
        validate_output_schema(synthetic_output)
        print()
    except AssertionError as e:
        print(f"ERROR: {e}\n")
        return
    
    # Step 6: Display results
    print("STEP 6: Summary of Output")
    print("-" * 78)
    print(f"Risk Score:              {synthetic_output['risk_score']:.4f}")
    print(f"Risk Level:              {synthetic_output['risk_level']}")
    print(f"Evaluation Date:         {synthetic_output['evaluation_date']}")
    print(f"Contributing Signals:    {', '.join(synthetic_output['contributing_signal_types'])}")
    print()
    
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  Demonstration Complete".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "  Remember: This is entirely synthetic and illustrative.".center(78) + "║")
    print("║" + "  It demonstrates the schema, not the AIMM model.".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    run_toy_demo()
