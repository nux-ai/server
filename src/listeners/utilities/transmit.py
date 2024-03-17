import httpx
from queue import Queue
from threading import Thread


class Sender:
    def __init__(self, endpoint, headers=None, max_pending=100):
        self.endpoint = endpoint
        self.headers = headers or {}
        self.queue = Queue(max_pending)
        self.thread = Thread(target=self._worker, daemon=True)
        self.thread.start()

    def send(self, payload):
        self.queue.put(payload)

    def _worker(self):
        with httpx.Client() as client:
            while True:
                payload = self.queue.get()
                response = client.post(
                    self.endpoint, json=payload, headers=self.headers
                )
                print(response.text)
                self.queue.task_done()
