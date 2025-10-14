import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

load_dotenv()
MONGO_URI = os.getenv("MONGO_CLIENT_URI")
DB_NAME = os.getenv(
    "DB_NAME",
    "meltwater-feeds-prod"
)

def get_async_client():
    return AsyncMongoClient(
        MONGO_URI,
        server_api=ServerApi('1')
    )
