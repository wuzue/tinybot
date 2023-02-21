using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

public static class ChuckNorrisApi{
  private static readonly HttpClient _httpClient = new HttpClient();
  public static async Task<string> GetRandomFact(){
    var response = await _httpClient.GetAsync("https://api.chucknorris.io/jokes/random");
    response.EnsureSuccessStatusCode();

    var content = await response.Content.ReadAsStringAsync();
    var json = JsonDocument.Parse(content);
    var fact = json.RootElement.GetProperty("value").GetString();

    return fact;
  }
}