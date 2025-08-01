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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SystemMonitor:
    """Collects system metrics from the current machine."""
    
    def __init__(self, target_url: str = None):
        self.target_url = target_url
        self.system = platform.system()
        logger.info(f"Initializing system monitor for {self.system}")
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used = memory.used / (1024**3)  # GB
            memory_total = memory.total / (1024**3)  # GB
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network metrics
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv
            
            # System load (Unix-like systems)
            load_avg = None
            if hasattr(psutil, 'getloadavg'):
                try:
                    load_avg = psutil.getloadavg()
                except:
                    pass
            
            # Process count
            process_count = len(psutil.pids())
            
            # Temperature (if available)
            temperature = None
            try:
                if self.system == "Darwin":  # macOS
                    # Try to get temperature using system_profiler
                    import subprocess
                    result = subprocess.run(['system_profiler', 'SPThermalDataType'], 
                                         capture_output=True, text=True)
                    if 'Temperature' in result.stdout:
                        # Extract temperature from output
                        temp_line = [line for line in result.stdout.split('\n') 
                                   if 'Temperature' in line]
                        if temp_line:
                            temperature = temp_line[0].split(':')[-1].strip()
            except:
                pass
            
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "hostname": platform.node(),
                "system": self.system,
                "cpu_usage": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_freq_mhz": cpu_freq.current if cpu_freq else None,
                "memory_usage": memory_percent,
                "memory_used_gb": round(memory_used, 2),
                "memory_total_gb": round(memory_total, 2),
                "disk_usage": disk_percent,
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "network_bytes_sent": network_bytes_sent,
                "network_bytes_recv": network_bytes_recv,
                "process_count": process_count,
                "load_average": load_avg,
                "temperature": temperature
            }
            
            logger.info(f"Collected metrics: CPU {cpu_percent}%, Memory {memory_percent}%, Disk {disk_percent}%")
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
            
            # Convert to CSV format
            csv_line = f"{metrics['timestamp']},{metrics['cpu_usage']},{metrics['memory_usage']},{metrics.get('latency_ms', 0)}\n"
            
            with open(metrics_file, "a") as f:
                f.write(csv_line)
            
            # Save logs
            logs_file = "data/real_logs.csv"
            for log in logs:
                csv_line = f"{log['timestamp']},{log['level']},{log['message']}\n"
                with open(logs_file, "a") as f:
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
    
    args = parser.parse_args()
    
    # Initialize monitor
    target_url = None if args.local_only else args.target
    monitor = SystemMonitor(target_url)
    
    # Run monitoring
    monitor.run_monitoring(args.interval, args.duration)


if __name__ == "__main__":
    main() 