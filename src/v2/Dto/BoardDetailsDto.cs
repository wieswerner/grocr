namespace Grocr.Models;

public class BoardDetailsDto : BoardDto
{
    public List<ListDto> Lists { get; set; }
}

public class ListDto
{
    public string Id { get; set; }
    public string Name { get; set; }
    public List<CardDto> Cards { get; set; }
}

public class CardDto
{
    public string Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public string DescriptionHtml { get; set; }
    public string BackgroundImage { get; set; }
}
