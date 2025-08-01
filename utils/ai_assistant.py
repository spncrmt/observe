"""
ai_assistant.py
This module contains helper functions for integrating AI capabilities into the
Observe AI dashboard. It includes:

1. Functions for detecting anomalies in metrics using simple statistical
   techniques (z‑scores and moving averages).
2. A root cause analysis routine that correlates anomalies with nearby log
   messages to propose likely causes.
3. A function to construct prompts and call the OpenAI API for natural language
   question answering and summarization.

The aim is to provide interpretable and beginner‑friendly AI behaviors. Each
function returns not only the result but also metadata explaining how the
result was produced. This transparency aligns with the UX for AI principles
adopted in this project.
"""

import os
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

# Import the new production-grade detection model
try:
    from .detection_model import detect_anomalies_custom, explain_root_cause
except ImportError:
    # Fallback if the new module isn't available
    detect_anomalies_custom = None
    explain_root_cause = None

# Import custom AI model interface
try:
    from .custom_ai_model import get_ai_model
    custom_ai_available = True
except ImportError:
    custom_ai_available = False

# Optional import: If openai package is unavailable, we handle ImportError gracefully
try:
    import openai
except ImportError:
    openai = None  # type: ignore


def detect_anomalies(
    metrics_df: pd.DataFrame,
    column: str = "cpu_usage",
    window: int = 60,
    z_threshold: float = 3.0,
) -> pd.DataFrame:
    """Detect anomalies in a metric column using rolling z‑scores.

    The function computes a rolling mean and standard deviation over a specified
    window. A point is considered anomalous if its z‑score exceeds the
    specified threshold. Returns a DataFrame with anomaly flags and z‑scores.

    Parameters
    ----------
    metrics_df : DataFrame
        DataFrame containing time‑series metrics.
    column : str, optional
        Name of the metric column to analyze. Default is "cpu_usage".
    window : int, optional
        Size of the rolling window (in rows) for mean and std. Default is 60.
    z_threshold : float, optional
        Z‑score threshold for marking anomalies. Default is 3.0.

    Returns
    -------
    DataFrame
        Original DataFrame with two additional columns: ``z_score`` and ``anomaly``.
    """
    # Use the new production-grade detection model if available
    if detect_anomalies_custom is not None:
        # We need logs_df for the new model, but the old interface doesn't provide it
        # Create an empty logs DataFrame as fallback
        logs_df = pd.DataFrame(columns=['timestamp', 'level', 'message'])
        logs_df['timestamp'] = pd.to_datetime([])
        
        try:
            return detect_anomalies_custom(
                metrics_df=metrics_df,
                logs_df=logs_df,
                target_column=column,
                window=window,
                z_threshold=z_threshold
            )
        except Exception as e:
            # Fall back to original implementation if new model fails
            print(f"Warning: New detection model failed, falling back to original: {e}")
    
    # Original implementation as fallback
    data = metrics_df.copy()
    if column not in data.columns:
        raise ValueError(f"Column '{column}' not found in metrics DataFrame")

    # Compute rolling mean and standard deviation
    rolling_mean = data[column].rolling(window=window, min_periods=1, center=False).mean()
    rolling_std = data[column].rolling(window=window, min_periods=1, center=False).std(ddof=0)
    # Avoid division by zero
    rolling_std = rolling_std.replace(0, 1e-6)

    # Compute z‑scores
    z_scores = (data[column] - rolling_mean) / rolling_std
    data["z_score"] = z_scores
    # Mark anomalies
    data["anomaly"] = (abs(z_scores) > z_threshold)
    return data


def root_cause_analysis(
    metrics_df: pd.DataFrame,
    logs_df: pd.DataFrame,
    anomaly_col: str = "anomaly",
    metric_column: str = "cpu_usage",
    time_window_minutes: int = 10,
) -> Dict[str, object]:
    """Perform a simple root cause analysis by correlating anomalies with log messages.

    This function looks for time ranges where anomalies occur in the metrics and
    extracts log messages within a specified time window around those anomalies.
    It then summarizes the frequency of error messages to propose likely causes.

    Parameters
    ----------
    metrics_df : DataFrame
        Metrics DataFrame with an ``anomaly`` boolean column.
    logs_df : DataFrame
        Logs DataFrame containing at least ``timestamp`` and ``message`` columns.
    anomaly_col : str, optional
        Name of the anomaly flag column. Default is ``anomaly``.
    metric_column : str, optional
        Name of the metric column used to describe the anomaly. Default is
        ``cpu_usage``.
    time_window_minutes : int, optional
        How many minutes before and after an anomaly timestamp to include in
        log analysis. Default is 10 minutes.

    Returns
    -------
    dict
        Dictionary containing details about anomalies and likely root causes.
    """
    # Use the new production-grade root cause analysis if available
    if explain_root_cause is not None:
        try:
            # The new function expects the anomalies DataFrame directly
            # and returns a list of dictionaries instead of the old format
            rca_results = explain_root_cause(
                metrics_df=metrics_df,
                logs_df=logs_df,
                anomalies_df=metrics_df,  # metrics_df should already have anomaly column
                time_window_minutes=time_window_minutes,
                max_analysis_count=10
            )
            
            # Convert to the expected format for backward compatibility
            analysis = []
            for result in rca_results:
                analysis.append({
                    "timestamp": result["timestamp"],
                    "metric_value": result["metric_value"],
                    "logs_analyzed": result["logs_analyzed"],
                    "error_counts": result["error_counts"]
                })
            
            return {
                "analysis": analysis,
                "description": f"Enhanced root cause analysis using production-grade detection model. Analyzed logs within ±{time_window_minutes} minutes of each anomaly detected in {metric_column}."
            }
        except Exception as e:
            # Fall back to original implementation if new model fails
            print(f"Warning: New root cause analysis failed, falling back to original: {e}")
    
    # Original implementation as fallback
    if anomaly_col not in metrics_df.columns:
        raise ValueError(f"Anomaly column '{anomaly_col}' not found in metrics DataFrame")
    # Identify anomaly timestamps
    anomalies = metrics_df[metrics_df[anomaly_col]]
    results = []
    for ts in anomalies["timestamp"]:
        window_start = ts - pd.Timedelta(minutes=time_window_minutes)
        window_end = ts + pd.Timedelta(minutes=time_window_minutes)
        logs_in_window = logs_df[(logs_df["timestamp"] >= window_start) & (logs_df["timestamp"] <= window_end)]
        # Count error messages within the window
        error_counts = logs_in_window[logs_in_window["level"] == "ERROR"]["message"].value_counts().to_dict()
        results.append({
            "timestamp": ts,
            "metric_value": float(metrics_df.loc[metrics_df["timestamp"] == ts, metric_column].iloc[0]),
            "logs_analyzed": len(logs_in_window),
            "error_counts": error_counts,
        })
    return {
        "analysis": results,
        "description": (
            f"Analyzed logs within ±{time_window_minutes} minutes of each anomaly "
            f"detected in {metric_column}. Counted occurrences of different error messages."
        ),
    }


