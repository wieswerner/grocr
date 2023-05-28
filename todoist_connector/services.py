import http.client
import json
from types import SimpleNamespace


class Api:
    def get_api_json(url):
        headers = { "Authorization": "Bearer <api>"}
        http_connection = http.client.HTTPSConnection("api.todoist.com")
        http_connection.request("GET", url, headers=headers)

        response = http_connection.getresponse().read()
        data = json.loads(response, object_hook=lambda d: SimpleNamespace(**d))
        return data
    
    def post_api_json(url, content):
        headers = { "Authorization": "Bearer <api>", "Content-Type": "application/json"}

        http_connection = http.client.HTTPSConnection("api.todoist.com")
        http_connection.request("POST", url, json.dumps(content), headers)

        response = http_connection.getresponse()
