from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import time


class EmbeddingHandler:
    def __init__(self, modality, model):
        if modality == "text":
            self.service = TextEmbeddingService(model)
        else:
            raise ValueError(f"Unknown modality: {modality}")

    def encode(self, data):
        start_time = time.time() * 1000
        embedding = self.service.encode(data).tolist()[0]
        return {
            "embedding": embedding,
            "elapsed_time": (time.time() * 1000) - start_time,
        }

    def get_configs(self):
        start_time = time.time() * 1000
        dimensions = self.service.get_dimensions()
        token_size = self.service.get_token_size()
        return {
            "dimensions": dimensions,
            "token_size": token_size,
            "elapsed_time": (time.time() * 1000) - start_time,
        }


class TextEmbeddingService:
    def __init__(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModel.from_pretrained(model)

    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def encode(self, sentences):
        encoded_input = self.tokenizer(
            sentences, padding=True, truncation=True, return_tensors="pt"
        )

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        sentence_embeddings = self.mean_pooling(
            model_output, encoded_input["attention_mask"]
        )
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        return sentence_embeddings

    def get_dimensions(self):
        return self.model.config.hidden_size

    def get_token_size(self):
        return self.tokenizer.model_max_length
