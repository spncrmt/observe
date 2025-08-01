"""
generate_data.py
This script generates synthetic telemetry data and log data for the Observe AI dashboard.

The goal is to simulate metrics and logs similar to those from a production environment
so you can develop and test the dashboard locally without needing access to a real
monitoring system. The generated dataset includes:

1. **Metrics**: CPU usage, memory usage, and latency sampled at one‑minute intervals
   over a seven‑day period. A random noise pattern is applied to create variability,
   and occasional spikes are injected to simulate anomalies.
2. **Logs**: Text log entries with timestamps that loosely correlate with the
   metrics. Some log messages correspond to error events to help the AI identify
   potential root causes. Each log record includes a timestamp, a log level,
   and a message.

The script saves the metrics and logs to CSV files under the ``data/`` folder.

To run the script:

```bash
python observe_ai/scripts/generate_data.py
```

This will create two files: ``data/metrics.csv`` and ``data/logs.csv`` in the
project directory. The function ``generate_data()`` can also be imported and
used directly from within the Streamlit app if you prefer to generate data
programmatically.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_metrics(start_time: datetime, end_time: datetime) -> pd.DataFrame:
    """Generate synthetic metrics between start_time and end_time at one‑minute intervals.

    Parameters
    ----------
    start_time : datetime
        The starting timestamp for the metrics.
    end_time : datetime
        The ending timestamp for the metrics.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing timestamp, cpu_usage, memory_usage, and latency columns.
    """
    timestamps = pd.date_range(start=start_time, end=end_time, freq="1T")
    n = len(timestamps)

    # Base patterns for CPU, memory and latency
    cpu_base = np.sin(np.linspace(0, 4 * np.pi, n)) * 10 + 50  # base CPU around 50%
    mem_base = np.sin(np.linspace(0, 3 * np.pi, n)) * 5 + 60  # base memory around 60%
    latency_base = np.cos(np.linspace(0, 5 * np.pi, n)) * 20 + 100  # base latency around 100ms

    # Random noise
    noise_cpu = np.random.normal(0, 5, n)
    noise_mem = np.random.normal(0, 3, n)
    noise_latency = np.random.normal(0, 10, n)

    cpu_usage = np.clip(cpu_base + noise_cpu, 0, 100)
    memory_usage = np.clip(mem_base + noise_mem, 0, 100)
    latency = np.clip(latency_base + noise_latency, 0, None)

    metrics_df = pd.DataFrame({
        "timestamp": timestamps,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "latency_ms": latency,
    })

    # Inject spikes to simulate anomalies
    for _ in range(5):
        idx = np.random.randint(0, n - 30)
        metrics_df.loc[idx: idx + 10, "cpu_usage"] += np.random.uniform(20, 40)
        metrics_df.loc[idx: idx + 10, "memory_usage"] += np.random.uniform(10, 20)
        metrics_df.loc[idx: idx + 10, "latency_ms"] += np.random.uniform(50, 100)

    return metrics_df


def generate_logs(start_time: datetime, end_time: datetime) -> pd.DataFrame:
    """Generate synthetic log entries between start_time and end_time.

    The logs include info, warning, and error messages. Error logs are more likely
    around times when anomalies are injected in the metrics.

    Parameters
    ----------
    start_time : datetime
        Start of the logging period.
    end_time : datetime
        End of the logging period.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing timestamp, level, and message columns.
    """
    # Create a base list of possible log messages
    info_messages = [
        "Scheduled job completed successfully.",
        "User logged in.",
        "Background worker processed request.",
        "Heartbeat check passed.",
        "Cache refreshed successfully.",
    ]
    warn_messages = [
        "High memory usage detected.",
        "Slow query detected.",
        "API response time above threshold.",
    ]
    error_messages = [
        "Database connection timeout.",
        "Service unavailable: 503 error.",
        "Out of memory error.",
        "Disk space critically low.",
        "Unhandled exception in worker thread.",
    ]

    timestamps = []
    levels = []
    messages = []

    current_time = start_time
    while current_time <= end_time:
        # Determine the number of logs per minute (0–3 logs)
        num_logs = np.random.poisson(1)
        for _ in range(num_logs):
            # Choose a log level based on probabilities
            level = np.random.choice(["INFO", "WARN", "ERROR"], p=[0.8, 0.15, 0.05])
            if level == "INFO":
                msg = np.random.choice(info_messages)
            elif level == "WARN":
                msg = np.random.choice(warn_messages)
            else:
                msg = np.random.choice(error_messages)
            timestamps.append(current_time)
            levels.append(level)
            messages.append(msg)
        current_time += timedelta(minutes=1)

    logs_df = pd.DataFrame({
        "timestamp": timestamps,
        "level": levels,
        "message": messages,
    })
    return logs_df


def save_data(metrics_df: pd.DataFrame, logs_df: pd.DataFrame, data_dir: str) -> None:
    """Save metrics and logs DataFrames to CSV files in the specified directory."""
    os.makedirs(data_dir, exist_ok=True)
    metrics_path = os.path.join(data_dir, "metrics.csv")
    logs_path = os.path.join(data_dir, "logs.csv")
    metrics_df.to_csv(metrics_path, index=False)
    logs_df.to_csv(logs_path, index=False)


def generate_data(data_dir: str = None) -> None:
    """Generate metrics and logs and save them to the data directory.

    If `data_dir` is None, the script will save into ``../data`` relative to
    this script's location. Use this function in other modules to generate
    synthetic data at runtime.
    """
    if data_dir is None:
        # Default data directory is observe_ai/data relative to this file
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    start = datetime.now() - timedelta(days=7)
    end = datetime.now()
    metrics_df = generate_metrics(start, end)
    logs_df = generate_logs(start, end)
    save_data(metrics_df, logs_df, data_dir)
    print(f"Generated metrics and logs saved to {data_dir}")


if __name__ == "__main__":
    generate_data()