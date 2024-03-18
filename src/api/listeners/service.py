from fastapi import HTTPException
from db_internal.service import BaseAsyncDBService

from utilities.internal_requests import AsyncHttpClient

from config import listener_url


class ListenerAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("listeners", index_id)
        self.listener_url = listener_url

    def init_client(self, api_key):
        self.http_client = AsyncHttpClient(
            url=self.listener_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    async def create_listener(self, connection_info):
        try:
            return await self.http_client.post(connection_info)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_listener_status(self, connection_info):
        pass
