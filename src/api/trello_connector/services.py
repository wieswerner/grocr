import http.client
import json
from types import SimpleNamespace

class Api:
    def get_api_json(url, trello_api_key, trello_api_token):
        full_url = url + f"?key={trello_api_key}&token={trello_api_token}"

        http_connection = http.client.HTTPSConnection("api.trello.com")
        http_connection.request("GET", full_url)

        response = http_connection.getresponse()
        data = json.loads(
            response.read(), object_hook=lambda d: SimpleNamespace(**d))
        return data
