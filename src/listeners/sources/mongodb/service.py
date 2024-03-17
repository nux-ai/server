from fastapi import HTTPException
import asyncio
from threading import Thread, Event
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
import time

from utilities.transmit import Sender


class MongoDBConnection:
    def __init__(self, uri, db):
        self.uri = uri
        self.db = db


class MongoDBService:
    def __init__(self, connection_info: MongoDBConnection):
        self.uri = connection_info.uri
        self.db_name = connection_info.db
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        self.sender = Sender(
            endpoint="https://localhost:8000/receive",
            headers={"Authorization": "Bearer YOUR_NUX_API_KEY"},
        )
        self.listeners = {}  # Dictionary to track listener threads
        self.stop_events = {}  # Track stop events for each thread

    def close(self):
        for collection_name in list(self.listeners.keys()):
            self.stop_notifier(collection_name)

    def stop_notifier(self, collection_name):
        if collection_name in self.listeners:
            print(f"Stopping listener for {collection_name}.")
            self.stop_events[collection_name].set()  # Signal the thread to stop
            self.listeners[collection_name].join()  # Wait for the thread to finish
            del self.listeners[collection_name]  # Remove the thread from the registry
            del self.stop_events[collection_name]  # Remove the event from the registry
        else:
            print(f"No active listener for {collection_name} to stop.")

    def invoke_notifier(self, collection_name):
        print(f"Invoking notifier for {collection_name}")
        if collection_name in self.listeners:
            return f"Listener already running for {collection_name}."

        stop_event = Event()
        self.stop_events[collection_name] = stop_event

        def listen_changes():
            print(f"Starting listener for {collection_name}.")
            collection = self.db[collection_name]
            with collection.watch() as stream:
                try:
                    while not stop_event.is_set():
                        if stream.alive:
                            change = stream.try_next()  # Non-blocking call
                            if change is not None:
                                print(f"Change detected: {change}")
                                self.sender.send(change)
                        else:
                            print("Stream is not alive. Attempting to reopen.")
                            stream = collection.watch()
                        time.sleep(1)
                except PyMongoError as e:
                    print(f"An error occurred: {e}")
                finally:
                    print(f"Stopped listener for {collection_name}.")

        thread = Thread(target=listen_changes, daemon=True)
        thread.start()
        self.listeners[collection_name] = thread
