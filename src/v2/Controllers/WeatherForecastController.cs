using Grocr.Domain;
using Grocr.Dto;
using Grocr.Models;
using Microsoft.AspNetCore.Mvc;

namespace Grocr.Controllers;

[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    private static readonly string[] Summaries = new[]
    {
        "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
    };

    private readonly ILogger<WeatherForecastController> _logger;
    private readonly Trello _trello;

    public WeatherForecastController(ILogger<WeatherForecastController> logger, Trello trello)
    {
        _logger = logger;
        _trello = trello;
    }

    [HttpGet]
    public IEnumerable<WeatherForecast> Get()
    {
        return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
                TemperatureC = Random.Shared.Next(-20, 55),
                Summary = Summaries[Random.Shared.Next(Summaries.Length)]
            })
            .ToArray();
    }
    
    [HttpPost]
    public async Task<IEnumerable<BoardDto>> Post()
    {
        var boards = await _trello.GetBoards();
        return boards;
    }
}