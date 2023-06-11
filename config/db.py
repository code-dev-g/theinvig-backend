from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MONGO_CONNECTION_URL = os.getenv('DATABASE_URL', 'localhost:27017')
MONGO_CONNECTION_URL = os.getenv('DATABASE_URL', 'localhost:27017')
DATABASE_NAME = "invig-m1"

connection = MongoClient(MONGO_CONNECTION_URL)
database = connection[DATABASE_NAME]