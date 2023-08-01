using System.Text.Json.Serialization;
using Grocr.Dto;
using Markdig;

namespace Grocr.Models;

public class TrelloCard
{
    [JsonPropertyName("id")]
    public string Id { get; set; }

    [JsonPropertyName("idList")]
    public string ListId { get; set; }

    [JsonPropertyName("name")]
    public string Name { get; set; }

    [JsonPropertyName("desc")]
    public string Desc { get; set; }

    [JsonPropertyName("cover")]
    public Cover Cover { get; set; }

    public CardDto ToDto()
    {
        return new CardDto
        {
            Id = Id,
            Name = Name,
            Description = Desc,
            DescriptionHtml = Markdown.ToHtml(Desc),
            BackgroundImage = Cover.Scaled?.Single(p => p.Width == 1280).Url,
        };
    }
}

public class Cover
{
    [JsonPropertyName("scaled")]
    public List<BackgroundImage>? Scaled { get; set; }
}
