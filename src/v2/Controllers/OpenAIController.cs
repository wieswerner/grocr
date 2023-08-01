using Grocr.Domain;
using Grocr.Dto;
using Microsoft.AspNetCore.Mvc;

namespace Grocr.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OpenAiController : ControllerBase
{
    private readonly ILogger<OpenAiController> _logger;
    private readonly Trello _trello;
    private readonly OpenAi _openAi;

    public OpenAiController(ILogger<OpenAiController> logger, Trello trello, OpenAi openAi)
    {
        _logger = logger;
        _trello = trello;
        _openAi = openAi;
    }

    [HttpGet]
    [Route("boards/{id}/ingredients")]
    public async Task<IEnumerable<IngredientDto>> Boards(string id, [FromQuery] string ids)
    {
        _logger.LogInformation("Getting Trello Board {Id}", id);
        var board = await _trello.GetBoard(id);

        var ingredients = await _openAi.GetRecipesForCards(board, ids);
        return ingredients;
    }

    [HttpGet]
    [Route("boards/{id}")]
    public async Task<BoardDto> Board(string id)
    {
        _logger.LogInformation("Getting Trello Board {Id}", id);
        var board = await _trello.GetBoard(id);

        _logger.LogInformation("Got Trello Board with id {Id}", board.Id);
        return board;
    }
}
