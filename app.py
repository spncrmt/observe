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

# Enable session state persistence
st.set_page_config(
    page_title="Observe AI Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.auth import UserAuth
from utils.ai_assistant import detect_anomalies, root_cause_analysis, ai_answer
from utils.session_manager import SessionManager
from utils.metric_collectors import MetricCollectorManager
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


def start_monitoring(interval: int = 60, selected_metrics: list = None):
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
        
        # Add selected metrics if provided
        if selected_metrics:
            cmd.extend(["--metrics"] + selected_metrics)
        
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
            try:
                metrics_df = pd.read_csv(REAL_METRICS_FILE, parse_dates=["timestamp"])
                # Get only recent data (last 2 hours)
                cutoff_time = datetime.now() - timedelta(hours=2)
                metrics_df = metrics_df[metrics_df['timestamp'] >= cutoff_time]
            except Exception as e:
                st.warning(f"Error reading metrics file: {e}")
                metrics_df = pd.DataFrame()
        else:
            metrics_df = pd.DataFrame()
        
        # Read real logs if available
        if os.path.exists(REAL_LOGS_FILE) and os.path.getsize(REAL_LOGS_FILE) > 0:
            try:
                logs_df = pd.read_csv(REAL_LOGS_FILE, parse_dates=["timestamp"])
                # Get only recent logs (last 2 hours)
                cutoff_time = datetime.now() - timedelta(hours=2)
                logs_df = logs_df[logs_df['timestamp'] >= cutoff_time]
            except Exception as e:
                st.warning(f"Error reading logs file: {e}")
                logs_df = pd.DataFrame()
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
    st.title("Observe AI Dashboard")

    # Initialize authentication system and ensure default user
    auth = UserAuth()
    auth.ensure_default_user()
    
    # Initialize session manager for persistent login
    session_manager = SessionManager()

    # Initialize session state variables with persistence
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = session_manager.is_logged_in()
    if "username" not in st.session_state:
        st.session_state.username = session_manager.get_username()
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "monitoring_active" not in st.session_state:
        st.session_state.monitoring_active = False
    if "monitoring_process" not in st.session_state:
        st.session_state.monitoring_process = None
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    if "monitoring_interval" not in st.session_state:
        st.session_state.monitoring_interval = 60
    if "selected_metrics" not in st.session_state:
        st.session_state.selected_metrics = ["cpu_usage", "memory_usage"]
    
    # Restore monitoring state from persistent storage
    persistent_active, persistent_interval = session_manager.get_monitoring_state()
    if persistent_active and not st.session_state.monitoring_active:
        st.session_state.monitoring_active = persistent_active
        st.session_state.monitoring_interval = persistent_interval
    
    # Check if monitoring should be active (persistent monitoring)
    if st.session_state.monitoring_active:
        # Verify monitoring process is still running
        if st.session_state.monitoring_process:
            try:
                # Check if process is still alive
                if st.session_state.monitoring_process.poll() is not None:
                    # Process has died, restart it
                    st.session_state.monitoring_process = start_monitoring(st.session_state.monitoring_interval)
                    if not st.session_state.monitoring_process:
                        st.session_state.monitoring_active = False
                        session_manager.save_monitoring_state(False, st.session_state.monitoring_interval)
            except:
                # Process check failed, restart monitoring
                st.session_state.monitoring_process = start_monitoring(st.session_state.monitoring_interval)
                if not st.session_state.monitoring_process:
                    st.session_state.monitoring_active = False
                    session_manager.save_monitoring_state(False, st.session_state.monitoring_interval)
        else:
            # No process but should be monitoring, start it
            st.session_state.monitoring_process = start_monitoring(st.session_state.monitoring_interval)
            if not st.session_state.monitoring_process:
                st.session_state.monitoring_active = False
                session_manager.save_monitoring_state(False, st.session_state.monitoring_interval)

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
                    session_manager.login(username)  # Save to persistent storage
                    st.sidebar.success(f"Logged in as {username}")
                    st.rerun()
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
        session_manager.logout()  # Clear persistent storage
        st.rerun()

    # Real-time Monitoring Controls
    st.sidebar.header("🖥️ Real-time Monitoring")
    
    # Metric selection
    metric_manager = MetricCollectorManager()
    available_metrics = metric_manager.get_available_metrics()
    
    st.sidebar.subheader("📊 Select Metrics to Monitor")
    selected_metrics = st.sidebar.multiselect(
        "Choose metrics to display:",
        options=available_metrics,
        default=st.session_state.selected_metrics,
        help="Select which metrics you want to monitor in real-time"
    )
    
    # Update selected metrics in session state
    if selected_metrics != st.session_state.selected_metrics:
        st.session_state.selected_metrics = selected_metrics
    
    # Show metric descriptions
    if selected_metrics:
        st.sidebar.markdown("**Selected Metrics:**")
        for metric in selected_metrics:
            info = metric_manager.get_metric_info(metric)
            if info:
                st.sidebar.caption(f"• {info['description']} ({info['unit']})")
    
    # Monitoring status
    if st.session_state.monitoring_active:
        st.sidebar.success("✅ Monitoring Active")
        if st.sidebar.button("🛑 Stop Monitoring"):
            if stop_monitoring(st.session_state.monitoring_process):
                st.session_state.monitoring_active = False
                st.session_state.monitoring_process = None
                session_manager.save_monitoring_state(False, st.session_state.monitoring_interval)
                st.success("Monitoring stopped!")
                st.rerun()
    else:
        st.sidebar.info("⏸️ Monitoring Inactive")
        
        # Monitoring configuration
        interval = st.sidebar.slider("Collection Interval (seconds)", 30, 300, 60)
        
        if st.sidebar.button("▶️ Start Monitoring"):
            process = start_monitoring(interval, selected_metrics)
            if process:
                st.session_state.monitoring_active = True
                st.session_state.monitoring_process = process
                st.session_state.monitoring_interval = interval
                session_manager.save_monitoring_state(True, interval)
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
        # Refresh every 30 seconds when monitoring is active (reduced frequency to prevent JS issues)
        if time.time() - st.session_state.last_refresh > 30:
            st.session_state.last_refresh = time.time()
            st.rerun()

    # Load data (real-time if monitoring, otherwise historical)
    try:
        if st.session_state.monitoring_active:
            metrics_df, logs_df = get_live_metrics()
            data_source = "🔄 Live Data"
        else:
            metrics_df, logs_df = load_data()
            data_source = "📊 Historical Data"

        # Display data source indicator
        st.info(f"{data_source} - {'Monitoring Active' if st.session_state.monitoring_active else 'Historical View'}")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        metrics_df, logs_df = pd.DataFrame(), pd.DataFrame()
        st.info("Using fallback data")

    # Detect anomalies for all metrics
    if not metrics_df.empty:
        cpu_analyzed = detect_anomalies(metrics_df, column="cpu_usage", window=60, z_threshold=3.5)
        memory_analyzed = detect_anomalies(metrics_df, column="memory_usage", window=60, z_threshold=3.5)
        latency_analyzed = detect_anomalies(metrics_df, column="latency_ms", window=60, z_threshold=3.5)
    else:
        cpu_analyzed = memory_analyzed = latency_analyzed = metrics_df

    # Dynamic Multi-Metric Dashboard
    st.subheader("📊 Live System Monitoring Dashboard")
    
    if not metrics_df.empty and st.session_state.selected_metrics:
        # Create dynamic columns based on selected metrics
        num_metrics = len(st.session_state.selected_metrics)
        cols = st.columns(min(3, num_metrics))  # Max 3 columns
        
        # Analyze each selected metric
        analyzed_metrics = {}
        for metric in st.session_state.selected_metrics:
            if metric in metrics_df.columns:
                analyzed_metrics[metric] = detect_anomalies(metrics_df, column=metric, window=60, z_threshold=3.5)
            else:
                analyzed_metrics[metric] = metrics_df
        
        # Display each selected metric
        for i, metric in enumerate(st.session_state.selected_metrics):
            col_idx = i % len(cols)
            metric_info = metric_manager.get_metric_info(metric)
            
            with cols[col_idx]:
                if metric_info:
                    st.markdown(f"### {metric_info['description']}")
                else:
                    st.markdown(f"### {metric.replace('_', ' ').title()}")
                
                # Create chart for this metric
                if metric in metrics_df.columns:
                    if st.session_state.monitoring_active:
                        fig = create_real_time_chart(analyzed_metrics[metric], metric)
                    else:
                        fig = px.line(
                            analyzed_metrics[metric],
                            x="timestamp",
                            y=metric,
                            title=f"{metric.replace('_', ' ').title()} over Time",
                        )
                        if "anomaly" in analyzed_metrics[metric].columns:
                            anomalies = analyzed_metrics[metric][analyzed_metrics[metric]["anomaly"]]
                            if not anomalies.empty:
                                fig.add_scatter(
                                    x=anomalies["timestamp"],
                                    y=anomalies[metric],
                                    mode="markers",
                                    marker=dict(color="red", size=6),
                                    name="Anomaly",
                                )
                    
                    st.plotly_chart(fig, use_container_width=True, height=300)
                    
                    # Show current value
                    if not metrics_df.empty:
                        latest_value = metrics_df[metric].iloc[-1] if metric in metrics_df.columns else 0
                        st.metric(
                            f"Current {metric_info['description'] if metric_info else metric.replace('_', ' ').title()}",
                            f"{latest_value:.2f}{metric_info['unit'] if metric_info else ''}"
                        )
                    
                    # Show relevant logs
                    if not logs_df.empty:
                        # Find logs related to this metric
                        metric_keywords = metric.replace('_', ' ').lower()
                        relevant_logs = logs_df[logs_df['message'].str.contains(metric_keywords, case=False, na=False)].tail(3)
                        if not relevant_logs.empty:
                            st.markdown("**Recent logs:**")
                            for _, log in relevant_logs.iterrows():
                                st.caption(f"{log['timestamp']}: {log['message']}")
                else:
                    st.warning(f"Metric '{metric}' not available in data")
        
        # System Status Summary
        st.markdown("---")
        st.subheader("📈 System Status Summary")
        
        if st.session_state.monitoring_active and not metrics_df.empty:
            latest = metrics_df.iloc[-1]
            
            # Create dynamic metrics grid based on selected metrics
            num_selected = len(st.session_state.selected_metrics)
            if num_selected > 0:
                # Create columns for selected metrics + monitoring info
                cols = st.columns(min(4, num_selected + 1))
                
                # Display each selected metric
                for i, metric in enumerate(st.session_state.selected_metrics):
                    if i < len(cols) - 1:  # Leave last column for monitoring info
                        metric_info = metric_manager.get_metric_info(metric)
                        if metric in metrics_df.columns:
                            current_value = latest[metric]
                            avg_value = metrics_df[metric].mean()
                            delta_value = current_value - avg_value
                            
                            with cols[i]:
                                st.metric(
                                    metric_info['description'] if metric_info else metric.replace('_', ' ').title(),
                                    f"{current_value:.2f}{metric_info['unit'] if metric_info else ''}",
                                    delta=f"{delta_value:.2f}{metric_info['unit'] if metric_info else ''}"
                                )
                
                # Monitoring info in last column
                with cols[-1]:
                    st.metric(
                        "Monitoring Time", 
                        f"{len(metrics_df)} samples",
                        delta=f"Every {st.session_state.monitoring_interval}s"
                    )
        
        # Anomaly Summary
        if not metrics_df.empty and st.session_state.selected_metrics:
            st.markdown("### 🔍 Anomaly Detection")
            
            # Create columns for selected metrics
            num_selected = len(st.session_state.selected_metrics)
            if num_selected > 0:
                cols = st.columns(min(3, num_selected))
                
                for i, metric in enumerate(st.session_state.selected_metrics):
                    if i < len(cols):
                        metric_info = metric_manager.get_metric_info(metric)
                        if metric in analyzed_metrics and 'anomaly' in analyzed_metrics[metric].columns:
                            anomalies_count = analyzed_metrics[metric][analyzed_metrics[metric]['anomaly']].shape[0]
                        else:
                            anomalies_count = 0
                        
                        with cols[i]:
                            st.metric(
                                f"{metric_info['description'] if metric_info else metric.replace('_', ' ').title()} Anomalies",
                                anomalies_count,
                                delta="Last 24h"
                            )
    
    else:
        st.warning("No metrics data available. Start monitoring to see live data.")

    # Show log table
    with st.expander("View Logs"):
        try:
            if not logs_df.empty:
                # Convert to string representation to avoid JavaScript issues
                logs_display = logs_df.tail(100).copy()
                # Ensure timestamp is properly formatted
                if 'timestamp' in logs_display.columns:
                    logs_display['timestamp'] = logs_display['timestamp'].astype(str)
                
                st.dataframe(
                    logs_display,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No logs available. Start monitoring to see live logs.")
        except Exception as e:
            st.error(f"Error displaying logs: {e}")
            st.info("Try refreshing the page or restarting monitoring.")



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
            if not cpu_analyzed.empty:
                rca = root_cause_analysis(cpu_analyzed, logs_df)
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