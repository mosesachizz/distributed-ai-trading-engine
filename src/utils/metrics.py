"""
Metrics collection for performance monitoring with Prometheus integration.
"""

import time
from typing import List
import statistics
from prometheus_client import Counter, Histogram

class MetricsCollector:
    """Collects and aggregates performance metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.trade_latencies: List[float] = []
        self.error_count: int = 0
        self.trade_execution_count: int = 0
        self.trade_rejection_count: int = 0
        # Prometheus metrics
        self.trade_latency = Histogram("trade_latency_ms", "Trade execution latency in milliseconds")
        self.trade_executions = Counter("trade_executions_total", "Total number of executed trades")
        self.trade_rejections = Counter("trade_rejections_total", "Total number of rejected trades")
        self.errors = Counter("trade_errors_total", "Total number of trade errors")

    def record_trade_latency(self, latency: float):
        """Record trade execution latency.
        
        Args:
            latency (float): Latency in milliseconds.
        """
        self.trade_latencies.append(latency)
        self.trade_latency.observe(latency)

    def record_trade_execution(self):
        """Increment trade execution counter."""
        self.trade_execution_count += 1
        self.trade_executions.inc()

    def record_trade_rejection(self):
        """Increment trade rejection counter."""
        self.trade_rejection_count += 1
        self.trade_rejections.inc()

    def record_error(self):
        """Increment error counter."""
        self.error_count += 1
        self.errors.inc()

    def get_average_latency(self) -> float:
        """Calculate average trade latency.
        
        Returns:
            float: Average latency in milliseconds.
        """
        return statistics.mean(self.trade_latencies) if self.trade_latencies else 0.0

    def get_error_count(self) -> int:
        """Get total number of errors.
        
        Returns:
            int: Error count.
        """
        return self.error_count