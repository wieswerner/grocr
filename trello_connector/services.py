import http.client
import json
from types import SimpleNamespace


class Api:
    def get_api_json(url):
        trello_key = "<key>"
        trello_token = "<token>"
        full_url = url + "?key=" + trello_key + "&token=" + trello_token

        http_connection = http.client.HTTPSConnection("api.trello.com")
        http_connection.request("GET", full_url)

        response = http_connection.getresponse().read()
        data = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
        return data
