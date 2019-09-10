using System;
using System.IO;
using System.Linq;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;

using JustEat.StatsD;
using System.Collections.Generic;
using Microsoft.Extensions.Logging;

namespace dotnet_statsd
{
    static class Metrics
    {
        private static Dictionary<string, string> MetricTags = new Dictionary<string, string>() {
            ["app"] = "example.dotnet.statsd",
            ["name"] = ".NET StatsD Example",
        };

        /// Name returns basename with MetricTags appended.
        public static string Name(string basename) =>
            String.Format("{0},{1}", basename, String.Join(",",
                MetricTags.Select(
                    x => string.Format("{0}={1}", x.Key, x.Value))));
    }

    public class Program
    {
        public static void Main(string[] args) =>
            CreateWebHostBuilder(args).Build().Run();

        public static IWebHostBuilder CreateWebHostBuilder(string[] args) =>
            WebHost.CreateDefaultBuilder(args)
                .ConfigureServices(serviceCollection =>
                    serviceCollection.AddStatsD(
                        Environment.GetEnvironmentVariable("STATSD_HOST")))
                .UseUrls("http://0.0.0.0:5000")
                .UseStartup<Startup>();
    }

    public class Startup
    {
        private IStatsDPublisher stats;

        public Startup(IStatsDPublisher statsDPublisher)
        {
            stats = statsDPublisher;
        }

        public void Configure(IApplicationBuilder app, ILoggerFactory loggerFactory)
        {
            loggerFactory.AddConsole();

            app.Run(async (context) =>
            {
                stats.Increment(Metrics.Name("root.requests"));
                await context.Response.WriteAsync("Hello! (dotnet-statsd)");
            });
        }
    }
}
