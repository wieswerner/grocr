from django.shortcuts import render
from . import models


# Create your views here.


def boards(request):
    trello_api_token = request.COOKIES['Trello_Token']
    trello_api_key = request.COOKIES['Trello_Api_Key']

    boards = models.Board.get_boards(trello_api_key, trello_api_token)

    return render(request, "boards.html", {"boards": boards})


def board(request, id):
    trello_api_token = request.COOKIES['Trello_Token']
    trello_api_key = request.COOKIES['Trello_Api_Key']

    board = models.Board.get_board_details(
        id, trello_api_key, trello_api_token)

    return render(request, "board.html", {"board": board})


def shopping_list(request, card_ids):
    trello_api_token = request.COOKIES['Trello_Token']
    trello_api_key = request.COOKIES['Trello_Api_Key']

    shopping_list = models.Shopping_List.create(
        card_ids, trello_api_key, trello_api_token)

    return render(request, "shopping-list.html", {"shopping_list": shopping_list})


def shopping_list_ai(request, card_ids):
    trello_api_token = request.COOKIES['Trello_Token']
    trello_api_key = request.COOKIES['Trello_Api_Key']
    openai_org = request.COOKIES['Open_AI_Org']
    openai_api_key = request.COOKIES['Open_AI_Api_Key']

    shopping_list = models.Shopping_List_AI.create(
        card_ids, trello_api_key, trello_api_token, openai_org, openai_api_key)

    return render(request, "shopping-list.html", {"shopping_list": shopping_list})


def recipies(request):
    return render(request, "recipies.html")
