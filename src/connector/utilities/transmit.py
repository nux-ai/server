import aiohttp
import asyncio


class Sender:
    def __init__(self, endpoint, headers=None, max_pending=100):
        self.endpoint = endpoint
        self.headers = headers or {}
        self.queue = asyncio.Queue(max_pending)
        self.task = asyncio.create_task(self._worker())

    async def send(self, payload):
        await self.queue.put(payload)

    async def _worker(self):
        async with aiohttp.ClientSession() as session:
            while True:
                payload = await self.queue.get()
                async with session.post(
                    self.endpoint, json=payload, headers=self.headers
                ) as response:
                    print(await response.text())
                self.queue.task_done()


# Usage
headers = {"Authorization": "Bearer your_token"}
sender = Sender("http://example.com/api", headers=headers)
asyncio.run(sender.send({"key": "value"}))
