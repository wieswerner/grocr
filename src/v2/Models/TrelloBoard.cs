using System.Text.Json.Serialization;

namespace Grocr.Models;

public class TrelloBoard
{
    [JsonPropertyName("id")]
    public string Id { get; set; }
    
    [JsonPropertyName("name")]
    public string Name { get; set; }

    [JsonPropertyName("desc")]
    public string Desc { get; set; }
    
    [JsonPropertyName("closed")]
    public bool Closed { get; set; }
    
    [JsonPropertyName("url")]
    public string Url { get; set; }

    [JsonPropertyName("prefs")]
    public Prefs Prefs { get; set; }

    public BoardDto ToDto()
    {
        return new BoardDto
        {
            Id = Id,
            Name = Name,
            Description = Desc,
            Closed = Closed,
            Url = Url,
            BackgroundImage = Prefs.BackgroundImageScaled
                .Single(p => p.Width == 1280)
                .Url
        };
    }
}

public class Prefs
{
    [JsonPropertyName("backgroundImageScaled")]
    public List<BackgroundImage> BackgroundImageScaled { get; set; }
}

public class BackgroundImage
{
    [JsonPropertyName("width")]
    public int Width { get; set; }
    
    [JsonPropertyName("height")]
    public int Height { get; set; }
   
    [JsonPropertyName("url")]
    public string Url { get; set; }
}