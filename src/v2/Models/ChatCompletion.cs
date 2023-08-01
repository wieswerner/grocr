using System.Text.Json.Serialization;

namespace Grocr.Models;

public class ChatCompletion
{
    [JsonPropertyName("model")]
    public string Model { get; init; } = "gpt-4";

    [JsonPropertyName("temperature")]
    public decimal Temperature { get; set; } = 0.5m;

    [JsonPropertyName("messages")]
    public List<Message> Messages { get; } = new();

    public void AddUserMessage(string message) =>
        Messages.Add(new Message { Role = "user", Content = message });

    public void AddSystemMessage(string message) =>
        Messages.Add(new Message { Role = "system", Content = message });

    public void AddMessage(string role, string message) =>
        Messages.Add(new Message { Role = role, Content = message });
}

public class OpenAiResponse
{
    [JsonPropertyName("id")]
    public string Id { get; set; }

    [JsonPropertyName("object")]
    public string Object { get; set; }

    [JsonPropertyName("created")]
    public int Created { get; set; }

    [JsonPropertyName("model")]
    public string Model { get; set; }

    [JsonPropertyName("choices")]
    public List<Choice> Choices { get; set; }
}

public class Message
{
    [JsonPropertyName("role")]
    public string Role { get; set; }

    [JsonPropertyName("content")]
    public string Content { get; set; }
}

public class Choice
{
    [JsonPropertyName("index")]
    public int Index { get; set; }

    [JsonPropertyName("message")]
    public Message Message { get; set; }
}
