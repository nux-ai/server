from fastapi import HTTPException
from db_internal.service import BaseAsyncDBService

from utilities.helpers import unique_name, generate_function_name
from utilities.zipper import PackageZipper
from config import parser_url


class ListenerAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("listeners", index_id)
        self.package_creator_url = parser_url + "/process/package"

    async def get_listener(self, provider_id, listener_name):
        result = await self.get_one(
            {"provider_id": provider_id, "listener_name": listener_name}
        )
        return result

    async def create_listener(self, listener_dict):
        try:
            # create package name
            code_function_name = generate_function_name(
                self.index_id,
                listener_dict["provider_id"],
                listener_dict["listener_name"],
            )
            # create package
            new_package = self._create_new_package(
                code_function_name,
                listener_dict["code_as_string"],
                listener_dict["settings"].get("requirements", []),
                listener_dict["settings"].get("python_version", "python3.10"),
            )
            # store in db
            # await self.create_one(

            # )

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def process_payload(self):
        # queue
        pass

    def _create_new_package(
        self, code_function_name, code_input, requirements, python_version
    ):
        obj = {
            "function_name": code_function_name,
            "code_as_string": code_input,
            "requirements": requirements,
            "python_version": python_version,
        }
        zipper = PackageZipper(obj, self.package_creator_url)
        return zipper.get_s3_url()
