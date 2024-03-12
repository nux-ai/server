import requests
import json

apiKey = "YOUR_API_KEY_HERE"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

query = "{ boards (limit:5) {name id} }"
data = {"query": query}

r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
print(r.json())


class MondayClient:
    def __init__(self, api_key):
        self.client = monday.MondayClient(api_key)

    def get_boards(self, board_ids=[]):
        """Fetch a list of boards. Optionally, specify board IDs to fetch."""
        return self.client.boards.fetch_boards(ids=board_ids)
