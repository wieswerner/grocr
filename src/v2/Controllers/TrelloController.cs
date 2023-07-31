using Grocr.Domain;
using Grocr.Models;
using Microsoft.AspNetCore.Mvc;

namespace Grocr.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TrelloController : ControllerBase
{
    private readonly ILogger<TrelloController> _logger;
    private readonly Trello _trello;

    public TrelloController(ILogger<TrelloController> logger, Trello trello)
    {
        _logger = logger;
        _trello = trello;
    }

    [HttpGet]
    [Route("boards")]
    public async Task<IEnumerable<BoardDto>> Boards()
    {
        _logger.LogInformation("Getting Trello Boards");
        var boards = await _trello.GetBoards();

        _logger.LogInformation("Got {Count} Trello Boards", boards.Count);
        return boards;
    }

    [HttpGet]
    [Route("boards/{id}")]
    public async Task<IEnumerable<BoardDto>> Board(string id)
    {
        _logger.LogInformation("Getting Trello Board {Id}", id);
        var boards = await _trello.GetBoard(id);

        _logger.LogInformation("Got {Count} Trello Boards", boards.Count);
        return boards;
    }
}
