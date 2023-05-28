from django.db import models
from bs4 import BeautifulSoup
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
            cards.append(Card.create_card(card_result))

        return cards

    def get_card(id):
        card_result = services.Api.get_api_json("/1/cards/" + str(id))
        return Card.create_card(card_result)

    def create_card(json):
        return Card(json.id, json.idList,  json.name, json.desc)


class Shopping_List(object):
    def __init__(self, cards, ingredients):
        self.cards = cards
        self.ingredients = ingredients

    def create(card_ids):
        id_list = str(card_ids).split(",")
        card_names = []
        ingredients = []

        for card_id in id_list:
            card = Card.get_card(card_id)
            card_names.append(card.name)

            ingredients += Shopping_List.get_ingredients(card)

        combined_ingredients = Shopping_List.combine_ingredients(ingredients)
        return Shopping_List(card_names, combined_ingredients)

    def get_ingredients(card):
        soup = BeautifulSoup(card.html, "html.parser")
        ul = soup.find("ul")
        ingredients = []

        for li in ul.find_all("li"):
            ingredients.append(li.string)

        return ingredients

    def combine_ingredients(ingredients):
        combined_ingredients = {}
        
        for ingredient in ingredients:
            text_amount = "1"

            if "(" and ")" in ingredient:
                text_amount = ingredient[ingredient.index("(") + 1:ingredient.rindex(")")]

            amount = float(text_amount)
            name = ingredient.replace(f"({text_amount})", "").strip()

            if name in combined_ingredients:
                amount += float(combined_ingredients[name])
            
            combined_ingredients[name] = amount

        return Shopping_List.flatten_dictionary(combined_ingredients)
    
    def flatten_dictionary(dictionary):
        list = []
        for key, value in dictionary.items():
            list.append(f"{round(value)}x {key}")

        return list
