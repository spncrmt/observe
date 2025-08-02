#!/usr/bin/env python3
"""
System Monitoring Agent
=======================

This script collects real system metrics from your Mac or PC and sends them
to your observability dashboard. It can run as a background service to
continuously monitor your system health.

Usage:
    python scripts/system_monitor.py --target dashboard_url --interval 60
"""

import psutil
import time
import json
import requests
import argparse
import logging
from datetime import datetime
from typing import Dict, Any
import platform
import os
import sys

# Add the parent directory to the path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.metric_collectors import MetricCollectorManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """Collects system metrics from the current machine."""
    
    def __init__(self, target_url: str = None, selected_metrics: list = None):
        self.target_url = target_url
        self.system = platform.system()
        self.metric_manager = MetricCollectorManager()
        self.selected_metrics = selected_metrics or ["cpu_usage", "memory_usage"]
        logger.info(f"Initializing system monitor for {self.system}")
        logger.info(f"Selected metrics: {self.selected_metrics}")
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics using modular collectors."""
        try:
            # Collect metrics using the metric manager
            metric_data = self.metric_manager.collect_metrics(self.selected_metrics)
            
            # Convert to the expected format
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "hostname": platform.node(),
                "system": self.system,
            }
            
            # Add collected metrics
            for metric_name, data in metric_data.items():
                metrics[metric_name] = data.value
            
            # Add some additional system info
            metrics["cpu_count"] = psutil.cpu_count()
            metrics["memory_total_gb"] = round(psutil.virtual_memory().total / (1024**3), 2)
            
            # Log collected metrics
            metric_values = [f"{data.description} {data.value}{data.unit}" for data in metric_data.values()]
            logger.info(f"Collected metrics: {', '.join(metric_values)}")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return {}
    
    def collect_logs(self) -> list:
        """Collect system logs (simplified version)."""
        logs = []
        try:
            # Get recent system events
            current_time = datetime.now()
            
            # Check for high resource usage
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            if cpu_percent > 80:
                logs.append({
                    "timestamp": current_time.isoformat(),
                    "level": "WARN",
                    "message": f"High CPU usage detected: {cpu_percent:.1f}%"
                })
            
            if memory.percent > 85:
                logs.append({
                    "timestamp": current_time.isoformat(),
                    "level": "WARN",
                    "message": f"High memory usage detected: {memory.percent:.1f}%"
                })
            
            # Check disk space
            disk = psutil.disk_usage('/')
            if (disk.used / disk.total) * 100 > 90:
                logs.append({
                    "timestamp": current_time.isoformat(),
                    "level": "ERROR",
                    "message": f"Disk space critically low: {((disk.used / disk.total) * 100):.1f}% used"
                })
            
            # Add normal heartbeat
            logs.append({
                "timestamp": current_time.isoformat(),
                "level": "INFO",
                "message": "System monitoring heartbeat"
            })
            
        except Exception as e:
            logs.append({
                "timestamp": current_time.isoformat(),
                "level": "ERROR",
                "message": f"Error collecting logs: {str(e)}"
            })
        
        return logs
    
    def send_to_dashboard(self, metrics: Dict[str, Any], logs: list) -> bool:
        """Send metrics and logs to the dashboard."""
        if not self.target_url:
            logger.warning("No target URL configured, skipping send")
            return False
        
        try:
            payload = {
                "metrics": metrics,
                "logs": logs,
                "hostname": platform.node(),
                "system": self.system
            }
            
            response = requests.post(
                f"{self.target_url}/api/metrics",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("Successfully sent metrics to dashboard")
                return True
            else:
                logger.error(f"Failed to send metrics: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending to dashboard: {e}")
            return False
    
    def save_locally(self, metrics: Dict[str, Any], logs: list) -> None:
        """Save metrics and logs to local files."""
        try:
            # Save metrics
            metrics_file = "data/real_metrics.csv"
            os.makedirs("data", exist_ok=True)
            
            # Check if file exists and has headers
            file_exists = os.path.exists(metrics_file) and os.path.getsize(metrics_file) > 0
            
            # Build CSV line dynamically based on available metrics
            csv_fields = ["timestamp"] + self.selected_metrics
            csv_values = [metrics.get("timestamp", "")]
            for metric in self.selected_metrics:
                csv_values.append(str(metrics.get(metric, 0)))
            
            csv_line = ",".join(csv_values) + "\n"
            
            with open(metrics_file, "a") as f:
                # Write headers if file is new
                if not file_exists:
                    f.write(",".join(csv_fields) + "\n")
                f.write(csv_line)
            
            # Save logs
            logs_file = "data/real_logs.csv"
            for log in logs:
                # Check if logs file exists and has headers
                logs_file_exists = os.path.exists(logs_file) and os.path.getsize(logs_file) > 0
                
                csv_line = f"{log['timestamp']},{log['level']},{log['message']}\n"
                with open(logs_file, "a") as f:
                    # Write headers if file is new
                    if not logs_file_exists:
                        f.write("timestamp,level,message\n")
                    f.write(csv_line)
            
            logger.info("Saved metrics and logs locally")
            
        except Exception as e:
            logger.error(f"Error saving locally: {e}")
    
    def run_monitoring(self, interval: int = 60, duration: int = None):
        """Run continuous monitoring."""
        logger.info(f"Starting system monitoring (interval: {interval}s)")
        
        start_time = time.time()
        iteration = 0
        
        while True:
            try:
                iteration += 1
                logger.info(f"Collection iteration {iteration}")
                
                # Collect metrics and logs
                metrics = self.collect_metrics()
                logs = self.collect_logs()
                
                if metrics:
                    # Send to dashboard if configured
                    if self.target_url:
                        self.send_to_dashboard(metrics, logs)
                    
                    # Save locally
                    self.save_locally(metrics, logs)
                
                # Check if we should stop
                if duration and (time.time() - start_time) > duration:
                    logger.info("Monitoring duration completed")
                    break
                
                # Wait for next interval
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="System Monitoring Agent")
    parser.add_argument("--target", help="Dashboard URL to send metrics to")
    parser.add_argument("--interval", type=int, default=60, help="Collection interval in seconds")
    parser.add_argument("--duration", type=int, help="Duration to run in seconds")
    parser.add_argument("--local-only", action="store_true", help="Only save locally, don't send to dashboard")
    parser.add_argument("--metrics", nargs="+", default=["cpu_usage", "memory_usage"], 
                       help="Metrics to collect (space-separated list)")
    
    args = parser.parse_args()
    
    # Initialize monitor with selected metrics
    target_url = None if args.local_only else args.target
    monitor = SystemMonitor(target_url, selected_metrics=args.metrics)
    
    # Run monitoring
    monitor.run_monitoring(args.interval, args.duration)


if __name__ == "__main__":
    main() 