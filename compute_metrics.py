"""
Compute Evaluation Metrics for Manipulation Detection

This module provides standard metrics for evaluating manipulation detection systems.
All implementations are independent of AIMM internals and work with generic arrays.

The metrics included are:
- Precision: fraction of positive predictions that are correct
- Recall: fraction of actual positives that were detected
- F1 Score: harmonic mean of precision and recall
- ROC AUC: area under the receiver operating characteristic curve
- Detection Delay: time difference between actual event and detection

Metrics are provided for evaluation transparency only and
do not reveal AIMM internal logic.
"""

from typing import List, Tuple, Union
from datetime import datetime, timedelta


def precision(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate precision: TP / (TP + FP)
    
    Precision answers: Of all positive predictions made, how many were correct?
    
    Parameters
    ----------
    y_true : List[int]
        Ground truth binary labels (0 or 1)
    y_pred : List[int]
        Predicted binary labels (0 or 1)
        
    Returns
    -------
    float
        Precision score in [0, 1]. Returns 0 if no positive predictions.
        
    Examples
    --------
    >>> y_true = [0, 1, 1, 0, 1]
    >>> y_pred = [0, 1, 0, 0, 1]
    >>> precision(y_true, y_pred)
    1.0
    """
    assert len(y_true) == len(y_pred), "Length mismatch between y_true and y_pred"
    
    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    fp = sum(t == 0 and p == 1 for t, p in zip(y_true, y_pred))
    
    if tp + fp == 0:
        return 0.0
    
    return tp / (tp + fp)


def recall(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate recall (sensitivity): TP / (TP + FN)
    
    Recall answers: Of all actual positive events, what fraction was detected?
    
    Parameters
    ----------
    y_true : List[int]
        Ground truth binary labels (0 or 1)
    y_pred : List[int]
        Predicted binary labels (0 or 1)
        
    Returns
    -------
    float
        Recall score in [0, 1]. Returns 0 if no actual positives.
        
    Examples
    --------
    >>> y_true = [0, 1, 1, 0, 1]
    >>> y_pred = [0, 1, 0, 0, 1]
    >>> recall(y_true, y_pred)
    0.6666...
    """
    assert len(y_true) == len(y_pred), "Length mismatch between y_true and y_pred"
    
    tp = sum(t == 1 and p == 1 for t, p in zip(y_true, y_pred))
    fn = sum(t == 1 and p == 0 for t, p in zip(y_true, y_pred))
    
    if tp + fn == 0:
        return 0.0
    
    return tp / (tp + fn)


def f1_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate F1 score: 2 * (precision * recall) / (precision + recall)
    
    F1 score is the harmonic mean of precision and recall. It provides a
    single metric that balances both concerns.
    
    Parameters
    ----------
    y_true : List[int]
        Ground truth binary labels (0 or 1)
    y_pred : List[int]
        Predicted binary labels (0 or 1)
        
    Returns
    -------
    float
        F1 score in [0, 1]. Returns 0 if both precision and recall are 0.
        
    Examples
    --------
    >>> y_true = [0, 1, 1, 0, 1]
    >>> y_pred = [0, 1, 0, 0, 1]
    >>> f1_score(y_true, y_pred)
    0.8
    """
    assert len(y_true) == len(y_pred), "Length mismatch between y_true and y_pred"
    
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    
    if prec + rec == 0:
        return 0.0
    
    return 2 * (prec * rec) / (prec + rec)


def roc_auc(y_true: List[int], y_scores: List[float]) -> float:
    """
    Calculate the area under the receiver operating characteristic curve.
    
    ROC AUC measures the model's ability to distinguish between positive and
    negative classes across all decision thresholds. A value of 1.0 indicates
    perfect separation; 0.5 indicates random classification.
    
    This implementation uses scipy/sklearn if available. If those libraries
    are not installed, it provides a pure Python implementation using the
    trapezoidal rule.
    
    Parameters
    ----------
    y_true : List[int]
        Ground truth binary labels (0 or 1)
    y_scores : List[float]
        Predicted scores or probabilities, typically in [0, 1]
        
    Returns
    -------
    float
        ROC AUC score in [0, 1]
        
    Examples
    --------
    >>> y_true = [0, 0, 1, 1]
    >>> y_scores = [0.1, 0.4, 0.35, 0.8]
    >>> roc_auc(y_true, y_scores)
    0.75
    """
    assert len(y_true) == len(y_scores), "Length mismatch between y_true and y_scores"
    assert all(0 <= s <= 1 for s in y_scores), "y_scores must be in [0, 1]"
    
    try:
        from sklearn.metrics import roc_auc_score
        return float(roc_auc_score(y_true, y_scores))
    except ImportError:
        # Pure Python implementation using the Mann-Whitney U statistic
        pos_scores = [s for t, s in zip(y_true, y_scores) if t == 1]
        neg_scores = [s for t, s in zip(y_true, y_scores) if t == 0]
        
        if not pos_scores or not neg_scores:
            return 0.5
        
        # Count concordant and discordant pairs
        concordant = sum(
            1 for pos in pos_scores for neg in neg_scores if pos > neg
        )
        discordant = sum(
            1 for pos in pos_scores for neg in neg_scores if pos < neg
        )
        
        total_pairs = len(pos_scores) * len(neg_scores)
        
        if total_pairs == 0:
            return 0.5
        
        return concordant / total_pairs


def detection_delay(
    true_event_dates: List[Union[str, datetime]],
    detected_dates: List[Union[str, datetime]],
) -> dict:
    """
    Calculate detection delay: time between actual event and detection.
    
    For each true event, finds the nearest detection and calculates the delay.
    Delays can be negative (detection before event) or positive (detection after event).
    
    Parameters
    ----------
    true_event_dates : List[Union[str, datetime]]
        Dates when actual events occurred. Strings should be ISO 8601 format.
    detected_dates : List[Union[str, datetime]]
        Dates when events were detected. Strings should be ISO 8601 format.
        
    Returns
    -------
    dict
        Dictionary with keys:
        - 'mean_delay_days': average delay in days (float)
        - 'max_delay_days': maximum delay in days (int)
        - 'min_delay_days': minimum delay in days (int)
        - 'detection_rate': fraction of events with a detection (float)
        
    Examples
    --------
    >>> true_dates = ["2025-12-24", "2025-12-25"]
    >>> detected_dates = ["2025-12-25", "2025-12-27"]
    >>> result = detection_delay(true_dates, detected_dates)
    >>> result['mean_delay_days']
    1.5
    """
    
    def parse_date(d: Union[str, datetime]) -> datetime:
        if isinstance(d, datetime):
            return d
        return datetime.fromisoformat(d)
    
    true_dates_parsed = [parse_date(d) for d in true_event_dates]
    detected_dates_parsed = [parse_date(d) for d in detected_dates]
    
    if not true_dates_parsed:
        return {
            "mean_delay_days": 0.0,
            "max_delay_days": 0,
            "min_delay_days": 0,
            "detection_rate": 0.0,
        }
    
    # For each true event, find nearest detection
    delays = []
    detected_count = 0
    
    for true_date in true_dates_parsed:
        if detected_dates_parsed:
            # Find nearest detected date
            nearest_detection = min(
                detected_dates_parsed,
                key=lambda x: abs((x - true_date).total_seconds()),
            )
            delay_days = (nearest_detection - true_date).days
            delays.append(delay_days)
            detected_count += 1
    
    if not delays:
        return {
            "mean_delay_days": 0.0,
            "max_delay_days": 0,
            "min_delay_days": 0,
            "detection_rate": 0.0,
        }
    
    return {
        "mean_delay_days": sum(delays) / len(delays),
        "max_delay_days": max(delays),
        "min_delay_days": min(delays),
        "detection_rate": detected_count / len(true_dates_parsed),
    }


if __name__ == "__main__":
    print("=" * 70)
    print("SYNTHETIC EVALUATION METRICS DEMONSTRATION")
    print("=" * 70)
    
    # Synthetic dataset: binary predictions
    y_true = [0, 0, 1, 1, 1, 0, 1, 0, 1, 0]
    y_pred = [0, 1, 1, 0, 1, 0, 1, 1, 1, 0]
    
    print("\nBinary Classification Metrics")
    print("-" * 70)
    print(f"y_true:  {y_true}")
    print(f"y_pred:  {y_pred}")
    print(f"\nPrecision: {precision(y_true, y_pred):.4f}")
    print(f"Recall:    {recall(y_true, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")
    
    # Synthetic dataset: probabilistic predictions
    y_scores = [0.1, 0.3, 0.9, 0.2, 0.8, 0.15, 0.85, 0.4, 0.95, 0.05]
    
    print("\n" + "-" * 70)
    print("Probabilistic Predictions (for ROC AUC)")
    print("-" * 70)
    print(f"y_true:   {y_true}")
    print(f"y_scores: {y_scores}")
    print(f"\nROC AUC:   {roc_auc(y_true, y_scores):.4f}")
    
    # Synthetic dataset: temporal detection
    true_event_dates = [
        "2025-12-20",
        "2025-12-22",
        "2025-12-25",
        "2025-12-28",
    ]
    detected_dates = [
        "2025-12-21",
        "2025-12-23",
        "2025-12-26",
        "2025-12-29",
    ]
    
    print("\n" + "-" * 70)
    print("Detection Delay Analysis")
    print("-" * 70)
    print(f"True Event Dates:  {true_event_dates}")
    print(f"Detected Dates:    {detected_dates}")
    
    delay_metrics = detection_delay(true_event_dates, detected_dates)
    print(f"\nMean Detection Delay:    {delay_metrics['mean_delay_days']:.2f} days")
    print(f"Max Detection Delay:     {delay_metrics['max_delay_days']} days")
    print(f"Min Detection Delay:     {delay_metrics['min_delay_days']} days")
    print(f"Detection Rate:          {delay_metrics['detection_rate']:.2%}")
    
    # Edge case: perfect predictions
    print("\n" + "=" * 70)
    print("EDGE CASE: Perfect Predictions")
    print("=" * 70)
    y_perfect = [0, 1, 1, 0]
    y_perfect_pred = [0, 1, 1, 0]
    
    print(f"y_true: {y_perfect}")
    print(f"y_pred: {y_perfect_pred}")
    print(f"\nPrecision: {precision(y_perfect, y_perfect_pred):.4f}")
    print(f"Recall:    {recall(y_perfect, y_perfect_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_perfect, y_perfect_pred):.4f}")
