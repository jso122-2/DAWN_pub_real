# utils/metrics_collector.py
"""
Metrics Collection System for DAWN
Provides comprehensive metric collection, analysis, and alerting capabilities.
"""

import asyncio
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import numpy as np
from datetime import datetime, timedelta
import json
from collections import deque
import psutil
import torch
from pydantic import BaseModel

from core.schema_anomaly_logger import log_anomaly, AnomalySeverity
from schema.registry import registry

class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"      # Monotonically increasing value
    GAUGE = "gauge"         # Point-in-time value
    HISTOGRAM = "histogram" # Distribution of values
    RATE = "rate"          # Events per time unit
    PERCENTAGE = "percentage" # Percentage value

@dataclass
class MetricValue:
    """Represents a single metric value with metadata."""
    value: float
    timestamp: float
    labels: Dict[str, str]
    source: str

class Metric:
    """Base class for all metric types."""
    def __init__(
        self,
        name: str,
        metric_type: MetricType,
        description: str,
        labels: Optional[Dict[str, str]] = None,
        retention_period: int = 3600,  # 1 hour in seconds
        alert_threshold: Optional[float] = None
    ):
        self.name = name
        self.type = metric_type
        self.description = description
        self.labels = labels or {}
        self.retention_period = retention_period
        self.alert_threshold = alert_threshold
        self.values: List[MetricValue] = []
        self._lock = threading.Lock()
        self.alert_handlers: List[callable] = []

    def add_value(self, value: float, source: str, labels: Optional[Dict[str, str]] = None) -> None:
        """Add a new value to the metric."""
        with self._lock:
            timestamp = time.time()
            metric_value = MetricValue(
                value=value,
                timestamp=timestamp,
                labels=labels or {},
                source=source
            )
            self.values.append(metric_value)
            self._cleanup_old_values()
            self._check_alerts(value)

    def _cleanup_old_values(self) -> None:
        """Remove values older than the retention period."""
        cutoff = time.time() - self.retention_period
        self.values = [v for v in self.values if v.timestamp > cutoff]

    def _check_alerts(self, value: float) -> None:
        """Check if the value exceeds alert threshold."""
        if self.alert_threshold is not None:
            if value > self.alert_threshold:
                for handler in self.alert_handlers:
                    handler(self, value)

    def get_latest_value(self) -> Optional[float]:
        """Get the most recent value."""
        with self._lock:
            return self.values[-1].value if self.values else None

    def get_statistics(self) -> Dict[str, float]:
        """Calculate basic statistics for the metric."""
        with self._lock:
            if not self.values:
                return {}
            
            values = [v.value for v in self.values]
            return {
                "min": min(values),
                "max": max(values),
                "mean": np.mean(values),
                "median": np.median(values),
                "std": np.std(values),
                "count": len(values)
            }

