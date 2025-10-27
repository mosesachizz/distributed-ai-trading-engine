"""
REST API for system monitoring and health checks with Prometheus metrics.
"""

from fastapi import FastAPI
from prometheus_client import make_wsgi_app, Counter, Histogram
from starlette.middleware.wsgi import WSGIMiddleware
from ..utils.logger import setup_logger
from ..utils.metrics import MetricsCollector

app = FastAPI(title="Trading Engine Monitoring API")
logger = setup_logger(__name__)
metrics = MetricsCollector()

# Prometheus metrics
trade_latency = Histogram("trade_latency_ms", "Trade execution latency in milliseconds")
trade_executions = Counter("trade_executions_total", "Total number of executed trades")
trade_rejections = Counter("trade_rejections_total", "Total number of rejected trades")
errors = Counter("trade_errors_total", "Total number of trade errors")

# Mount Prometheus metrics endpoint
app.mount("/metrics", WSGIMiddleware(make_wsgi_app()))

@app.get("/health")
async def health_check() -> dict:
    """Check the health of the trading engine.
    
    Returns:
        dict: Health status and metrics.
    """
    try:
        status = {
            "status": "healthy",
            "trade_latency_avg_ms": metrics.get_average_latency(),
            "error_count": metrics.get_error_count()
        }
        logger.info("Health check: %s", status)
        return status
    except Exception as e:
        logger.error("Health check failed: %s", str(e))
        return {"status": "unhealthy", "error": str(e)}