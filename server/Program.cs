using System;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Newtonsoft.Json;

namespace YourNamespace
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            builder.Services.AddHttpClient();

            var app = builder.Build();

            app.MapGet("/weather", async context =>
            {
                var cityName = context.Request.Query["message"];

                if (!string.IsNullOrEmpty(cityName))
                {
                    var httpClient = context.RequestServices.GetService<HttpClient>();
                    var url = $"http://api.weatherapi.com/v1/current.json?key=aa2bd92bba6f4e0c9bb103249232202&q={cityName}&aqi=no";
                    var response = await httpClient.GetAsync(url);
                    var responseContent = await response.Content.ReadAsStringAsync();
                    dynamic weatherData = JsonConvert.DeserializeObject(responseContent);
                    var regionName = weatherData.location.region;
                    var getCountry = weatherData.location.country;
                    var temperature = weatherData.current.temp_c;

                    await context.Response.WriteAsync($"The temperature in {cityName} - {regionName}, {getCountry} is {temperature}°C.");
                }
                else
                {
                    await context.Response.WriteAsync("Please provide a valid message.");
                }
            });

            await app.RunAsync();
        }
    }
}