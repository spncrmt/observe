"""
Production-Grade Anomaly Detection and Root Cause Analysis Module
================================================================

This module provides advanced anomaly detection and root cause analysis
capabilities for observability dashboards. It uses statistical methods
to detect anomalies in system metrics and correlates them with log data
to provide actionable insights.

Key Features:
- Rolling window anomaly detection using z-score analysis
- Multi-metric correlation analysis
- Log correlation with ±5 minute windows
- Error pattern recognition and classification
- Production-ready with comprehensive error handling
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import Counter
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _validate_dataframes(metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> None:
    """
    Validate input dataframes for required columns and data types.
    
    Args:
        metrics_df: DataFrame with timestamp, cpu_usage, memory_usage, latency_ms
        logs_df: DataFrame with timestamp, level, message
        
    Raises:
        ValueError: If required columns are missing or data types are incorrect
    """
    required_metrics_cols = ['timestamp', 'cpu_usage', 'memory_usage', 'latency_ms']
    required_logs_cols = ['timestamp', 'level', 'message']
    
    # Check metrics dataframe
    missing_metrics_cols = [col for col in required_metrics_cols if col not in metrics_df.columns]
    if missing_metrics_cols:
        raise ValueError(f"Missing required columns in metrics_df: {missing_metrics_cols}")
    
    # Check logs dataframe
    missing_logs_cols = [col for col in required_logs_cols if col not in logs_df.columns]
    if missing_logs_cols:
        raise ValueError(f"Missing required columns in logs_df: {missing_logs_cols}")
    
    # Validate timestamp columns are datetime
    if not pd.api.types.is_datetime64_any_dtype(metrics_df['timestamp']):
        raise ValueError("metrics_df['timestamp'] must be datetime type")
    
    if not pd.api.types.is_datetime64_any_dtype(logs_df['timestamp']):
        raise ValueError("logs_df['timestamp'] must be datetime type")


def _calculate_rolling_statistics(
    df: pd.DataFrame, 
    column: str, 
    window: int = 60,
    min_periods: int = 30
) -> pd.DataFrame:
    """
    Calculate rolling mean and standard deviation for anomaly detection.
    
    Args:
        df: DataFrame with the target column
        column: Column name to analyze
        window: Rolling window size in periods
        min_periods: Minimum periods required for calculation
        
    Returns:
        DataFrame with rolling statistics added
    """
    df = df.copy()
    
    # Calculate rolling statistics
    df[f'{column}_rolling_mean'] = df[column].rolling(
        window=window, 
        min_periods=min_periods,
        center=True
    ).mean()
    
    df[f'{column}_rolling_std'] = df[column].rolling(
        window=window, 
        min_periods=min_periods,
        center=True
    ).std()
    
    # Handle NaN values by forward filling
    df[f'{column}_rolling_mean'] = df[f'{column}_rolling_mean'].ffill()
    df[f'{column}_rolling_std'] = df[f'{column}_rolling_std'].ffill()
    
    return df


def _detect_anomalies_zscore(
    df: pd.DataFrame, 
    column: str, 
    z_threshold: float = 3.0
) -> pd.DataFrame:
    """
    Detect anomalies using z-score method with rolling statistics.
    
    Args:
        df: DataFrame with rolling statistics
        column: Column name to analyze
        z_threshold: Z-score threshold for anomaly detection
        
    Returns:
        DataFrame with anomaly column added
    """
    df = df.copy()
    
    # Calculate z-score
    rolling_mean_col = f'{column}_rolling_mean'
    rolling_std_col = f'{column}_rolling_std'
    
    # Avoid division by zero
    df[f'{column}_zscore'] = np.where(
        df[rolling_std_col] > 0,
        (df[column] - df[rolling_mean_col]) / df[rolling_std_col],
        0
    )
    
    # Detect anomalies
    df['anomaly'] = abs(df[f'{column}_zscore']) > z_threshold
    
    return df


def _correlate_log_errors(
    anomaly_timestamps: pd.Series, 
    logs_df: pd.DataFrame,
    time_window_minutes: int = 5
) -> Dict[datetime, List[str]]:
    """
    Correlate anomaly timestamps with error logs within a time window.
    
    Args:
        anomaly_timestamps: Series of anomaly timestamps
        logs_df: DataFrame with log entries
        time_window_minutes: Time window for correlation (±minutes)
        
    Returns:
        Dictionary mapping anomaly timestamps to correlated error messages
    """
    correlation_map = {}
    
    for anomaly_time in anomaly_timestamps:
        # Define time window
        start_time = anomaly_time - timedelta(minutes=time_window_minutes)
        end_time = anomaly_time + timedelta(minutes=time_window_minutes)
        
        # Filter logs within time window
        window_logs = logs_df[
            (logs_df['timestamp'] >= start_time) & 
            (logs_df['timestamp'] <= end_time)
        ]
        
        # Extract error and warning messages
        error_messages = window_logs[
            window_logs['level'].isin(['ERROR', 'WARN'])
        ]['message'].tolist()
        
        correlation_map[anomaly_time] = error_messages
    
    return correlation_map


def _classify_error_patterns(error_messages: List[str]) -> Dict[str, int]:
    """
    Classify and count error patterns from log messages.
    
    Args:
        error_messages: List of error messages
        
    Returns:
        Dictionary of error patterns and their counts
    """
    if not error_messages:
        return {}
    
    # Define common error patterns
    error_patterns = {
        'Out of memory': r'out of memory|memory error|memory exhaustion',
        'Database timeout': r'database.*timeout|connection.*timeout|db.*timeout',
        'Disk space': r'disk.*space|disk.*full|storage.*full',
        'API timeout': r'api.*timeout|response.*time|slow.*query',
        'High memory usage': r'high.*memory|memory.*usage',
        'Service crash': r'service.*crash|application.*crash|process.*died'
    }
    
    pattern_counts = {}
    
    for pattern_name, regex_pattern in error_patterns.items():
        count = sum(
            1 for msg in error_messages 
            if re.search(regex_pattern, msg.lower())
        )
        if count > 0:
            pattern_counts[pattern_name] = count
    
    # Add uncategorized errors
    categorized_messages = []
    for pattern in error_patterns.values():
        categorized_messages.extend([
            msg for msg in error_messages 
            if re.search(pattern, msg.lower())
        ])
    
    uncategorized = [
        msg for msg in error_messages 
        if msg not in categorized_messages
    ]
    
    if uncategorized:
        pattern_counts['Other errors'] = len(uncategorized)
    
    return pattern_counts


def detect_anomalies_custom(
    metrics_df: pd.DataFrame, 
    logs_df: pd.DataFrame,
    target_column: str = 'cpu_usage',
    window: int = 60,
    z_threshold: float = 3.0,
    min_periods: int = 30
) -> pd.DataFrame:
    """
    Detect anomalies in system metrics using rolling statistics and z-score analysis.
    
    This function implements a production-grade anomaly detection algorithm that:
    1. Calculates rolling mean and standard deviation for the target metric
    2. Computes z-scores to identify statistical outliers
    3. Flags timestamps with correlated error logs
    4. Provides comprehensive anomaly analysis
    
    Args:
        metrics_df: DataFrame with system metrics (timestamp, cpu_usage, memory_usage, latency_ms)
        logs_df: DataFrame with system logs (timestamp, level, message)
        target_column: Column name to analyze for anomalies (default: 'cpu_usage')
        window: Rolling window size for statistics calculation (default: 60)
        z_threshold: Z-score threshold for anomaly detection (default: 3.0)
        min_periods: Minimum periods required for rolling calculations (default: 30)
        
    Returns:
        DataFrame with additional columns:
        - anomaly: Boolean indicating anomaly detection
        - {target_column}_rolling_mean: Rolling mean of the target metric
        - {target_column}_rolling_std: Rolling standard deviation
        - {target_column}_zscore: Z-score value
        - correlated_errors: List of error messages within ±5 minutes
        
    Raises:
        ValueError: If required columns are missing or data types are incorrect
        Exception: For other processing errors
    """
    try:
        # Validate input dataframes
        _validate_dataframes(metrics_df, logs_df)
        
        # Ensure data is sorted by timestamp
        metrics_df = metrics_df.sort_values('timestamp').reset_index(drop=True)
        logs_df = logs_df.sort_values('timestamp').reset_index(drop=True)
        
        # Calculate rolling statistics
        result_df = _calculate_rolling_statistics(
            metrics_df, 
            target_column, 
            window, 
            min_periods
        )
        
        # Detect anomalies using z-score
        result_df = _detect_anomalies_zscore(result_df, target_column, z_threshold)
        
        # Correlate with error logs
        anomaly_timestamps = result_df[result_df['anomaly']]['timestamp']
        error_correlation = _correlate_log_errors(anomaly_timestamps, logs_df)
        
        # Add correlated errors to the dataframe
        result_df['correlated_errors'] = result_df['timestamp'].map(error_correlation)
        result_df['correlated_errors'] = result_df['correlated_errors'].fillna('[]').apply(lambda x: x if x != '[]' else [])
        
        logger.info(f"Anomaly detection completed: {result_df['anomaly'].sum()} anomalies detected")
        
        return result_df
        
    except Exception as e:
        logger.error(f"Error in anomaly detection: {str(e)}")
        raise


def explain_root_cause(
    metrics_df: pd.DataFrame, 
    logs_df: pd.DataFrame, 
    anomalies_df: pd.DataFrame,
    time_window_minutes: int = 5,
    max_analysis_count: int = 10
) -> List[Dict[str, Any]]:
    """
    Perform root cause analysis for detected anomalies.
    
    This function analyzes each anomaly to identify potential root causes by:
    1. Examining system metrics around the anomaly time
    2. Analyzing log patterns within the time window
    3. Correlating multiple metrics to identify patterns
    4. Providing human-readable explanations
    
    Args:
        metrics_df: Original metrics DataFrame
        logs_df: Logs DataFrame
        anomalies_df: DataFrame with anomaly detection results
        time_window_minutes: Time window for analysis (±minutes, default: 5)
        max_analysis_count: Maximum number of anomalies to analyze (default: 10)
        
    Returns:
        List of dictionaries containing root cause analysis for each anomaly:
        {
            "timestamp": datetime,
            "metric_value": float,
            "logs_analyzed": int,
            "error_counts": Dict[str, int],
            "explanation": str,
            "severity": str,
            "recommended_actions": List[str]
        }
    """
    try:
        # Get anomaly timestamps
        anomaly_times = anomalies_df[anomalies_df['anomaly']]['timestamp'].head(max_analysis_count)
        
        analysis_results = []
        
        for anomaly_time in anomaly_times:
            # Define analysis window
            start_time = anomaly_time - timedelta(minutes=time_window_minutes)
            end_time = anomaly_time + timedelta(minutes=time_window_minutes)
            
            # Get metrics in the window
            window_metrics = metrics_df[
                (metrics_df['timestamp'] >= start_time) & 
                (metrics_df['timestamp'] <= end_time)
            ]
            
            # Get logs in the window
            window_logs = logs_df[
                (logs_df['timestamp'] >= start_time) & 
                (logs_df['timestamp'] <= end_time)
            ]
            
            # Get the specific anomaly metric value
            anomaly_row = anomalies_df[anomalies_df['timestamp'] == anomaly_time]
            metric_value = anomaly_row.iloc[0]['cpu_usage'] if 'cpu_usage' in anomaly_row.columns else 0
            
            # Analyze error patterns
            error_logs = window_logs[window_logs['level'].isin(['ERROR', 'WARN'])]
            error_counts = _classify_error_patterns(error_logs['message'].tolist())
            
            # Generate explanation
            explanation = _generate_root_cause_explanation(
                anomaly_time, 
                metric_value, 
                error_counts, 
                window_metrics
            )
            
            # Determine severity
            severity = _determine_severity(metric_value, error_counts)
            
            # Generate recommended actions
            recommended_actions = _generate_recommended_actions(error_counts, severity)
            
            analysis_result = {
                "timestamp": anomaly_time,
                "metric_value": metric_value,
                "logs_analyzed": len(window_logs),
                "error_counts": error_counts,
                "explanation": explanation,
                "severity": severity,
                "recommended_actions": recommended_actions
            }
            
            analysis_results.append(analysis_result)
        
        logger.info(f"Root cause analysis completed: {len(analysis_results)} anomalies analyzed")
        return analysis_results
        
    except Exception as e:
        logger.error(f"Error in root cause analysis: {str(e)}")
        raise


def _generate_root_cause_explanation(
    timestamp: datetime,
    metric_value: float,
    error_counts: Dict[str, int],
    window_metrics: pd.DataFrame
) -> str:
    """
    Generate human-readable explanation for root cause analysis.
    
    Args:
        timestamp: Anomaly timestamp
        metric_value: Value of the anomalous metric
        error_counts: Dictionary of error patterns and counts
        window_metrics: Metrics data in the analysis window
        
    Returns:
        Human-readable explanation string
    """
    explanations = []
    
    # Base explanation
    explanations.append(f"Anomaly detected at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    explanations.append(f"CPU usage: {metric_value:.1f}%")
    
    # Add error context
    if error_counts:
        top_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        error_descriptions = [f"{error} ({count} occurrences)" for error, count in top_errors]
        explanations.append(f"Correlated errors: {', '.join(error_descriptions)}")
    
    # Add metric context
    if not window_metrics.empty:
        avg_cpu = window_metrics['cpu_usage'].mean()
        avg_memory = window_metrics['memory_usage'].mean()
        explanations.append(f"Window averages - CPU: {avg_cpu:.1f}%, Memory: {avg_memory:.1f}%")
    
    # Determine likely cause
    if 'Out of memory' in error_counts:
        explanations.append("Likely cause: Memory exhaustion leading to system instability")
    elif 'Database timeout' in error_counts:
        explanations.append("Likely cause: Database performance issues affecting system response")
    elif 'Disk space' in error_counts:
        explanations.append("Likely cause: Storage constraints impacting system performance")
    elif 'API timeout' in error_counts:
        explanations.append("Likely cause: External service dependencies causing delays")
    else:
        explanations.append("Likely cause: System resource contention or unknown external factors")
    
    return " ".join(explanations)


def _determine_severity(metric_value: float, error_counts: Dict[str, int]) -> str:
    """
    Determine severity level based on metric value and error patterns.
    
    Args:
        metric_value: Value of the anomalous metric
        error_counts: Dictionary of error patterns and counts
        
    Returns:
        Severity level: 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    """
    # Base severity on metric value
    if metric_value >= 95:
        base_severity = 'CRITICAL'
    elif metric_value >= 85:
        base_severity = 'HIGH'
    elif metric_value >= 75:
        base_severity = 'MEDIUM'
    else:
        base_severity = 'LOW'
    
    # Adjust based on error patterns
    critical_errors = ['Out of memory', 'Service crash', 'Disk space']
    high_errors = ['Database timeout', 'API timeout']
    
    for error in critical_errors:
        if error in error_counts and error_counts[error] > 0:
            return 'CRITICAL'
    
    for error in high_errors:
        if error in error_counts and error_counts[error] > 2:
            return 'HIGH'
    
    return base_severity


def _generate_recommended_actions(error_counts: Dict[str, int], severity: str) -> List[str]:
    """
    Generate recommended actions based on error patterns and severity.
    
    Args:
        error_counts: Dictionary of error patterns and counts
        severity: Severity level
        
    Returns:
        List of recommended actions
    """
    actions = []
    
    # Immediate actions based on severity
    if severity == 'CRITICAL':
        actions.append("Immediate system restart or failover required")
        actions.append("Scale up resources immediately")
    elif severity == 'HIGH':
        actions.append("Investigate and resolve within 30 minutes")
        actions.append("Consider scaling resources")
    
    # Specific actions based on error patterns
    if 'Out of memory' in error_counts:
        actions.append("Increase memory allocation or optimize memory usage")
        actions.append("Check for memory leaks in application code")
    
    if 'Database timeout' in error_counts:
        actions.append("Optimize database queries or increase connection pool")
        actions.append("Check database server performance")
    
    if 'Disk space' in error_counts:
        actions.append("Clean up disk space or increase storage")
        actions.append("Implement log rotation and cleanup")
    
    if 'API timeout' in error_counts:
        actions.append("Check external service health and response times")
        actions.append("Implement circuit breaker pattern")
    
    # General monitoring actions
    actions.append("Set up alerts for similar patterns")
    actions.append("Review system logs for additional context")
    
    return actions


def get_anomaly_summary(anomalies_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a summary of detected anomalies for dashboard display.
    
    Args:
        anomalies_df: DataFrame with anomaly detection results
        
    Returns:
        Dictionary with anomaly summary statistics
    """
    if anomalies_df.empty or 'anomaly' not in anomalies_df.columns:
        return {
            "total_anomalies": 0,
            "anomaly_rate": 0.0,
            "severity_distribution": {},
            "time_range": None
        }
    
    anomaly_data = anomalies_df[anomalies_df['anomaly']]
    
    # Calculate basic statistics
    total_anomalies = len(anomaly_data)
    total_records = len(anomalies_df)
    anomaly_rate = (total_anomalies / total_records) * 100 if total_records > 0 else 0
    
    # Time range
    time_range = None
    if not anomaly_data.empty and 'timestamp' in anomaly_data.columns:
        time_range = {
            "start": anomaly_data['timestamp'].min(),
            "end": anomaly_data['timestamp'].max()
        }
    
    # Severity distribution (if available)
    severity_distribution = {}
    if 'severity' in anomaly_data.columns:
        severity_counts = anomaly_data['severity'].value_counts()
        severity_distribution = severity_counts.to_dict()
    
    return {
        "total_anomalies": total_anomalies,
        "anomaly_rate": anomaly_rate,
        "severity_distribution": severity_distribution,
        "time_range": time_range
    } 