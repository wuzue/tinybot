using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using System.Net.Http;
using Microsoft.AspNetCore.Cors.Infrastructure;
using DotNetEnv;
using System.Threading.Tasks;
using System.Text;
using Newtonsoft.Json.Linq;

Env.Load();

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

app.MapPost("/api/messages", async (HttpContext context) =>{
    string requestBody = await new StreamReader(context.Request.Body).ReadToEndAsync();
    var message = JObject.Parse(requestBody)["message"].ToString();

    using (var client = new HttpClient())
    {
        var request = new HttpRequestMessage(HttpMethod.Post, "http://localhost:5000/process-message");
        request.Content = new StringContent(JsonConvert.SerializeObject(new { message }), Encoding.UTF8, "application/json");

        var response = await client.SendAsync(request);
        var responseData = await response.Content.ReadAsStringAsync();
        return Results.Ok(new { response = responseData });
    }
});

await app.RunAsync();
