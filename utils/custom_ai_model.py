"""
Custom AI Model Interface
=========================

This module provides a flexible interface for integrating your own AI explanation model
instead of using OpenAI. You can easily replace the AI model implementation while
maintaining the same interface for the Streamlit app.

To use your own AI model:
1. Implement the CustomAIModel class below
2. Update the get_ai_model() function to return your model
3. The app will automatically use your custom model
"""

from typing import Dict, Any, Optional
import pandas as pd
from abc import ABC, abstractmethod


class CustomAIModel(ABC):
    """
    Abstract base class for custom AI models.
    
    Implement this class to create your own AI explanation model.
    """
    
    @abstractmethod
    def generate_answer(
        self, 
        question: str, 
        metrics_df: pd.DataFrame, 
        logs_df: pd.DataFrame,
        **kwargs
    ) -> Dict[str, str]:
        """
        Generate an answer to a question about system health.
        
        Args:
            question: The user's question about system health
            metrics_df: DataFrame with system metrics
            logs_df: DataFrame with system logs
            **kwargs: Additional parameters for your model
            
        Returns:
            Dictionary with 'answer' and 'reasoning' keys
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the AI model is available and ready to use.
        
        Returns:
            True if the model is available, False otherwise
        """
        pass


class EnhancedRuleBasedAI(CustomAIModel):
    """
    Enhanced rule-based AI model that provides intelligent explanations
    without requiring external API calls.
    
    This model uses pattern matching, statistical analysis, and domain knowledge
    to provide meaningful explanations about system health.
    """
    
    def __init__(self):
        self.available = True
    
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
        Generate intelligent answers using rule-based analysis.
        """
        # Analyze the question and data
        question_lower = question.lower()
        
        # Extract key information
        metrics_summary = self._analyze_metrics(metrics_df)
        log_analysis = self._analyze_logs(logs_df)
        anomaly_analysis = self._analyze_anomalies(metrics_df)
        
        # Generate answer based on question type
        if any(word in question_lower for word in ['cpu', 'usage', 'spike', 'high']):
            answer, reasoning = self._analyze_cpu_usage(question, metrics_summary, log_analysis, anomaly_analysis)
        elif any(word in question_lower for word in ['memory', 'ram', 'out of memory']):
            answer, reasoning = self._analyze_memory_usage(question, metrics_summary, log_analysis, anomaly_analysis)
        elif any(word in question_lower for word in ['latency', 'slow', 'response time']):
            answer, reasoning = self._analyze_latency(question, metrics_summary, log_analysis, anomaly_analysis)
        elif any(word in question_lower for word in ['error', 'problem', 'issue', 'wrong']):
            answer, reasoning = self._analyze_errors(question, metrics_summary, log_analysis, anomaly_analysis)
        else:
            answer, reasoning = self._analyze_general_health(question, metrics_summary, log_analysis, anomaly_analysis)
        
        return {"answer": answer, "reasoning": reasoning}
    
    def _analyze_metrics(self, metrics_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze metrics and extract key statistics."""
        if metrics_df.empty:
            return {}
        
        latest = metrics_df.iloc[-1]
        summary = metrics_df.describe()
        
        return {
            'latest_cpu': latest.get('cpu_usage', 0),
            'latest_memory': latest.get('memory_usage', 0),
            'latest_latency': latest.get('latency_ms', 0),
            'avg_cpu': summary.get('cpu_usage', {}).get('mean', 0),
            'avg_memory': summary.get('memory_usage', {}).get('mean', 0),
            'avg_latency': summary.get('latency_ms', {}).get('mean', 0),
            'cpu_std': summary.get('cpu_usage', {}).get('std', 0),
            'memory_std': summary.get('memory_usage', {}).get('std', 0),
            'latency_std': summary.get('latency_ms', {}).get('std', 0),
            'total_records': len(metrics_df)
        }
    
    def _analyze_logs(self, logs_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze logs and extract error patterns."""
        if logs_df.empty:
            return {}
        
        # Count error levels
        error_counts = logs_df['level'].value_counts().to_dict()
        
        # Analyze recent errors
        recent_logs = logs_df.tail(20)
        recent_errors = recent_logs[recent_logs['level'].isin(['ERROR', 'WARN'])]
        
        # Extract common error patterns
        error_patterns = {}
        for _, log in recent_errors.iterrows():
            message = log['message'].lower()
            if 'memory' in message:
                error_patterns['memory_issues'] = error_patterns.get('memory_issues', 0) + 1
            elif 'timeout' in message:
                error_patterns['timeout_issues'] = error_patterns.get('timeout_issues', 0) + 1
            elif 'disk' in message:
                error_patterns['disk_issues'] = error_patterns.get('disk_issues', 0) + 1
            elif 'api' in message:
                error_patterns['api_issues'] = error_patterns.get('api_issues', 0) + 1
        
        return {
            'error_counts': error_counts,
            'recent_errors': len(recent_errors),
            'error_patterns': error_patterns,
            'total_logs': len(logs_df)
        }
    
    def _analyze_anomalies(self, metrics_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze potential anomalies in metrics."""
        if metrics_df.empty:
            return {}
        
        # Simple anomaly detection
        cpu_values = metrics_df['cpu_usage'].dropna()
        memory_values = metrics_df['memory_usage'].dropna()
        
        cpu_mean = cpu_values.mean()
        cpu_std = cpu_values.std()
        memory_mean = memory_values.mean()
        memory_std = memory_values.std()
        
        # Find recent anomalies (last 10 records)
        recent = metrics_df.tail(10)
        cpu_anomalies = recent[abs(recent['cpu_usage'] - cpu_mean) > 2 * cpu_std]
        memory_anomalies = recent[abs(recent['memory_usage'] - memory_mean) > 2 * memory_std]
        
        return {
            'cpu_anomalies': len(cpu_anomalies),
            'memory_anomalies': len(memory_anomalies),
            'cpu_mean': cpu_mean,
            'memory_mean': memory_mean,
            'cpu_std': cpu_std,
            'memory_std': memory_std
        }
    
    def _analyze_cpu_usage(self, question: str, metrics: Dict, logs: Dict, anomalies: Dict) -> tuple:
        """Analyze CPU usage patterns."""
        latest_cpu = metrics.get('latest_cpu', 0)
        avg_cpu = metrics.get('avg_cpu', 0)
        cpu_anomalies = anomalies.get('cpu_anomalies', 0)
        
        if latest_cpu > 80:
            severity = "high"
            status = "concerning"
        elif latest_cpu > 60:
            severity = "moderate"
            status = "elevated"
        else:
            severity = "normal"
            status = "healthy"
        
        answer = f"Current CPU usage is {latest_cpu:.1f}% (average: {avg_cpu:.1f}%). "
        
        if cpu_anomalies > 0:
            answer += f"Detected {cpu_anomalies} recent CPU anomalies. "
        
        if severity == "high":
            answer += "This indicates high system load that may require attention."
        elif severity == "moderate":
            answer += "CPU usage is elevated but within acceptable ranges."
        else:
            answer += "CPU usage is within normal operating parameters."
        
        reasoning = f"Analyzed CPU metrics: current={latest_cpu:.1f}%, average={avg_cpu:.1f}%, anomalies={cpu_anomalies}. "
        reasoning += f"Severity assessment: {severity} ({status})."
        
        return answer, reasoning
    
    def _analyze_memory_usage(self, question: str, metrics: Dict, logs: Dict, anomalies: Dict) -> tuple:
        """Analyze memory usage patterns."""
        latest_memory = metrics.get('latest_memory', 0)
        avg_memory = metrics.get('avg_memory', 0)
        memory_anomalies = anomalies.get('memory_anomalies', 0)
        memory_issues = logs.get('error_patterns', {}).get('memory_issues', 0)
        
        if latest_memory > 90:
            severity = "critical"
            status = "memory pressure"
        elif latest_memory > 75:
            severity = "high"
            status = "elevated memory usage"
        else:
            severity = "normal"
            status = "healthy memory levels"
        
        answer = f"Current memory usage is {latest_memory:.1f}% (average: {avg_memory:.1f}%). "
        
        if memory_issues > 0:
            answer += f"Detected {memory_issues} memory-related errors. "
        
        if memory_anomalies > 0:
            answer += f"Found {memory_anomalies} memory usage anomalies. "
        
        if severity == "critical":
            answer += "Memory usage is critically high and may cause system instability."
        elif severity == "high":
            answer += "Memory usage is elevated and should be monitored."
        else:
            answer += "Memory usage is within normal operating parameters."
        
        reasoning = f"Analyzed memory metrics: current={latest_memory:.1f}%, average={avg_memory:.1f}%, "
        reasoning += f"anomalies={memory_anomalies}, memory_errors={memory_issues}. "
        reasoning += f"Severity: {severity} ({status})."
        
        return answer, reasoning
    
    def _analyze_latency(self, question: str, metrics: Dict, logs: Dict, anomalies: Dict) -> tuple:
        """Analyze latency patterns."""
        latest_latency = metrics.get('latest_latency', 0)
        avg_latency = metrics.get('avg_latency', 0)
        
        if latest_latency > 200:
            severity = "high"
            status = "slow response times"
        elif latest_latency > 150:
            severity = "moderate"
            status = "elevated latency"
        else:
            severity = "normal"
            status = "good response times"
        
        answer = f"Current latency is {latest_latency:.1f}ms (average: {avg_latency:.1f}ms). "
        
        if severity == "high":
            answer += "Response times are significantly slow and may impact user experience."
        elif severity == "moderate":
            answer += "Latency is elevated but may be acceptable depending on the application."
        else:
            answer += "Response times are within acceptable ranges."
        
        reasoning = f"Analyzed latency metrics: current={latest_latency:.1f}ms, average={avg_latency:.1f}ms. "
        reasoning += f"Severity: {severity} ({status})."
        
        return answer, reasoning
    
    def _analyze_errors(self, question: str, metrics: Dict, logs: Dict, anomalies: Dict) -> tuple:
        """Analyze error patterns."""
        recent_errors = logs.get('recent_errors', 0)
        error_patterns = logs.get('error_patterns', {})
        total_logs = logs.get('total_logs', 0)
        
        if recent_errors == 0:
            answer = "No recent errors detected. System appears to be operating normally."
            reasoning = "No error patterns found in recent logs."
        else:
            error_types = list(error_patterns.keys())
            answer = f"Detected {recent_errors} recent errors. "
            
            if error_types:
                answer += f"Error types include: {', '.join(error_types)}. "
            
            if recent_errors > 10:
                answer += "Error rate is concerning and may indicate system issues."
            elif recent_errors > 5:
                answer += "Moderate error activity detected."
            else:
                answer += "Low error activity, system appears stable."
            
            reasoning = f"Analyzed {total_logs} total logs, found {recent_errors} recent errors. "
            reasoning += f"Error patterns: {error_patterns}."
        
        return answer, reasoning
    
    def _analyze_general_health(self, question: str, metrics: Dict, logs: Dict, anomalies: Dict) -> tuple:
        """Provide general system health assessment."""
        latest_cpu = metrics.get('latest_cpu', 0)
        latest_memory = metrics.get('latest_memory', 0)
        latest_latency = metrics.get('latest_latency', 0)
        recent_errors = logs.get('recent_errors', 0)
        
        # Calculate overall health score
        health_score = 100
        
        if latest_cpu > 80:
            health_score -= 20
        elif latest_cpu > 60:
            health_score -= 10
            
        if latest_memory > 90:
            health_score -= 25
        elif latest_memory > 75:
            health_score -= 15
            
        if latest_latency > 200:
            health_score -= 20
        elif latest_latency > 150:
            health_score -= 10
            
        if recent_errors > 10:
            health_score -= 30
        elif recent_errors > 5:
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
        answer += f"Current metrics - CPU: {latest_cpu:.1f}%, Memory: {latest_memory:.1f}%, "
        answer += f"Latency: {latest_latency:.1f}ms, Recent errors: {recent_errors}."
        
        reasoning = f"Health score: {health_score}/100. Analyzed CPU ({latest_cpu:.1f}%), "
        reasoning += f"Memory ({latest_memory:.1f}%), Latency ({latest_latency:.1f}ms), "
        reasoning += f"Errors ({recent_errors}). Status: {status}."
        
        return answer, reasoning


def get_ai_model() -> CustomAIModel:
    """
    Get the AI model to use for explanations.
    
    Replace this function to use your own AI model implementation.
    Currently returns an advanced temporal-aware model.
    
    Returns:
        CustomAIModel instance
    """
    try:
        from .advanced_ai_model import get_advanced_ai_model
        return get_advanced_ai_model()
    except ImportError:
        # Fallback to basic model if advanced model not available
        return EnhancedRuleBasedAI()


# Example of how to implement your own AI model:
class YourCustomAIModel(CustomAIModel):
    """
    Example implementation of a custom AI model.
    
    Replace this with your own AI model implementation.
    """
    
    def __init__(self, model_path: str = None):
        """
        Initialize your AI model.
        
        Args:
            model_path: Path to your model file (if needed)
        """
        self.model_path = model_path
        self.available = True  # Set to False if model fails to load
    
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
        Generate answer using your custom AI model.
        
        Implement your AI model logic here.
        """
        # Example implementation - replace with your actual AI model
        try:
            # Your AI model logic here
            # For example:
            # - Load your model
            # - Preprocess the data
            # - Generate response
            # - Post-process the output
            
            # Placeholder implementation
            answer = f"Custom AI model response to: {question}"
            reasoning = "Generated using your custom AI model implementation."
            
            return {"answer": answer, "reasoning": reasoning}
            
        except Exception as e:
            return {
                "answer": "Custom AI model encountered an error.",
                "reasoning": f"Error: {str(e)}"
            } 