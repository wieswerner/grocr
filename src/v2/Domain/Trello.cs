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

        var boards = await JsonSerializer.DeserializeAsync<List<TrelloBoard>>(json);
        return boards!.Select(board => board.ToDto()).ToList();
    }

    public async Task<BoardDto> GetBoard(string id)
    {
        var json = await _httpClient.GetStreamAsync(
            $"https://api.trello.com/1/boards/{id}?key={AppKey}&token={UserToken}"
        );

        var board = await JsonSerializer.DeserializeAsync<TrelloBoard>(json);
        var boardLists = await GetBoardLists(id);
        var boardCards = await GetBoardCards(id);

        var boardDto = board!.BoardDetailsDto();
        boardDto.Lists = boardLists.Select(list => list.ToDto()).ToList();

        foreach (var list in boardDto.Lists)
        {
            list.Cards = boardCards
                .Where(card => card.ListId == list.Id)
                .Select(card => card.ToDto())
                .ToList();
        }

        return boardDto;
    }

    private async Task<IList<TrelloList>> GetBoardLists(string boardId)
    {
        var json = await _httpClient.GetStreamAsync(
            $"https://api.trello.com/1/boards/{boardId}/lists?key={AppKey}&token={UserToken}"
        );

        var lists = await JsonSerializer.DeserializeAsync<List<TrelloList>>(json);
        return lists!;
    }

    private async Task<IList<TrelloCard>> GetBoardCards(string boardId)
    {
        var json = await _httpClient.GetStreamAsync(
            $"https://api.trello.com/1/boards/{boardId}/cards?key={AppKey}&token={UserToken}"
        );

        var lists = await JsonSerializer.DeserializeAsync<List<TrelloCard>>(json);
        return lists!;
    }
}
