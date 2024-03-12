from db_internal.service import BaseAsyncDBService

from utilities.helpers import unique_name, generate_function_name
from utilities.zipper import PackageZipper


class ListenerAsyncService(BaseAsyncDBService):
    def __init__(self, index_id):
        super().__init__("listeners", index_id)

    async def get_listener(self, provider_id, listener_name):
        return await self.get_one(
            {"provider_id": provider_id, "listener_name": listener_name}
        )

    async def create_listener(self, listener_dict):
        # insert listener into db
        provider_id = listener_dict["provider_id"]
        listener_name = listener_dict.get("listener_name", unique_name())
        code_as_string = listener_dict["code_as_string"]
        settings = listener_dict.get("settings", {})

        # create new package
        code_function_name = generate_function_name(
            self.index_id, provider_id, listener_name
        )
        pass

    async def process_payload(self):
        # queue
        pass

    def _create_new_package(self, code_function_name, code_input):
        obj = {
            "function_name": code_function_name,
            "code_as_string": code_input,
            "requirements": self.parsed_settings["requirements"],
            "python_version": self.parsed_settings["python_version"],
        }
        zipper = PackageZipper(obj, self.package_creator_url)
        return zipper.get_s3_url()
