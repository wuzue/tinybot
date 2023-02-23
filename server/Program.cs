using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using System.Net.Http;
using Microsoft.AspNetCore.Cors.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

// Add CORS policy to allow all origins, methods and headers
var corsPolicy = new CorsPolicyBuilder()
    .AllowAnyOrigin()
    .AllowAnyMethod()
    .AllowAnyHeader()
    .Build();

builder.Services.AddCors(options =>
{
    options.AddPolicy("CorsPolicy", corsPolicy);
});

builder.Services.AddHttpClient();

var app = builder.Build();

// Enable CORS for the "/weather" endpoint
app.UseCors("CorsPolicy");

app.MapGet("/weather", async context =>
{
    var cityName = context.Request.Query["message"];

    if (!string.IsNullOrEmpty(cityName))
    {
        var httpClient = context.RequestServices.GetService<HttpClient>();
        var url = $"http://api.weatherapi.com/v1/current.json?key=API&q={cityName}&aqi=no";
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
