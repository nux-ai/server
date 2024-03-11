import os
from dotenv import load_dotenv

load_dotenv()

python_version = os.getenv("PYTHON_VERSION")
log_level = os.getenv("LOG_LEVEL")

# dbs
redis_url = os.getenv("REDIS_URL")
mongo_url = os.getenv("MONGO_URL")

# inference
openai_key = os.getenv("OPENAI_KEY")

# containers
parser_url = os.getenv("PARSER_CONTAINER_URL")
storage_url = os.getenv("STORAGE_CONTAINER_URL")
inference_url = os.getenv("INFERENCE_CONTAINER_URL")

# cloud
mongodb_atlas = {
    "public_key": os.getenv("MONGODB_PUBLIC_KEY"),
    "private_key": os.getenv("MONGODB_PRIVATE_KEY"),
    "group_id": os.getenv("MONGODB_GROUP_ID"),
}
