from django.db import models
from bs4 import BeautifulSoup
from . import services
from openai_connector.services import OpenAiApi

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

    def get_boards(trello_api_key, trello_api_token):
        board_results = services.Api.get_api_json(
            "/1/members/me/boards", trello_api_key, trello_api_token)
        boards = []

        for board_result in board_results:
            boards.append(Board.get_board(board_result.id,
                          trello_api_key, trello_api_token))

        return boards

    def get_board(id, trello_api_key, trello_api_token):
        board = services.Api.get_api_json(
            f"/1/boards/{id}", trello_api_key, trello_api_token)
        return Board(board.id, board.name, board.desc, board.closed, "/trello/board/" + board.id, board.prefs.backgroundImageScaled[3].url)

    def get_board_details(id, trello_api_key, trello_api_token):
        board = Board.get_board(id, trello_api_key, trello_api_token)
        board.lists = List.get_lists(
            board.id, trello_api_key, trello_api_token)
        cards = Card.get_cards(board.id, trello_api_key, trello_api_token)

        for board_list in board.lists:
            board_list.cards = [
                card for card in cards if card.list_id == board_list.id]

        return board


class List(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.cards = []

    def get_lists(board_id, trello_api_key, trello_api_token):
        list_results = services.Api.get_api_json(
            f"/1/boards/{board_id}/lists", trello_api_key, trello_api_token)
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

    def get_cards(board_id, trello_api_key, trello_api_token):
        card_results = services.Api.get_api_json(
            f"/1/boards/{board_id}/cards", trello_api_key, trello_api_token)
        cards = []

        for card_result in card_results:
            cards.append(Card.create_card(card_result))

        return cards

    def get_card(id, trello_api_key, trello_api_token):
        card_result = services.Api.get_api_json(
            f"/1/cards/{id}", trello_api_key, trello_api_token)
        return Card.create_card(card_result)

    def create_card(json):
        return Card(json.id, json.idList,  json.name, json.desc)


class Shopping_List(object):
    def __init__(self, cards, ingredients):
        self.cards = cards
        self.ingredients = ingredients

    def create(card_ids, trello_api_key, trello_api_token):
        id_list = str(card_ids).split(",")
        card_names = []
        ingredients = []

        for card_id in id_list:
            card = Card.get_card(card_id, trello_api_key, trello_api_token)
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
                text_amount = ingredient[ingredient.index(
                    "(") + 1:ingredient.rindex(")")]

            amount = float(text_amount)
            name = ingredient.replace(f"({text_amount})", "").strip()

            if name in combined_ingredients:
                amount += float(combined_ingredients[name])

            combined_ingredients[name] = amount

        return Shopping_List.flatten_dictionary(combined_ingredients)

    def flatten_dictionary(dictionary):
        keys = sorted(list(dictionary.keys()), key=str.casefold)

        ingredients = []
        for key in keys:
            ingredients.append(f"{round(dictionary[key])}x {key}")

        return ingredients


class Shopping_List_AI(object):
    def __init__(self, cards, ingredients):
        self.cards = cards
        self.ingredients = ingredients

    def create(card_ids, trello_api_key, trello_api_token, openai_org, openai_api_key):
        id_list = str(card_ids).split(",")
        card_names = []
        ingredients = {}

        for card_id in id_list:
            card = Card.get_card(card_id, trello_api_key, trello_api_token)
            card_names.append(card.name)

            ingredients[card.name] = Shopping_List_AI.get_ingredients(card)

        combined_ingredients = Shopping_List_AI.combine_ingredients(
            ingredients, openai_org, openai_api_key)
        return Shopping_List_AI(card_names, combined_ingredients)

    def get_ingredients(card):
        soup = BeautifulSoup(card.html, "html.parser")
        uls = soup.find_all("ul")
        ingredients = []

        for ul in uls: 
            for li in ul.find_all("li"):
                ingredients.append(li.string)

        return ingredients

    def combine_ingredients(ingredients, openai_org, openai_api_key):
        ingredient_input = ""
        for key in ingredients:
            ingredient_input += f"{key}\n"
            for ingredient in ingredients[key]:
                ingredient_input += f"- {ingredient}\n"

        input = f"""
        This is an recipe app that helps generate a shopping list. You're a helpful assistant. 
        You help this app by taking a list of ingredients, normalising it and combining the ingredients.
        Please combine all the ingredients from all recipes into a single list taking into consideration: 
        1. If no quantity is specified assume quantity of 1.
        2. All weights and volumes should be converted to metric.
        3. Combine food ingredients where possible.
        4. Sum amounts together.
        5. Can you return only the ingredients as an unordered list.
        6. Can you seperate each ingredient with a new line.
        7. Ingredients might be spelled slightly differntly, combine these as well.\n\n

        Ingredients: {ingredient_input}
        """

        ai_result = OpenAiApi.ask_open_ai(input, openai_org, openai_api_key)
        
        if ai_result.count('\n') > 1:
            ai_result = ai_result.split("\n")
        elif ai_result.count(',') > 1:
            ai_result = ai_result.split(",")

        combined_ingredients = []

        for ingredient in ai_result:
            if len(ingredient) > 0 and not ingredient.startswith("Note") and not ingredient.startswith("(Note") and not ingredient.endswith(":"):
                combined_ingredients.append(ingredient.strip())

        combined_ingredients.sort()
        return combined_ingredients
