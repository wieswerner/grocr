from django.shortcuts import render
from . import models

# Create your views here.


def boards(request):
    boards = models.Board.get_boards()
    return render(request, "boards.html", {"boards": boards})


def board(request, id):
    board = models.Board.get_board_details(id)
    return render(request, "board.html", {"board": board})


def shopping_list(request, card_ids):
    shopping_list = models.Shopping_List.create(card_ids)
    return render(request, "shopping-list.html", {"shopping_list": shopping_list})


def recipies(request):
    return render(request, "recipies.html")
