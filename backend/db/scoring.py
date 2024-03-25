# For a given riot id / account object, we find its puuid and find all corresponding matches

# Path: backend/db/scoring.py

from dotenv import load_dotenv
from pymongo.server_api import ServerApi
import os
from pymongo import MongoClient



load_dotenv()

# MongoDB Credentials and Riot API Key
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
db_name = "LOL"

print(RIOT_API_KEY)

uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.hevxxit.mongodb.net/LOL?retryWrites=true&w=majority&appName=Cluster0"

# SCORING CONSTANTS (Bullshitted from deeplol.gg idk)
DEFAULT_SCORE = 50
KILL_SCORE = 4.8
DEATH_SCORE = -3.85
OBJECTIVE_SCORE = 0.45
ENEMY_OBJECTIVE_SCORE = -0.34
STRUCTURE_SCORE = 0.50
ENEMY_STRUCTURE_SCORE = -0.47



def create_mongo_client(uri):
    """Connect to the specified MongoDB collection."""
    client = MongoClient(uri)
    return client

def get_account_by_puuid(collection, puuid):
    """Get account details by puuid."""
    return collection.find_one({"puuid": puuid})

def get_all_puuids(collection):
    """Get all the puuids from the MongoDB collection."""
    return collection.distinct("puuid")

def get_matches_by_puuid(collection, puuid):
    """Get all matches for a given puuid."""
    return collection.find({"puuid": puuid})

def calculate_op_score(match):
    """Calculate the OP score for a given match."""
    # Your scoring logic here
    return 0



if __name__ == "__main__":
    client = create_mongo_client(uri)
    accounts_collection = client[db_name]["accounts"]
    matches_collection = client[db_name]["matches"]
    puuids_arr = []
    puuids_arr = get_all_puuids(accounts_collection)
