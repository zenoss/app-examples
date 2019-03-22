# stdlib Imports
import os
import sys

# Third Party Imports
from flask import Flask
from statsd import StatsClient


# Read configuration from the environment.
STATSD_HOST = os.environ.get("STATSD_HOST")
STATSD_PORT = os.environ.get("STATSD_PORT", 8125)


# Define the key:value tags we want to send with all metrics.
METRIC_TAGS = {
    "contextUUID": "example.python.relationship",
    "name": "Python Relationship Example",
}

# Configure reporter to send metrics to statsd.
if STATSD_HOST:
    STATSD = StatsClient(STATSD_HOST, STATSD_PORT)
else:
    sys.exit("STATSD_HOST must be set")


# Create the Flask app.
app = Flask(__name__)


@app.route("/")
def root():
    # Increment a counter metric.
    STATSD.incr("root.requests", tags=METRIC_TAGS)
    return "Hello! (python-relationship)"


def set_relationship_tags():
    """Add relationship tags from environment."""
    sink_tags = os.environ.get("RELATIONSHIP_SINK_TAGS", "")
    for i, tag in enumerate(sink_tags.strip().split()):
        METRIC_TAGS[f'simpleCustomRelationshipSinkTag.{i}'] = tag


if __name__ == "__main__":
    set_relationship_tags()
    app.run(host="0.0.0.0")
