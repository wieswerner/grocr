from django.shortcuts import render
from . import models

# Create your views here.


def boards(request):
    boards = models.Board.get_boards()
    return render(request, "boards.html", {"boards": boards})


def board(request, id):
    board = models.Board.get_board_details(id)
    lists = models.List.get_lists(id)
    return render(request, "board.html", {"board": board, "lists": lists})


def recipies(request):
    return render(request, "recipies.html")
