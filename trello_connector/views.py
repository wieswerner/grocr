from django.shortcuts import render
from django.http import HttpResponse

import http.client
import json
from . import models
from types import SimpleNamespace

# Create your views here.
def api_boards(request):
    boards = get_boards()
    return render(request, "boards.html", {"boards" : boards})

def api_board(request, id):
    board = get_board_details(id)
    return render(request, "board.html", {"board" : board})

def get_boards():
    board_results = get_api_json("/1/members/me/boards")
    boards = []

    for board_result in board_results:
        board = get_board_details(board_result.id)
        boards.append(board)
            
    return boards

def get_board_details(id):
    board = get_api_json("/1/boards/" + str(id))
    return Board(board.id, board.name, board.desc, board.closed, "/trello/board/" + board.id, board.prefs.backgroundImageScaled[3].url)

def get_api_json(url):
    trello_token = "<your trello token>"
    trello_key = "<your trello key>"
    full_url = url + "?key=" + trello_key + "&token=" + trello_token

    http_connection = http.client.HTTPSConnection("api.trello.com")
    http_connection.request("GET", full_url)
    
    response = http_connection.getresponse().read()
    data = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
    return data

def recipies(request):
    return render(request, "recipies.html")

class Board(object):
    def __init__(self, id, name, description, closed, url, backgroundImage):
        self.id = id
        self.name = name
        self.description = description
        self.closed = closed
        self.url = url
        self.backgroundImage = backgroundImage
