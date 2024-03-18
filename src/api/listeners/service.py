from fastapi import HTTPException
from db_internal.service import BaseAsyncDBService

from utilities.internal_requests import AsyncHttpClient

from config import listener_url
from unstructured.partition.auto import partition

from unstructured.partition.api import partition_via_api
import requests
import json
from io import BytesIO


class ListenerAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("listeners", index_id)
        self.listener_url = listener_url
