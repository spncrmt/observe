import psutil
import time
import platform
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricData:
    """Container for metric data with timestamp."""
    timestamp: datetime
    value: float
    unit: str
    description: str


class BaseMetricCollector:
    """Base class for metric collectors."""
    
    def __init__(self):
        self.name = "base"
        self.description = "Base metric collector"
        self.unit = ""
    
    def collect(self) -> MetricData:
        """Collect metric data. Override in subclasses."""
        raise NotImplementedError
    
    def is_available(self) -> bool:
        """Check if this collector is available on the current system."""
        return True


class CPUMetricCollector(BaseMetricCollector):
    """Collects CPU usage metrics."""
    
    def __init__(self):
        self.name = "cpu_usage"
        self.description = "CPU Usage"
        self.unit = "%"
    
    def collect(self) -> MetricData:
        return MetricData(
            timestamp=datetime.now(),
            value=psutil.cpu_percent(interval=1),
            unit=self.unit,
            description=self.description
        )


class MemoryMetricCollector(BaseMetricCollector):
    """Collects memory usage metrics."""
    
    def __init__(self):
        self.name = "memory_usage"
        self.description = "Memory Usage"
        self.unit = "%"
    
    def collect(self) -> MetricData:
        memory = psutil.virtual_memory()
        return MetricData(
            timestamp=datetime.now(),
            value=memory.percent,
            unit=self.unit,
            description=self.description
        )


class DiskIOMetricCollector(BaseMetricCollector):
    """Collects disk I/O metrics."""
    
    def __init__(self):
        self.name = "disk_io"
        self.description = "Disk I/O"
        self.unit = "MB/s"
        self._last_io = None
        self._last_time = None
    
    def collect(self) -> MetricData:
        current_io = psutil.disk_io_counters()
        current_time = time.time()
        
        if self._last_io and self._last_time:
            time_diff = current_time - self._last_time
            read_diff = (current_io.read_bytes - self._last_io.read_bytes) / (1024 * 1024)
            write_diff = (current_io.write_bytes - self._last_io.write_bytes) / (1024 * 1024)
            total_io = (read_diff + write_diff) / time_diff
        else:
            total_io = 0.0
        
        self._last_io = current_io
        self._last_time = current_time
        
        return MetricData(
            timestamp=datetime.now(),
            value=total_io,
            unit=self.unit,
            description=self.description
        )


class NetworkTrafficCollector(BaseMetricCollector):
    """Collects network traffic metrics."""
    
    def __init__(self):
        self.name = "network_traffic"
        self.description = "Network Traffic"
        self.unit = "MB/s"
        self._last_net = None
        self._last_time = None
    
    def collect(self) -> MetricData:
        current_net = psutil.net_io_counters()
        current_time = time.time()
        
        if self._last_net and self._last_time:
            time_diff = current_time - self._last_time
            bytes_diff = (current_net.bytes_sent + current_net.bytes_recv - 
                         self._last_net.bytes_sent - self._last_net.bytes_recv)
            traffic = (bytes_diff / (1024 * 1024)) / time_diff
        else:
            traffic = 0.0
        
        self._last_net = current_net
        self._last_time = current_time
        
        return MetricData(
            timestamp=datetime.now(),
            value=traffic,
            unit=self.unit,
            description=self.description
        )


class UptimeCollector(BaseMetricCollector):
    """Collects system uptime."""
    
    def __init__(self):
        self.name = "uptime"
        self.description = "System Uptime"
        self.unit = "hours"
    
    def collect(self) -> MetricData:
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = uptime_seconds / 3600
        
        return MetricData(
            timestamp=datetime.now(),
            value=uptime_hours,
            unit=self.unit,
            description=self.description
        )


class ResponseLatencyCollector(BaseMetricCollector):
    """Collects response latency (simulated)."""
    
    def __init__(self):
        self.name = "response_latency"
        self.description = "Response Latency"
        self.unit = "ms"
    
    def collect(self) -> MetricData:
        # Simulate latency measurement
        start_time = time.time()
        time.sleep(0.001)  # Simulate some work
        latency = (time.time() - start_time) * 1000
        
        return MetricData(
            timestamp=datetime.now(),
            value=latency,
            unit=self.unit,
            description=self.description
        )


class ErrorRateCollector(BaseMetricCollector):
    """Collects error rate (simulated)."""
    
    def __init__(self):
        self.name = "error_rate"
        self.description = "Error Rate"
        self.unit = "%"
    
    def collect(self) -> MetricData:
        # Simulate error rate based on system load
        cpu_percent = psutil.cpu_percent(interval=0.1)
        # Higher CPU usage might correlate with more errors
        error_rate = min(5.0, cpu_percent / 20.0)  # Max 5% error rate
        
        return MetricData(
            timestamp=datetime.now(),
            value=error_rate,
            unit=self.unit,
            description=self.description
        )


class ProcessHealthCollector(BaseMetricCollector):
    """Collects process health metrics."""
    
    def __init__(self):
        self.name = "process_health"
        self.description = "Process Health"
        self.unit = "processes"
    
    def collect(self) -> MetricData:
        # Count running processes
        process_count = len(psutil.pids())
        
        return MetricData(
            timestamp=datetime.now(),
            value=process_count,
            unit=self.unit,
            description=self.description
        )


class ServerLoadCollector(BaseMetricCollector):
    """Collects server load averages."""
    
    def __init__(self):
        self.name = "server_load"
        self.description = "Server Load"
        self.unit = "load"
    
    def collect(self) -> MetricData:
        if platform.system() == "Darwin":  # macOS
            # Get load average (1m, 5m, 15m)
            load_avg = psutil.getloadavg()
            # Use 1-minute load average
            load_value = load_avg[0]
        else:
            # For other systems, simulate load based on CPU
            load_value = psutil.cpu_percent(interval=0.1) / 100.0
        
        return MetricData(
            timestamp=datetime.now(),
            value=load_value,
            unit=self.unit,
            description=self.description
        )


class MetricCollectorManager:
    """Manages multiple metric collectors."""
    
    def __init__(self):
        self.collectors = {
            "cpu_usage": CPUMetricCollector(),
            "memory_usage": MemoryMetricCollector(),
            "disk_io": DiskIOMetricCollector(),
            "network_traffic": NetworkTrafficCollector(),
            "uptime": UptimeCollector(),
            "response_latency": ResponseLatencyCollector(),
            "error_rate": ErrorRateCollector(),
            "process_health": ProcessHealthCollector(),
            "server_load": ServerLoadCollector(),
        }
    
    def get_available_metrics(self) -> List[str]:
        """Get list of available metric names."""
        return list(self.collectors.keys())
    
    def get_collector(self, metric_name: str) -> Optional[BaseMetricCollector]:
        """Get a specific collector by name."""
        return self.collectors.get(metric_name)
    
    def collect_metrics(self, selected_metrics: List[str]) -> Dict[str, MetricData]:
        """Collect data for selected metrics only."""
        results = {}
        for metric_name in selected_metrics:
            collector = self.get_collector(metric_name)
            if collector and collector.is_available():
                try:
                    results[metric_name] = collector.collect()
                except Exception as e:
                    print(f"Error collecting {metric_name}: {e}")
        return results
    
    def get_metric_info(self, metric_name: str) -> Dict[str, Any]:
        """Get information about a specific metric."""
        collector = self.get_collector(metric_name)
        if collector:
            return {
                "name": collector.name,
                "description": collector.description,
                "unit": collector.unit,
                "available": collector.is_available()
            }
        return None 