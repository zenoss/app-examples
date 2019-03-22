package com.zenoss.example.javametrics;

import com.google.common.base.Joiner;
import com.readytalk.metrics.StatsDReporter;
import com.zenoss.example.javametrics.health.DummyHealthCheck;
import com.zenoss.example.javametrics.resources.HelloWorldResource;
import io.dropwizard.Application;
import io.dropwizard.setup.Environment;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class JavaMetricsApplication extends Application<JavaMetricsConfiguration> {

    public static void main(final String[] args) throws Exception {
        new JavaMetricsApplication().run(args);
    }

    @Override
    public String getName() {
        return "JavaMetrics";
    }

    @Override
    public void run(final JavaMetricsConfiguration configuration,
                    final Environment environment) {

        startStatsd(configuration, environment);

        environment.healthChecks().register("dummy", new DummyHealthCheck());
        environment.jersey().register(new HelloWorldResource());
    }

    public void startStatsd(final JavaMetricsConfiguration configuration,
                            final Environment environment) {
        String statsdHost = System.getenv("STATSD_HOST");
        if (statsdHost == null) {
            return;
        }

        Map<String, String> metricTags = configuration.getstatsDMetricTags();
        String tagString = "," + Joiner.on(",").withKeyValueSeparator("=").join(metricTags);

        StatsDReporter.forRegistry(environment.metrics())
            .suffixedWith(tagString)
            .build(statsdHost, 8125)
            .start(10, TimeUnit.SECONDS);
    }
}
