from pymongo import MongoClient
from .settings import settings

client = MongoClient(settings.MONGO_URL)
database = client[settings.DB_NAME]
