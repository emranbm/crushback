import prometheus_client
from prometheus_client import Histogram

SERVER_LATENCY = Histogram(
    "crushback_server_latency",
    "The time expended at server to handle requests.",
    labelnames=("agent", "action"),
)
