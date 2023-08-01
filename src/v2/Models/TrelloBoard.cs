using System.Text.Json.Serialization;
using Grocr.Dto;

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

    public BoardDto ToDto() => BoardDetailsDto();

    public BoardDetailsDto BoardDetailsDto()
    {
        return new BoardDetailsDto
        {
            Id = Id,
            Name = Name,
            Description = Desc,
            Closed = Closed,
            Url = Url,
            BackgroundImage = Prefs.BackgroundImageScaled.Single(p => p.Width == 1280).Url
        };
    }
}

public class Prefs
{
    [JsonPropertyName("backgroundImageScaled")]
    public List<BackgroundImage> BackgroundImageScaled { get; set; }
}