using System.Text.Json;
using Grocr.Models;

namespace Grocr.Domain;

public class Trello
{
    private readonly HttpClient _httpClient = new();

    private static string AppKey = "23ea7d6ca385d4df69ba5f7dbbafe09b";
    private static string UserToken =
        "ATTA2534192d45e6cd241ff3f9dd0085e173e5a432e04559496b989a631fdea621e707853A27";

    public async Task<IList<BoardDto>> GetBoards()
    {
        var json = await _httpClient.GetStreamAsync(
            $"https://api.trello.com/1/members/me/boards?key={AppKey}&token={UserToken}"
        );

        var trelloBoards = await JsonSerializer.DeserializeAsync<List<TrelloBoard>>(json);
        return trelloBoards!.Select(board => board.ToDto()).ToList();
    }

    public async Task<IList<BoardDto>> GetBoard(string id)
    {
        var json = await _httpClient.GetStreamAsync(
            $"https://api.trello.com/1/boards/{id}?key={AppKey}&token={UserToken}"
        );

        var trelloBoard = await JsonSerializer.DeserializeAsync<TrelloBoard>(json);

        return new List<BoardDto>();

        // return trelloBoards!.Select(board => board.ToDto()).ToList();
    }
}
