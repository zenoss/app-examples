
var express = require('express')
var StatsD = require('hot-shots')


// Read configuration from the environment.
var STATSD_HOST = process.env.STATSD_HOST
var STATSD_PORT = process.env.STATSD_PORT || 8125


// Define the key:value tags we want to send with all metrics.
var METRIC_TAGS = {
    "contextUUID": "example.node.statsd",
    "name": "NodeJS StatsD Example",
}

// Configure client to send metrics to statsd.
if (STATSD_HOST) {
    var STATSD = new StatsD({host: STATSD_HOST, port: STATSD_PORT})
} else {
    console.log("STATSD_HOST must be set")
    process.exit(1)
}

// Create the Express app
var app = express()

app.get('/', function(req, res) {
    // Increment a counter metric.
    STATSD.increment("root.requests", tags=METRIC_TAGS)
    res.send("Hello! (node_statsd)\n")
})

app.listen(5000)
