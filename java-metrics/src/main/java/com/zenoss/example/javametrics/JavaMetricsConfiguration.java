package com.zenoss.example.javametrics;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.dropwizard.Configuration;
import java.util.Collections;
import java.util.Map;
import javax.validation.constraints.NotNull;

public class JavaMetricsConfiguration extends Configuration {

    @NotNull
    private Map<String, String> statsDMetricTags = Collections.emptyMap();

    @JsonProperty("statsDMetricTags")
    public Map<String, String> getstatsDMetricTags() {
        return statsDMetricTags;
    }

    @JsonProperty("statsDMetricTags")
    public void setstatsDMetricTags(Map<String, String> statsDMetricTags) {
        this.statsDMetricTags = statsDMetricTags;
    }
}
