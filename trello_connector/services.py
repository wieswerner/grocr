import http.client
import json
from types import SimpleNamespace


class Api:
    def get_api_json(url):
        trello_key = "ea61c22a90bf9afbacbdb0ef6d869401"
        trello_token = "ATTA6264207f0306380a59c7f5564251d07e20a49932eac327dd45811d56b0c99cd0BB871AC9"
        full_url = url + "?key=" + trello_key + "&token=" + trello_token

        http_connection = http.client.HTTPSConnection("api.trello.com")
        http_connection.request("GET", full_url)

        response = http_connection.getresponse().read()
        data = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
        return data
