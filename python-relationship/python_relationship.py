# stdlib Imports
import itertools
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


def get_env_relationship_tags():
    """Generate relationship tags from ad hoc environment."""
    tags = os.environ.get("RELATIONSHIP_SINK_TAGS", "")
    for tag in tags.split():
        tag = tag.strip()
        if tag:
            yield tag


def get_kubernetes_relationship_tags():
    """Generate relationship tags from Kubernetes environment."""
    cluster = os.environ.get("KUBERNETES_CLUSTER", "")
    namespace = os.environ.get("KUBERNETES_NAMESPACE", "")
    pod = os.environ.get("KUBERNETES_POD", "")
    container = os.environ.get("KUBERNETES_CONTAINER", "")

    if cluster and namespace and pod:
        # Create a relationship to the associated pod.
        yield "kubernetesPod.{}.{}.{}".format(cluster, namespace, pod)

        if container:
            # Create a relationship to the associated container.
            yield "kubernetesContainer.{}.{}.{}.{}".format(
                cluster, namespace, pod, container)


def set_relationship_tags(tags):
    """Add relationship tags."""
    global METRIC_TAGS

    for i, tag in enumerate(tags):
        METRIC_TAGS[f'simpleCustomRelationshipSinkTag.{i}'] = tag


if __name__ == "__main__":
    set_relationship_tags(
        itertools.chain(
            get_env_relationship_tags(),
            get_kubernetes_relationship_tags()))

    print("Adding the following tags to all metrics:")
    from pprint import pprint
    pprint(METRIC_TAGS)

    app.run(host="0.0.0.0")
