using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using Grocr.Dto;
using Grocr.Models;
using HtmlAgilityPack;

namespace Grocr.Domain;

public class OpenAi
{
    private readonly HttpClient _httpClient;
    private string ApiKey => Environment.GetEnvironmentVariable("Grocr_OpenAI_ApiKey")!;
    private const string Endpoint = "https://api.openai.com/v1/chat/completions";

    public OpenAi()
    {
        _httpClient = new HttpClient();
        _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue(
            "Bearer",
            ApiKey
        );
    }

    public async Task<IList<IngredientDto>> GetRecipesForCards(
        BoardDetailsDto board,
        string cardIds
    )
    {
        var idList = cardIds.Split(',');
        var selectedCards = board.Lists
            .SelectMany(list => list.Cards)
            .Where(card => idList.Contains(card.Id));

        var chatCompletion = new ChatCompletion();
        AddSystemMessage(chatCompletion);
        PopulateIngredients(chatCompletion, selectedCards);

        var openAiResponse = await ExecuteRequest(chatCompletion);
        var ingredients = ExtractIngredients(openAiResponse);
        return ingredients;
    }

    private async Task<OpenAiResponse> ExecuteRequest(ChatCompletion chatCompletion)
    {
        var json = JsonSerializer.Serialize(chatCompletion);

        var result = await _httpClient.PostAsync(
            Endpoint,
            new StringContent(json, Encoding.UTF8, "application/json")
        );

        var contentStream = await result.Content.ReadAsStreamAsync();
        var openAiResponse = await JsonSerializer.DeserializeAsync<OpenAiResponse>(contentStream)!;
        return openAiResponse!;
    }

    private static void PopulateIngredients(
        ChatCompletion chatCompletion,
        IEnumerable<CardDto> cards
    )
    {
        var document = new HtmlDocument();
        var stringBuilder = new StringBuilder();
        var index = 1;

        foreach (var card in cards)
        {
            stringBuilder.AppendLine($"Recipe {index++}: {card.Name}");

            document.LoadHtml(card.DescriptionHtml);
            var unorderedLists = document.DocumentNode.SelectNodes("//ul");

            if (unorderedLists == null || unorderedLists.Count == 0)
                continue;

            foreach (var ul in unorderedLists)
            {
                foreach (var li in ul.SelectNodes(".//li"))
                {
                    stringBuilder.AppendLine($"- {li.InnerText}");
                }
            }
        }

        var prompt = stringBuilder.ToString();
        chatCompletion.AddUserMessage(prompt);
    }

    private static void AddSystemMessage(ChatCompletion chatCompletion)
    {
        var systemMessage = """
        This is an recipe app that helps generate a shopping list. You're a helpful assistant. 
        You help this app by taking a list of ingredients, normalising it and combining the ingredients.
        Please combine all the ingredients from all recipes into a single list taking into consideration:

        1. If no quantity is specified assume quantity of 1.
        2. All weights and volumes should be converted to metric.
        3. Combine food ingredients where possible.
        4. Sum amounts together.
        5. Can you return only the ingredients as an unordered list.
        6. Can you separate each ingredient with a new line.
        7. Ingredients might be spelled slightly differently, combine these as well.
        """;

        chatCompletion.AddSystemMessage(systemMessage);
    }

    private static IList<IngredientDto> ExtractIngredients(OpenAiResponse openAiResponse)
    {
        var ingredients = openAiResponse.Choices[0].Message.Content
            .Split("- ")
            .Select(value => new IngredientDto { Name = value.Trim() });

        return ingredients
            .Where(ingredient => !string.IsNullOrWhiteSpace(ingredient.Name))
            .ToList();
    }
}
