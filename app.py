"""
Observe AI Dashboard
=====================

This Streamlit application implements an AI‑enhanced observability dashboard
inspired by professional tools like Grafana. It demonstrates how a solo
developer can integrate authentication, metrics visualization, anomaly
detection, root cause analysis, natural language question answering, and
user feedback loops into a cohesive product. The design follows Greg
Nudelman's UX for AI principles by framing AI as a helpful assistant, making
its reasoning transparent, and giving the user control over the experience.

Running the app
---------------

Install the dependencies listed in ``requirements.txt`` and then run:

```bash
streamlit run observe_ai/app.py
```

On first launch, the app will generate synthetic data if no data files are
present. A default user ``admin/admin`` is created automatically. Use this
account to log in, then navigate the dashboard, input your OpenAI API key, and
start exploring the AI assistant features. You can register additional users
via the registration form.
"""

import os
import sys
import json
import time
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any

# Ensure internal modules are importable as local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.auth import UserAuth
from utils.ai_assistant import detect_anomalies, root_cause_analysis, ai_answer
from scripts.generate_data import generate_data


# Constants
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
METRICS_FILE = os.path.join(DATA_DIR, "metrics.csv")
LOGS_FILE = os.path.join(DATA_DIR, "logs.csv")
REAL_METRICS_FILE = os.path.join(DATA_DIR, "real_metrics.csv")
REAL_LOGS_FILE = os.path.join(DATA_DIR, "real_logs.csv")
FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "feedback.json")


def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load metrics and logs from CSV. Generate data if files are missing."""
    # Try to load real data first
    try:
        if os.path.exists(REAL_METRICS_FILE) and os.path.getsize(REAL_METRICS_FILE) > 0:
            metrics_df = pd.read_csv(REAL_METRICS_FILE, parse_dates=["timestamp"])
            logs_df = pd.read_csv(REAL_LOGS_FILE, parse_dates=["timestamp"]) if os.path.exists(REAL_LOGS_FILE) else pd.DataFrame()
            return metrics_df, logs_df
    except Exception as e:
        st.warning(f"Could not load real data: {e}")
    
    # Fall back to synthetic data
    if not os.path.exists(METRICS_FILE) or not os.path.exists(LOGS_FILE):
        generate_data(DATA_DIR)
    try:
        metrics_df = pd.read_csv(METRICS_FILE, parse_dates=["timestamp"])
    except Exception:
        metrics_df = pd.DataFrame()
    try:
        logs_df = pd.read_csv(LOGS_FILE, parse_dates=["timestamp"])
    except Exception:
        logs_df = pd.DataFrame()
    return metrics_df, logs_df


def save_feedback(feedback_entry: Dict[str, Any]) -> None:
    """Append a feedback entry to the feedback file (JSON list)."""
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(feedback_entry)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def start_monitoring(interval: int = 60):
    """Start the system monitoring in background."""
    try:
        # Start the monitoring script in background
        cmd = [
            sys.executable, 
            "scripts/system_monitor.py", 
            "--local-only", 
            "--interval", 
            str(interval)
        ]
        
        # Use subprocess.Popen to run in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return process
    except Exception as e:
        st.error(f"Failed to start monitoring: {e}")
        return None


def stop_monitoring(process):
    """Stop the monitoring process."""
    if process:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        return True
    return False


def get_live_metrics() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get the latest metrics and logs for real-time display."""
    try:
        # Read real metrics if available
        if os.path.exists(REAL_METRICS_FILE) and os.path.getsize(REAL_METRICS_FILE) > 0:
            metrics_df = pd.read_csv(REAL_METRICS_FILE, parse_dates=["timestamp"])
            # Get only recent data (last 2 hours)
            cutoff_time = datetime.now() - timedelta(hours=2)
            metrics_df = metrics_df[metrics_df['timestamp'] >= cutoff_time]
        else:
            metrics_df = pd.DataFrame()
        
        # Read real logs if available
        if os.path.exists(REAL_LOGS_FILE) and os.path.getsize(REAL_LOGS_FILE) > 0:
            logs_df = pd.read_csv(REAL_LOGS_FILE, parse_dates=["timestamp"])
            # Get only recent logs (last 2 hours)
            cutoff_time = datetime.now() - timedelta(hours=2)
            logs_df = logs_df[logs_df['timestamp'] >= cutoff_time]
        else:
            logs_df = pd.DataFrame()
        
        return metrics_df, logs_df
    except Exception as e:
        st.error(f"Error loading live metrics: {e}")
        return pd.DataFrame(), pd.DataFrame()


