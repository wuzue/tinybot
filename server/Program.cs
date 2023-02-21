using System.Net.Http;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);

//add cors services
builder.Services.AddCors();

var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.MapGet("/api/jokes", async context => {
  using var httpClient = new HttpClient();
  var response = await httpClient.GetAsync("https://api.chucknorris.io/jokes/random");
  response.EnsureSuccessStatusCode();
  var content = await response.Content.ReadAsStringAsync();
  var joke = JsonSerializer.Deserialize<Joke>(content, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
  await context.Response.WriteAsJsonAsync(joke);
});

//enable cors
app.UseCors(builder => builder
  .AllowAnyOrigin()
  .AllowAnyMethod()
  .AllowAnyHeader());

app.Run();

public class Joke{
  public string value { get; set; }
}