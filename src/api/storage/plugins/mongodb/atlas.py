import sys

sys.path.insert(0, "..")

import httpx
import json
from settings import *


class AtlasClient:
    def __init__(self, cluster_name, group_id, public_key, private_key):
        self.cluster_name = cluster_name
        self.group_id = group_id
        self.public_key = public_key
        self.private_key = private_key
        self.mappings_as_json = json.load(open("mappingsFile.json"))
        self.url = f"https://cloud.mongodb.com/api/atlas/v2/groups/{self.group_id}/clusters/{self.cluster_name}/fts/indexes?pretty=true"
        self.headers = {"Content-Type": "application/vnd.atlas.2023-01-01+json"}

    async def create_index(self):
        payload = {
            "collectionName": "string",
            "database": "string",
            "name": "string",
            "type": "vectorSearch",
            "fields": [{"property1": {}, "property2": {}}],
        }
        pass

    async def list_indexes(self):
        pass

    async def _post_request(self, data):
        async with httpx.AsyncClient() as client:
            r = await client.post(
                self.url,
                headers=self.headers,
                data=json.dumps(data),
                auth=(self.public_key, self.private_key),
            )
        return r.text
