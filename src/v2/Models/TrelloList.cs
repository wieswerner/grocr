using System.Text.Json.Serialization;
using Grocr.Dto;

namespace Grocr.Models;

public class TrelloList
{
    [JsonPropertyName("id")]
    public string Id { get; set; }

    [JsonPropertyName("name")]
    public string Name { get; set; }

    public ListDto ToDto()
    {
        return new ListDto { Id = Id, Name = Name };
    }
}
