package com.zenoss.example.javametrics.resources;

import com.codahale.metrics.annotation.Timed;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

@Path("/")
@Produces(MediaType.TEXT_PLAIN)
public class HelloWorldResource {

    @GET
    @Timed
    public String show() {
        return "Hello! (java-metrics)";
    }
}

