from django.db import models
from . import services

# Create your models here.


class Board(object):
    def __init__(self, id, name, description, closed, url, backgroundImage):
        self.id = id
        self.name = name
        self.description = description
        self.closed = closed
        self.url = url
        self.backgroundImage = backgroundImage

    def get_boards():
        board_results = services.Api.get_api_json("/1/members/me/boards")
        boards = []

        for board_result in board_results:
            board = Board.get_board_details(board_result.id)
            boards.append(board)

        return boards

    def get_board_details(id):
        board = services.Api.get_api_json("/1/boards/" + str(id))
        return Board(board.id, board.name, board.desc, board.closed, "/trello/board/" + board.id, board.prefs.backgroundImageScaled[3].url)


class List(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_lists(board_id):
        list_results = services.Api.get_api_json("/1/boards/" + str(board_id) + "/lists")
        lists = []

        for list_result in list_results:
            lists.append(List(list_result.id, list_result.name))

        return lists
