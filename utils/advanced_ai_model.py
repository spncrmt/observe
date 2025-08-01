"""
Advanced AI Model for Temporal Analysis
=======================================

This module provides a more sophisticated AI model that can handle:
- Temporal questions (when, last time, previous, etc.)
- Historical pattern analysis
- Context-aware responses
- Specific event identification
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from utils.custom_ai_model import CustomAIModel


class AdvancedObservabilityAI(CustomAIModel):
    """
    Advanced AI model that can handle temporal questions and provide
    sophisticated analysis of system metrics and logs.
    """
    
    def __init__(self):
        self.available = True
        self.temporal_keywords = [
            'when', 'last', 'previous', 'before', 'after', 'recent',
            'spike', 'peak', 'high', 'low', 'increase', 'decrease'
        ]
    
    def is_available(self) -> bool:
        return self.available
    
    def generate_answer(
        self, 
        question: str, 
        metrics_df: pd.DataFrame, 
        logs_df: pd.DataFrame,
        **kwargs
    ) -> Dict[str, str]:
        """
        Generate intelligent answers with temporal awareness.
        """
        question_lower = question.lower()
        
        # Check if this is a temporal question
        if self._is_temporal_question(question_lower):
            return self._handle_temporal_question(question, metrics_df, logs_df)
        
        # Check for specific metric questions
        if any(word in question_lower for word in ['cpu', 'usage', 'spike', 'high']):
            return self._analyze_cpu_temporal(question, metrics_df, logs_df)
        elif any(word in question_lower for word in ['memory', 'ram', 'out of memory']):
            return self._analyze_memory_temporal(question, metrics_df, logs_df)
        elif any(word in question_lower for word in ['latency', 'slow', 'response time']):
            return self._analyze_latency_temporal(question, metrics_df, logs_df)
        elif any(word in question_lower for word in ['error', 'problem', 'issue', 'wrong']):
            return self._analyze_errors_temporal(question, metrics_df, logs_df)
        else:
            return self._analyze_general_health_temporal(question, metrics_df, logs_df)
    
    def _is_temporal_question(self, question: str) -> bool:
        """Check if the question is asking about temporal events."""
        return any(keyword in question for keyword in self.temporal_keywords)
    
    def _handle_temporal_question(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Handle questions about when events occurred."""
        question_lower = question.lower()
        
        # Extract the metric being asked about
        if 'cpu' in question_lower:
            return self._find_cpu_spikes(question, metrics_df, logs_df)
        elif 'memory' in question_lower:
            return self._find_memory_spikes(question, metrics_df, logs_df)
        elif 'latency' in question_lower or 'slow' in question_lower:
            return self._find_latency_spikes(question, metrics_df, logs_df)
        elif 'error' in question_lower:
            return self._find_recent_errors(question, metrics_df, logs_df)
        else:
            return self._find_general_spikes(question, metrics_df, logs_df)
    
    def _find_cpu_spikes(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Find CPU usage spikes and their timing."""
        # Define what constitutes a "spike"
        cpu_mean = metrics_df['cpu_usage'].mean()
        cpu_std = metrics_df['cpu_usage'].std()
        spike_threshold = cpu_mean + 2 * cpu_std
        
        # Find spikes
        spikes = metrics_df[metrics_df['cpu_usage'] > spike_threshold].copy()
        spikes = spikes.sort_values('timestamp', ascending=False)
        
        if spikes.empty:
            answer = "No significant CPU usage spikes detected in the available data."
            reasoning = f"Analyzed {len(metrics_df)} records. No CPU usage above {spike_threshold:.1f}% (mean + 2*std)."
        else:
            # Get the most recent spike
            latest_spike = spikes.iloc[0]
            spike_time = latest_spike['timestamp']
            spike_value = latest_spike['cpu_usage']
            
            # Find related logs
            window_start = spike_time - timedelta(minutes=5)
            window_end = spike_time + timedelta(minutes=5)
            related_logs = logs_df[
                (logs_df['timestamp'] >= window_start) & 
                (logs_df['timestamp'] <= window_end)
            ]
            
            # Analyze related errors
            errors = related_logs[related_logs['level'].isin(['ERROR', 'WARN'])]
            error_summary = ""
            if not errors.empty:
                error_counts = errors['message'].value_counts().head(3)
                error_summary = f" Related errors: {', '.join([f'{msg} ({count})' for msg, count in error_counts.items()])}."
            
            answer = f"The last significant CPU usage spike occurred on {spike_time.strftime('%Y-%m-%d at %H:%M:%S')} with {spike_value:.1f}% usage.{error_summary}"
            
            if len(spikes) > 1:
                second_spike = spikes.iloc[1]
                answer += f" The previous spike was on {second_spike['timestamp'].strftime('%Y-%m-%d at %H:%M:%S')} with {second_spike['cpu_usage']:.1f}% usage."
            
            reasoning = f"Found {len(spikes)} CPU spikes above {spike_threshold:.1f}% threshold. Analyzed {len(related_logs)} logs within ±5 minutes of latest spike."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _find_memory_spikes(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Find memory usage spikes and their timing."""
        memory_mean = metrics_df['memory_usage'].mean()
        memory_std = metrics_df['memory_usage'].std()
        spike_threshold = memory_mean + 2 * memory_std
        
        spikes = metrics_df[metrics_df['memory_usage'] > spike_threshold].copy()
        spikes = spikes.sort_values('timestamp', ascending=False)
        
        if spikes.empty:
            answer = "No significant memory usage spikes detected in the available data."
            reasoning = f"Analyzed {len(metrics_df)} records. No memory usage above {spike_threshold:.1f}% (mean + 2*std)."
        else:
            latest_spike = spikes.iloc[0]
            spike_time = latest_spike['timestamp']
            spike_value = latest_spike['memory_usage']
            
            # Find related logs
            window_start = spike_time - timedelta(minutes=5)
            window_end = spike_time + timedelta(minutes=5)
            related_logs = logs_df[
                (logs_df['timestamp'] >= window_start) & 
                (logs_df['timestamp'] <= window_end)
            ]
            
            errors = related_logs[related_logs['level'].isin(['ERROR', 'WARN'])]
            error_summary = ""
            if not errors.empty:
                error_counts = errors['message'].value_counts().head(3)
                error_summary = f" Related errors: {', '.join([f'{msg} ({count})' for msg, count in error_counts.items()])}."
            
            answer = f"The last significant memory usage spike occurred on {spike_time.strftime('%Y-%m-%d at %H:%M:%S')} with {spike_value:.1f}% usage.{error_summary}"
            
            if len(spikes) > 1:
                second_spike = spikes.iloc[1]
                answer += f" The previous spike was on {second_spike['timestamp'].strftime('%Y-%m-%d at %H:%M:%S')} with {second_spike['memory_usage']:.1f}% usage."
            
            reasoning = f"Found {len(spikes)} memory spikes above {spike_threshold:.1f}% threshold. Analyzed {len(related_logs)} logs within ±5 minutes of latest spike."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _find_latency_spikes(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Find latency spikes and their timing."""
        latency_mean = metrics_df['latency_ms'].mean()
        latency_std = metrics_df['latency_ms'].std()
        spike_threshold = latency_mean + 2 * latency_std
        
        spikes = metrics_df[metrics_df['latency_ms'] > spike_threshold].copy()
        spikes = spikes.sort_values('timestamp', ascending=False)
        
        if spikes.empty:
            answer = "No significant latency spikes detected in the available data."
            reasoning = f"Analyzed {len(metrics_df)} records. No latency above {spike_threshold:.1f}ms (mean + 2*std)."
        else:
            latest_spike = spikes.iloc[0]
            spike_time = latest_spike['timestamp']
            spike_value = latest_spike['latency_ms']
            
            answer = f"The last significant latency spike occurred on {spike_time.strftime('%Y-%m-%d at %H:%M:%S')} with {spike_value:.1f}ms response time."
            
            if len(spikes) > 1:
                second_spike = spikes.iloc[1]
                answer += f" The previous spike was on {second_spike['timestamp'].strftime('%Y-%m-%d at %H:%M:%S')} with {second_spike['latency_ms']:.1f}ms response time."
            
            reasoning = f"Found {len(spikes)} latency spikes above {spike_threshold:.1f}ms threshold."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _find_recent_errors(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Find recent error patterns and their timing."""
        # Get recent errors (last 24 hours)
        recent_cutoff = metrics_df['timestamp'].max() - timedelta(hours=24)
        recent_logs = logs_df[logs_df['timestamp'] >= recent_cutoff]
        recent_errors = recent_logs[recent_logs['level'].isin(['ERROR', 'WARN'])]
        
        if recent_errors.empty:
            answer = "No errors detected in the last 24 hours."
            reasoning = "Analyzed logs from the last 24 hours. No ERROR or WARN level messages found."
        else:
            # Group errors by time windows
            recent_errors = recent_errors.sort_values('timestamp', ascending=False)
            latest_error = recent_errors.iloc[0]
            
            # Count error types
            error_counts = recent_errors['message'].value_counts().head(5)
            error_summary = ", ".join([f"{msg} ({count})" for msg, count in error_counts.items()])
            
            answer = f"The last error occurred on {latest_error['timestamp'].strftime('%Y-%m-%d at %H:%M:%S')}: {latest_error['message']}. "
            answer += f"Recent error types: {error_summary}."
            
            reasoning = f"Found {len(recent_errors)} errors in the last 24 hours. Analyzed error patterns and timing."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _find_general_spikes(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Find general system spikes across all metrics."""
        # Analyze all metrics for spikes
        cpu_spikes = self._find_cpu_spikes(question, metrics_df, logs_df)
        memory_spikes = self._find_memory_spikes(question, metrics_df, logs_df)
        latency_spikes = self._find_latency_spikes(question, metrics_df, logs_df)
        
        # Combine the most recent spikes
        answer_parts = []
        if "No significant" not in cpu_spikes["answer"]:
            answer_parts.append("CPU: " + cpu_spikes["answer"].split(" occurred on ")[1].split(" with ")[0])
        if "No significant" not in memory_spikes["answer"]:
            answer_parts.append("Memory: " + memory_spikes["answer"].split(" occurred on ")[1].split(" with ")[0])
        if "No significant" not in latency_spikes["answer"]:
            answer_parts.append("Latency: " + latency_spikes["answer"].split(" occurred on ")[1].split(" with ")[0])
        
        if answer_parts:
            answer = "Recent system spikes: " + "; ".join(answer_parts)
        else:
            answer = "No significant system spikes detected in the available data."
        
        reasoning = f"Analyzed CPU, memory, and latency metrics for spikes. Found patterns across {len(metrics_df)} records."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _analyze_cpu_temporal(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Analyze CPU usage with temporal awareness."""
        current_cpu = metrics_df.iloc[-1]['cpu_usage']
        avg_cpu = metrics_df['cpu_usage'].mean()
        
        # Find recent trends
        recent_data = metrics_df.tail(20)
        recent_avg = recent_data['cpu_usage'].mean()
        
        if current_cpu > avg_cpu + 10:
            trend = "increasing"
            status = "elevated"
        elif current_cpu < avg_cpu - 10:
            trend = "decreasing"
            status = "below average"
        else:
            trend = "stable"
            status = "normal"
        
        answer = f"Current CPU usage is {current_cpu:.1f}% (average: {avg_cpu:.1f}%). "
        answer += f"Recent trend shows {trend} usage. "
        
        if trend == "increasing":
            answer += "This may indicate increasing system load."
        elif trend == "decreasing":
            answer += "This suggests reduced system activity."
        else:
            answer += "System appears to be operating normally."
        
        reasoning = f"Analyzed CPU trends: current={current_cpu:.1f}%, average={avg_cpu:.1f}%, recent_avg={recent_avg:.1f}%. Trend: {trend} ({status})."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _analyze_memory_temporal(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Analyze memory usage with temporal awareness."""
        current_memory = metrics_df.iloc[-1]['memory_usage']
        avg_memory = metrics_df['memory_usage'].mean()
        
        recent_data = metrics_df.tail(20)
        recent_avg = recent_data['memory_usage'].mean()
        
        if current_memory > avg_memory + 10:
            trend = "increasing"
            status = "elevated"
        elif current_memory < avg_memory - 10:
            trend = "decreasing"
            status = "below average"
        else:
            trend = "stable"
            status = "normal"
        
        answer = f"Current memory usage is {current_memory:.1f}% (average: {avg_memory:.1f}%). "
        answer += f"Recent trend shows {trend} usage. "
        
        if trend == "increasing":
            answer += "This may indicate memory pressure or potential leaks."
        elif trend == "decreasing":
            answer += "This suggests memory cleanup or reduced load."
        else:
            answer += "Memory usage appears stable."
        
        reasoning = f"Analyzed memory trends: current={current_memory:.1f}%, average={avg_memory:.1f}%, recent_avg={recent_avg:.1f}%. Trend: {trend} ({status})."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _analyze_latency_temporal(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Analyze latency with temporal awareness."""
        current_latency = metrics_df.iloc[-1]['latency_ms']
        avg_latency = metrics_df['latency_ms'].mean()
        
        recent_data = metrics_df.tail(20)
        recent_avg = recent_data['latency_ms'].mean()
        
        if current_latency > avg_latency + 50:
            trend = "increasing"
            status = "slow"
        elif current_latency < avg_latency - 50:
            trend = "decreasing"
            status = "fast"
        else:
            trend = "stable"
            status = "normal"
        
        answer = f"Current latency is {current_latency:.1f}ms (average: {avg_latency:.1f}ms). "
        answer += f"Recent trend shows {trend} response times. "
        
        if trend == "increasing":
            answer += "This may indicate system performance issues."
        elif trend == "decreasing":
            answer += "This suggests improved system performance."
        else:
            answer += "Response times appear stable."
        
        reasoning = f"Analyzed latency trends: current={current_latency:.1f}ms, average={avg_latency:.1f}ms, recent_avg={recent_avg:.1f}ms. Trend: {trend} ({status})."
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _analyze_errors_temporal(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Analyze errors with temporal awareness."""
        return self._find_recent_errors(question, metrics_df, logs_df)
    
    def _analyze_general_health_temporal(self, question: str, metrics_df: pd.DataFrame, logs_df: pd.DataFrame) -> Dict[str, str]:
        """Analyze general system health with temporal awareness."""
        current_cpu = metrics_df.iloc[-1]['cpu_usage']
        current_memory = metrics_df.iloc[-1]['memory_usage']
        current_latency = metrics_df.iloc[-1]['latency_ms']
        
        # Calculate health score
        health_score = 100
        
        if current_cpu > 80:
            health_score -= 20
        elif current_cpu > 60:
            health_score -= 10
            
        if current_memory > 90:
            health_score -= 25
        elif current_memory > 75:
            health_score -= 15
            
        if current_latency > 200:
            health_score -= 20
        elif current_latency > 150:
            health_score -= 10
        
        # Check recent errors
        recent_logs = logs_df.tail(50)
        recent_errors = recent_logs[recent_logs['level'].isin(['ERROR', 'WARN'])]
        if len(recent_errors) > 10:
            health_score -= 30
        elif len(recent_errors) > 5:
            health_score -= 15
        
        if health_score >= 80:
            status = "healthy"
            assessment = "System is operating normally with good performance."
        elif health_score >= 60:
            status = "moderate"
            assessment = "System shows some concerns but is generally stable."
        else:
            status = "concerning"
            assessment = "System has multiple issues that require attention."
        
        answer = f"Overall system health: {status.upper()}. {assessment} "
        answer += f"Current metrics - CPU: {current_cpu:.1f}%, Memory: {current_memory:.1f}%, "
        answer += f"Latency: {current_latency:.1f}ms, Recent errors: {len(recent_errors)}."
        
        reasoning = f"Health score: {health_score}/100. Analyzed CPU ({current_cpu:.1f}%), "
        reasoning += f"Memory ({current_memory:.1f}%), Latency ({current_latency:.1f}ms), "
        reasoning += f"Errors ({len(recent_errors)}). Status: {status}."
        
        return {"answer": answer, "reasoning": reasoning}


def get_advanced_ai_model() -> CustomAIModel:
    """
    Get the advanced AI model for temporal analysis.
    
    Returns:
        AdvancedObservabilityAI instance
    """
    return AdvancedObservabilityAI() 