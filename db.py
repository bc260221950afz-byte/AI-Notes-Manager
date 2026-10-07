from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
# Local MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Check MongoDB connection
    client.admin.command("ping")
    print("MongoDB Connected Successfully!")
    # Database
    db = client["ai_notes_db"]
    # Collection
    notes_collection = db["notes"]
except ConnectionFailure:
    print("MongoDB connection failed!")
    notes_collection = None