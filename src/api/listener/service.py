from db_internal.service import BaseSyncDBService

from utilities.methods import BadRequestError
from utilities.helpers import generate_uuid


class CommentSyncService(BaseSyncDBService):
    def __init__(self, index_id, version_id=None, scope=None):
        super().__init__("comments", index_id, version_id, scope)

    def create(
        self,
        workbook_id: str,
        author_id: str,
        comment: str,
        metadata: dict,
        replied_to: str,
    ):
        obj = {
            "workbook_id": workbook_id,
            "author_id": author_id,
            "comment_id": generate_uuid(length=10, dashes=False),
            "comment": comment,
            "metadata": metadata,
            "replied_to": replied_to,
        }
        return self.create_one(obj)

    def list(self, lookup_conditions=None, limit=None, offset=None):
        if lookup_conditions is None:
            lookup_conditions = {}
        results = self.list_by_index(lookup_conditions, limit, offset)
        return results
