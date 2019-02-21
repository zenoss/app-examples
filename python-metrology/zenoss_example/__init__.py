# stdlib Imports
import os

# Third Party Imports
from flask import Flask
from metrology import Metrology


# Read configuration from the environment.
STATSD_HOST = os.environ.get("STATSD_HOST", None)
STATSD_PORT = os.environ.get("STATSD_PORT", 8125)
STATSD_INTERVAL = os.environ.get("STATSD_INTERVAL", 60)


def join_tags(tags):
    """Return a concatenated tags string given a dict."""
    return ",".join("=".join(x) for x in tags.items())


# Define the key:value tags we want to send with all metrics.
METRIC_TAGS = join_tags({
    "contextUUID": "example.python.metrology",
    "meta_type": "com.zenoss.example.python.metrology",
    "name": "Python Metrology Example",
})


def register_metrics(metric_definitions):
    """Register the given metrics."""
    metrics = {}
    for name, type_ in metric_definitions.items():
        metrics[name] = type_(",".join((name, METRIC_TAGS)))
    return metrics


# Register the metrics we intend to update and send.
METRICS = register_metrics({
    "root.requests": Metrology.counter,
})

# Configure reporter to send metrics to statsd.
if STATSD_HOST:
    from metrology.reporter.statsd import StatsDReporter
    reporter = StatsDReporter(
        host=STATSD_HOST,
        port=int(STATSD_PORT),
        interval=int(STATSD_INTERVAL))

    reporter.start()


# Create the Flask app.
app = Flask(__name__)


@app.route("/")
def root():
    # Update a pre-registered metric.
    METRICS["root.requests"].increment()
    return "Hello! (python-metrology)"
