package main

import (
	"fmt"
	"net"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gorilla/handlers"
	statsd "github.com/pubnub/go-metrics-statsd"
	metrics "github.com/rcrowley/go-metrics"
)

// Define the tags we want to send with all metrics.
var metricTags = map[string]string{
	"app":  "example.go.metrics",
	"name": "Go Metrics Example",
}

func main() {
	// Register metrics.
	requests := metrics.NewCounter()
	registerMetric("root.requests", requests)

	// Start reporting metrics to statsd.
	startStatsd()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		requests.Inc(1)
		fmt.Fprintf(w, "Hello! (go-metrics)")
	})

	http.ListenAndServe(
		":5000",
		handlers.LoggingHandler(os.Stdout, http.DefaultServeMux))
}

// Register a metric with metricTags defined above.
func registerMetric(name string, i interface{}) {
	pairs := make([]string, len(metricTags))
	for k, v := range metricTags {
		pairs = append(pairs, fmt.Sprintf("%s=%s", k, v))
	}
	metrics.Register(fmt.Sprintf("%s,%s", name, strings.Join(pairs, ",")), i)
}

// Start reporting metrics to statsd.
func startStatsd() {
	statsdHost := os.Getenv("STATSD_HOST")
	if statsdHost == "" {
		return
	}

	statsdAddr, err := net.ResolveUDPAddr("udp", net.JoinHostPort(statsdHost, "8125"))
	if err != nil {
		panic(err.Error())
	}

	if statsdHost != "" {
		go statsd.StatsD(metrics.DefaultRegistry, 1*time.Minute, "", statsdAddr)
	}
}