class Counter(Metric):
    """Counter metric that only increases."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, metric_type=MetricType.COUNTER, **kwargs)
        self._last_value = 0

    def increment(self, amount: float = 1.0, source: str = "default", labels: Optional[Dict[str, str]] = None) -> None:
        """Increment the counter."""
        with self._lock:
            self._last_value += amount
            self.add_value(self._last_value, source, labels)

class Gauge(Metric):
    """Gauge metric that can increase or decrease."""
    def set(self, value: float, source: str = "default", labels: Optional[Dict[str, str]] = None) -> None:
        """Set the gauge value."""
        self.add_value(value, source, labels)

class Histogram(Metric):
    """Histogram metric for value distributions."""
    def __init__(self, *args, buckets: List[float] = None, **kwargs):
        super().__init__(*args, metric_type=MetricType.HISTOGRAM, **kwargs)
        self.buckets = buckets or [0.1, 0.5, 1.0, 2.5, 5.0, 10.0, float('inf')]

    def observe(self, value: float, source: str = "default", labels: Optional[Dict[str, str]] = None) -> None:
        """Observe a value for the histogram."""
        self.add_value(value, source, labels)

    def get_bucket_counts(self) -> Dict[float, int]:
        """Get the count of values in each bucket."""
        with self._lock:
            counts = {bucket: 0 for bucket in self.buckets}
            for value in self.values:
                for bucket in self.buckets:
                    if value.value <= bucket:
                        counts[bucket] += 1
                        break
            return counts

class Rate(Metric):
    """Rate metric for events per time unit."""
    def __init__(self, *args, window_size: int = 60, **kwargs):
        super().__init__(*args, metric_type=MetricType.RATE, **kwargs)
        self.window_size = window_size
        self._event_times = deque(maxlen=1000)  # Store last 1000 events

    def record_event(self, source: str = "default", labels: Optional[Dict[str, str]] = None) -> None:
        """Record an event occurrence."""
        with self._lock:
            now = time.time()
            self._event_times.append(now)
            self._update_rate()

    def _update_rate(self) -> None:
        """Update the rate value based on recent events."""
        if not self._event_times:
            return

        now = time.time()
        window_start = now - self.window_size
        events_in_window = sum(1 for t in self._event_times if t >= window_start)
        rate = events_in_window / self.window_size
        self.add_value(rate, "rate_calculator", {})

class Percentage(Metric):
    """Percentage metric for ratio values."""
    def set_percentage(self, value: float, source: str = "default", labels: Optional[Dict[str, str]] = None) -> None:
        """Set a percentage value (0-100)."""
        if not 0 <= value <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        self.add_value(value, source, labels)

class MetricsCollector:
    """Main metrics collection system."""
    def __init__(self):
        self.metrics: Dict[str, Metric] = {}
        self._lock = threading.Lock()
        self._system_metrics_task: Optional[asyncio.Task] = None
        self._running = False

    def register_metric(
        self,
        name: str,
        metric_type: MetricType,
        description: str,
        labels: Optional[Dict[str, str]] = None,
        retention_period: int = 3600,
        alert_threshold: Optional[float] = None
    ) -> Metric:
        """Register a new metric."""
        with self._lock:
            if name in self.metrics:
                raise ValueError(f"Metric {name} already exists")

            metric_classes = {
                MetricType.COUNTER: Counter,
                MetricType.GAUGE: Gauge,
                MetricType.HISTOGRAM: Histogram,
                MetricType.RATE: Rate,
                MetricType.PERCENTAGE: Percentage
            }

            metric = metric_classes[metric_type](
                name=name,
                metric_type=metric_type,
                description=description,
                labels=labels,
                retention_period=retention_period,
                alert_threshold=alert_threshold
            )
            self.metrics[name] = metric
            return metric

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name."""
        return self.metrics.get(name)

    async def start(self) -> None:
        """Start the metrics collector."""
        self._running = True
        self._system_metrics_task = asyncio.create_task(self._collect_system_metrics())

    async def stop(self) -> None:
        """Stop the metrics collector."""
        self._running = False
        if self._system_metrics_task:
            self._system_metrics_task.cancel()
            try:
                await self._system_metrics_task
            except asyncio.CancelledError:
                pass

    async def _collect_system_metrics(self) -> None:
        """Collect system metrics periodically."""
        while self._running:
            try:
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                self._get_or_create_gauge("system.cpu.percent").set(cpu_percent)

                # Memory metrics
                memory = psutil.virtual_memory()
                self._get_or_create_gauge("system.memory.percent").set(memory.percent)
                self._get_or_create_gauge("system.memory.used").set(memory.used)
                self._get_or_create_gauge("system.memory.available").set(memory.available)

                # GPU metrics if available
                if torch.cuda.is_available():
                    for i in range(torch.cuda.device_count()):
                        memory_allocated = torch.cuda.memory_allocated(i)
                        memory_reserved = torch.cuda.memory_reserved(i)
                        self._get_or_create_gauge(f"system.gpu.{i}.memory.allocated").set(memory_allocated)
                        self._get_or_create_gauge(f"system.gpu.{i}.memory.reserved").set(memory_reserved)

                await asyncio.sleep(5)  # Collect every 5 seconds
            except Exception as e:
                print(f"Error collecting system metrics: {e}")
                await asyncio.sleep(1)

    def _get_or_create_gauge(self, name: str) -> Gauge:
        """Get or create a gauge metric."""
        metric = self.get_metric(name)
        if metric is None:
            metric = self.register_metric(
                name=name,
                metric_type=MetricType.GAUGE,
                description=f"System metric: {name}",
                retention_period=3600
            )
        return metric

    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics in a format suitable for external systems."""
        with self._lock:
            return {
                name: {
                    "type": metric.type.value,
                    "description": metric.description,
                    "values": [
                        {
                            "value": v.value,
                            "timestamp": v.timestamp,
                            "labels": v.labels,
                            "source": v.source
                        }
                        for v in metric.values
                    ],
                    "statistics": metric.get_statistics()
                }
                for name, metric in self.metrics.items()
            }

# Global metrics collector instance
metrics = MetricsCollector()

# Context manager for timing operations
class timing:
    """Context manager for timing operations."""
    def __init__(self, metric_name: str, labels: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.labels = labels or {}
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is not None:
            duration = time.time() - self.start_time
            metric = metrics.get_metric(self.metric_name)
            if metric is None:
                metric = metrics.register_metric(
                    name=self.metric_name,
                    metric_type=MetricType.HISTOGRAM,
                    description=f"Timing for {self.metric_name}",
                    labels=self.labels
                )
            metric.observe(duration, "timing", self.labels)

# Global metrics collector
metrics = MetricsCollector()

# Convenience functions
def record_metric(name: str, value: float, tags: Optional[Dict[str, str]] = None):
    """Record a metric value"""
    metrics.record(name, value, tags)

def increment_counter(name: str, delta: float = 1.0):
    """Increment a counter metric"""
    metrics.increment(name, delta)

def set_gauge(name: str, value: float):
    """Set a gauge metric"""
    metrics.gauge(name, value)

def timing(name: str):
    """Time an operation"""
    return metrics.timing(name)