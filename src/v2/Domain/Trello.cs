using System.Text.Json;
using Grocr.Dto;
using Grocr.Models;

namespace Grocr.Domain;

public class Trello
{
    private readonly HttpClient _httpClient = new();

    private string AppKey => Environment.GetEnvironmentVariable("Grocr_Trello_AppKey")!;
    private static string UserToken =>
        Environment.GetEnvironmentVariable("Grocr_Trello_UserToken")!;

    public async Task<IList<BoardDto>> GetBoards()
    {
        var json = await _httpClient.GetStreamAsync(
            $"https://api.trello.com/1/members/me/boards?key={AppKey}&token={UserToken}"
        );

        var boards = await JsonSerializer.DeserializeAsync<List<TrelloBoard>>(json);
        return boards!.Select(board => board.ToDto()).ToList();
    }

    public async Task<BoardDetailsDto> GetBoard(string id)
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
