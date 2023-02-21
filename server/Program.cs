var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.MapPost("/api/messages", async context => {
    await context.Response.WriteAsync("Message received!");
});

app.Run();
