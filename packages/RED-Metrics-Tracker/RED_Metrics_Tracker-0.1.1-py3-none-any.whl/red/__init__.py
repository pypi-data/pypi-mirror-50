"""RED Metrics tracker able to instrument flask views using prometheus metrics."""
from red.blueprint import metrics_blueprint
from red.metrics import HTTP_EXCEPTIONS_TOTAL, HTTP_REQUESTS_LATENCY, HTTP_REQUESTS_TOTAL
from red.tracker import REDMetricsTracker

__all__ = [
    "REDMetricsTracker",
    "metrics_blueprint",
    "HTTP_REQUESTS_TOTAL",
    "HTTP_EXCEPTIONS_TOTAL",
    "HTTP_REQUESTS_LATENCY",
]

__version__ = "0.1.1"
