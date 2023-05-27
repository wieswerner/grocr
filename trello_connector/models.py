from django.db import models
from . import services
import markdown

# Create your models here.


class Board(object):
    def __init__(self, id, name, description, closed, url, backgroundImage):
        self.id = id
        self.name = name
        self.description = description
        self.closed = closed
        self.url = url
        self.backgroundImage = backgroundImage
        self.lists = []

    def get_boards():
        board_results = services.Api.get_api_json("/1/members/me/boards")
        boards = []

        for board_result in board_results:
            boards.append(Board.get_board(board_result.id))

        return boards

    def get_board(id):
        board = services.Api.get_api_json("/1/boards/" + str(id))
        return Board(board.id, board.name, board.desc, board.closed, "/trello/board/" + board.id, board.prefs.backgroundImageScaled[3].url)

    def get_board_details(id):
        board = Board.get_board(id)
        board.lists = List.get_lists(board.id)
        cards = Card.get_cards(board.id)

        for board_list in board.lists:
            board_list.cards = [
                card for card in cards if card.list_id == board_list.id]

        return board


class List(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.cards = []

    def get_lists(board_id):
        list_results = services.Api.get_api_json(
            "/1/boards/" + str(board_id) + "/lists")
        lists = []

        for list_result in list_results:
            lists.append(List(list_result.id, list_result.name))

        return lists


class Card(object):
    def __init__(self, id, list_id, name, description):
        self.id = id
        self.list_id = list_id
        self.name = name
        self.description = description
        self.html = markdown.markdown(description)

    def get_cards(board_id):
        card_results = services.Api.get_api_json(
            "/1/boards/" + str(board_id) + "/cards")
        cards = []

        for card_result in card_results:
            cards.append(Card(card_result.id, card_result.idList,
                         card_result.name, card_result.desc))

        return cards