def ai_answer(
    question: str,
    metrics_df: pd.DataFrame,
    logs_df: pd.DataFrame,
    api_key: str = None,
    model: str = None,
) -> Dict[str, str]:
    """Generate AI-powered answers about system health using custom AI models.

    This function uses a custom AI model to analyze system metrics and logs
    to provide intelligent answers about system health. It prioritizes the
    custom AI model over OpenAI for better privacy and control.

    Parameters
    ----------
    question : str
        The natural language question asked by the user.
    metrics_df : DataFrame
        DataFrame containing system metrics.
    logs_df : DataFrame
        DataFrame containing system logs.
    api_key : str, optional
        OpenAI API key (used as fallback if custom AI is unavailable).
    model : str, optional
        Model specification (used for OpenAI fallback).

    Returns
    -------
    dict
        Dictionary with keys ``answer`` and ``reasoning``.
    """
    # Try custom AI model first
    if custom_ai_available:
        try:
            ai_model = get_ai_model()
            if ai_model.is_available():
                return ai_model.generate_answer(question, metrics_df, logs_df)
        except Exception as e:
            print(f"Custom AI model failed, falling back to OpenAI: {e}")
    
    # Fallback to OpenAI if custom AI is not available
    if openai is not None and api_key:
        return _openai_fallback(question, metrics_df, logs_df, api_key, model)
    
    # Final fallback
    return {
        "answer": "AI functionality is unavailable. Please check your custom AI model configuration or OpenAI API key.",
        "reasoning": "No AI model available for analysis.",
    }


def _openai_fallback(
    question: str,
    metrics_df: pd.DataFrame,
    logs_df: pd.DataFrame,
    api_key: str,
    model: str = "gpt-4o",
) -> Dict[str, str]:
    """OpenAI fallback implementation."""
    # Summarize metrics (mean and latest value)
    summary_stats = metrics_df.describe().loc[["mean", "std"]].round(2).to_dict()
    latest_metrics = metrics_df.tail(1).to_dict(orient="records")[0]
    # Get sample of last 5 log messages
    recent_logs = logs_df.tail(5).to_dict(orient="records")

    prompt = (
        "You are an AI assistant integrated into an observability dashboard."
        " Your task is to answer the user's question about the system's health"
        " based on the provided metrics and logs. Describe your reasoning"
        " transparently by explaining which metrics or log entries you used."
        "\n\n"
        f"Question: {question}\n"
        f"Metrics Summary (mean/std): {summary_stats}\n"
        f"Latest Metrics Snapshot: {latest_metrics}\n"
        f"Recent Logs: {recent_logs}\n"
        "Answer in a concise manner and include a 'Reasoning' section."
    )

    # Configure the OpenAI client
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=300,
            temperature=0.2,
        )
        content = response.choices[0].message["content"]
        # Attempt to parse the answer and reasoning if separated by heading
        if "Reasoning:" in content:
            answer_part, reasoning_part = content.split("Reasoning:", 1)
            answer = answer_part.strip()
            reasoning = reasoning_part.strip()
        else:
            answer = content.strip()
            reasoning = "Reasoning not explicitly provided by AI."
    except Exception as e:
        answer = "An error occurred when contacting the OpenAI API."
        reasoning = str(e)
    return {"answer": answer, "reasoning": reasoning}


# Keep the old function name for backward compatibility
def openai_answer(
    question: str,
    metrics_df: pd.DataFrame,
    logs_df: pd.DataFrame,
    api_key: str,
    model: str = "gpt-4o",
) -> Dict[str, str]:
    """Backward compatibility wrapper for openai_answer."""
    return ai_answer(question, metrics_df, logs_df, api_key, model)