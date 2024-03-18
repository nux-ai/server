from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import time

from _utils import create_success_response

from modalities.image import ImageEmbeddingService
from modalities.text import TextEmbeddingService


class EmbeddingHandler:
    def __init__(self, modality, model):
        if modality == "text":
            self.service = TextEmbeddingService(model)
        elif modality == "image":
            self.service = ImageEmbeddingService(model)
       elif modality == "audio":
            self.service = AudioEmbeddingService(model)
        else:
            raise ValueError(f"Unknown modality: {modality}")

    def encode(self, data):
        start_time = time.time() * 1000
        embedding = self.service.encode(data).tolist()[0]
        return create_success_response(
            {
                "embedding": embedding,
                "elapsed_time": (time.time() * 1000) - start_time,
            }
        )

    def get_configs(self):
        start_time = time.time() * 1000
        dimensions = self.service.get_dimensions()
        token_size = self.service.get_token_size()
        return create_success_response(
            {
                "dimensions": dimensions,
                "token_size": token_size,
                "elapsed_time": (time.time() * 1000) - start_time,
            }
        )