def create_real_time_chart(metrics_df: pd.DataFrame, metric_choice: str):
    """Create a real-time chart with live data."""
    if metrics_df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Add the main metric line
    fig.add_trace(go.Scatter(
        x=metrics_df['timestamp'],
        y=metrics_df[metric_choice],
        mode='lines+markers',
        name=metric_choice.replace('_', ' ').title(),
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    
    # Add anomaly markers if available
    if 'anomaly' in metrics_df.columns:
        anomalies = metrics_df[metrics_df['anomaly']]
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies['timestamp'],
                y=anomalies[metric_choice],
                mode='markers',
                name='Anomaly',
                marker=dict(color='red', size=8, symbol='x'),
                showlegend=True
            ))
    
    # Update layout
    fig.update_layout(
        title=f"Live {metric_choice.replace('_', ' ').title()} Monitoring",
        xaxis_title="Time",
        yaxis_title=metric_choice.replace('_', ' ').title(),
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig


def main():
    st.set_page_config(page_title="Observe AI Dashboard", layout="wide")
    st.title("Observe AI Dashboard")

    # Initialize authentication system and ensure default user
    auth = UserAuth()
    auth.ensure_default_user()

    # Initialize session state variables
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("username", "")
    st.session_state.setdefault("api_key", "")
    st.session_state.setdefault("monitoring_active", False)
    st.session_state.setdefault("monitoring_process", None)
    st.session_state.setdefault("last_refresh", time.time())

    # Login/Registration interface
    if not st.session_state.logged_in:
        st.sidebar.header("User Authentication")
        auth_choice = st.sidebar.radio("Action", ["Login", "Register"])
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if auth_choice == "Login":
            if st.sidebar.button("Login"):
                if auth.authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.sidebar.success(f"Logged in as {username}")
                else:
                    st.sidebar.error("Invalid username or password.")
        else:
            # Registration
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            if st.sidebar.button("Register"):
                if password != confirm_password:
                    st.sidebar.error("Passwords do not match.")
                elif not username:
                    st.sidebar.error("Username cannot be empty.")
                else:
                    success = auth.register_user(username, password)
                    if success:
                        st.sidebar.success("Registration successful. Please log in.")
                    else:
                        st.sidebar.error("User already exists.")
        return

    # Logged-in user interface
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Real-time Monitoring Controls
    st.sidebar.header("🖥️ Real-time Monitoring")
    
    # Monitoring status
    if st.session_state.monitoring_active:
        st.sidebar.success("✅ Monitoring Active")
        if st.sidebar.button("🛑 Stop Monitoring"):
            if stop_monitoring(st.session_state.monitoring_process):
                st.session_state.monitoring_active = False
                st.session_state.monitoring_process = None
                st.success("Monitoring stopped!")
                st.rerun()
    else:
        st.sidebar.info("⏸️ Monitoring Inactive")
        
        # Monitoring configuration
        interval = st.sidebar.slider("Collection Interval (seconds)", 30, 300, 60)
        
        if st.sidebar.button("▶️ Start Monitoring"):
            process = start_monitoring(interval)
            if process:
                st.session_state.monitoring_active = True
                st.session_state.monitoring_process = process
                st.success(f"Monitoring started! Collecting data every {interval} seconds.")
                st.rerun()
            else:
                st.error("Failed to start monitoring.")

    # AI Model Configuration
    st.sidebar.header("AI Model Configuration")
    
    # Model selection
    model_choice = st.sidebar.selectbox(
        "AI Model",
        ["Custom AI Model", "OpenAI (Fallback)"],
        help="Choose your preferred AI model for explanations."
    )
    
    if model_choice == "OpenAI (Fallback)":
        api_key_input = st.sidebar.text_input(
            "OpenAI API Key (Optional)",
            type="password",
            help="Only needed if using OpenAI fallback.",
        )
        if api_key_input:
            st.session_state.api_key = api_key_input
        if st.session_state.api_key:
            st.sidebar.success("OpenAI API key set")
        else:
            st.sidebar.info("Using custom AI model (no API key needed)")
    else:
        st.sidebar.success("Using custom AI model")
        st.session_state.api_key = ""

    # Auto-refresh for real-time data
    if st.session_state.monitoring_active:
        # Refresh every 10 seconds when monitoring is active
        if time.time() - st.session_state.last_refresh > 10:
            st.session_state.last_refresh = time.time()
            st.rerun()

    # Load data (real-time if monitoring, otherwise historical)
    if st.session_state.monitoring_active:
        metrics_df, logs_df = get_live_metrics()
        data_source = "🔄 Live Data"
    else:
        metrics_df, logs_df = load_data()
        data_source = "📊 Historical Data"

    # Display data source indicator
    st.info(f"{data_source} - {'Monitoring Active' if st.session_state.monitoring_active else 'Historical View'}")

    # Detect anomalies for CPU usage using enhanced detection model
    if not metrics_df.empty:
        metrics_analyzed = detect_anomalies(metrics_df, column="cpu_usage", window=60, z_threshold=3.5)
    else:
        metrics_analyzed = metrics_df

    # Display metrics chart
    st.subheader("System Metrics")
    metric_choice = st.selectbox("Select metric to view", ["cpu_usage", "memory_usage", "latency_ms"])
    
    if not metrics_analyzed.empty:
        if st.session_state.monitoring_active:
            # Real-time chart
            fig = create_real_time_chart(metrics_analyzed, metric_choice)
        else:
            # Historical chart
            chart_data = metrics_analyzed.copy()
            fig = px.line(
                chart_data,
                x="timestamp",
                y=metric_choice,
                title=f"{metric_choice.replace('_', ' ').title()} over Time",
            )
            # Highlight anomalies on the plot
            if "anomaly" in chart_data.columns:
                anomalies = chart_data[chart_data["anomaly"]]
                fig.add_scatter(
                    x=anomalies["timestamp"],
                    y=anomalies[metric_choice],
                    mode="markers",
                    marker=dict(color="red", size=6),
                    name="Anomaly",
                )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No metrics data available. Start monitoring to see live data.")

    # Show log table
    with st.expander("View Logs"):
        if not logs_df.empty:
            st.dataframe(logs_df.tail(100))
        else:
            st.info("No logs available. Start monitoring to see live logs.")

    # System Status Dashboard
    if st.session_state.monitoring_active and not metrics_df.empty:
        st.subheader("📊 Live System Status")
        
        # Get latest metrics
        latest = metrics_df.iloc[-1] if not metrics_df.empty else None
        
        if latest is not None:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "CPU Usage", 
                    f"{latest['cpu_usage']:.1f}%",
                    delta=f"{latest['cpu_usage'] - metrics_df['cpu_usage'].mean():.1f}%"
                )
            
            with col2:
                st.metric(
                    "Memory Usage", 
                    f"{latest['memory_usage']:.1f}%",
                    delta=f"{latest['memory_usage'] - metrics_df['memory_usage'].mean():.1f}%"
                )
            
            with col3:
                if 'latency_ms' in latest:
                    st.metric(
                        "Latency", 
                        f"{latest['latency_ms']:.1f}ms",
                        delta=f"{latest['latency_ms'] - metrics_df['latency_ms'].mean():.1f}ms"
                    )
                else:
                    st.metric("Data Points", len(metrics_df))
            
            with col4:
                st.metric(
                    "Monitoring Time", 
                    f"{len(metrics_df)} samples",
                    delta=f"Every {interval}s"
                )

    # Natural language query input
    st.subheader("Ask the AI about your system")
    query = st.text_input(
        "Enter a question about your system's health (e.g., 'Why is CPU usage spiking?')",
        key="query_input",
    )
    if st.button("Ask"):
        if not query.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Querying AI..."):
                ai_result = ai_answer(
                    question=query.strip(),
                    metrics_df=metrics_df,
                    logs_df=logs_df,
                    api_key=st.session_state.api_key,
                )
            st.write("**AI Answer:**")
            st.write(ai_result.get("answer", "No answer available."))
            st.write("**AI Reasoning:**")
            st.write(ai_result.get("reasoning", "No reasoning available."))

            # Root cause analysis
            if not metrics_analyzed.empty:
                rca = root_cause_analysis(metrics_analyzed, logs_df)
                st.subheader("Root Cause Analysis")
                for entry in rca["analysis"][:5]:
                    st.markdown(
                        f"**Anomaly at {entry['timestamp']}**\n\n"
                        f"Metric value: {entry['metric_value']:.2f}\n\n"
                        f"Logs analyzed: {entry['logs_analyzed']}\n\n"
                        f"Top error messages: {entry['error_counts']}"
                    )
                st.caption(rca["description"])

            # Feedback interface
            st.subheader("Was this helpful?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Helpful 👍"):
                    save_feedback({
                        "timestamp": datetime.now(),
                        "user": st.session_state.username,
                        "question": query.strip(),
                        "ai_answer": ai_result.get("answer"),
                        "helpful": True,
                    })
                    st.success("Thanks for your feedback!")
            with col2:
                if st.button("Not Helpful 👎"):
                    save_feedback({
                        "timestamp": datetime.now(),
                        "user": st.session_state.username,
                        "question": query.strip(),
                        "ai_answer": ai_result.get("answer"),
                        "helpful": False,
                    })
                    st.success("Thanks for your feedback! We'll use it to improve.")

    st.markdown("---")
    st.caption(
        "**Note:** This is a demo observability dashboard with synthetic data. "
        "AI answers may be approximate and are provided for educational purposes only."
    )


if __name__ == "__main__":
    main()