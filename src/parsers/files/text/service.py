import aiohttp

from unstructured.partition.pdf import partition_pdf
from unstructured.cleaners.core import clean
from unstructured.chunking.basic import chunk_elements


from _exceptions import InternalServerError


class TextService:
    def __init__(self, file_stream, metadata):
        self.metadata = metadata
        self.file_stream = file_stream
        self.chunks = []

    def _clean(self, text):
        return clean(text, bullets=True, extra_whitespace=True, dashes=True)

    def _chunk(self, elements, chunk_size=500, overlap_percent=15):
        overlap_subset = int(chunk_size * (overlap_percent / 100))
        return chunk_elements(
            elements,
            max_characters=chunk_size,
            overlap=overlap_subset,
        )

    async def run_pdf(self):
        try:
            elements = partition_pdf(
                file=self.file_stream,
                infer_table_structure="true",
                metadata_filename=self.metadata["filename"],
                # skip_infer_table_types=[],
                strategy="hi_res",
                hi_res_model_name="detectron2_onnx",
            )
            chunks = self._chunk(elements)
            for c in chunks:
                response_obj = c.to_dict()
                response_obj["text"] = self._clean(response_obj["text"])
                self.chunks.append(response_obj)

            return {
                "success": True,
                "status": 200,
                "error": None,
                "response": self.chunks,
            }, 200
        except Exception as e:
            error = {"message": str(e)}
            raise InternalServerError(error)
