import asyncio
import time
from fastapi import HTTPException
import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from app.models import Account
from riot_api.riot_api import get_match_ids_by_puuid, get_match_by_id

# We fetch data from the RIOT API to store in the database

# Use API call functions to fetch data from the RIOT API

SERVER_URL = "http://127.0.0.1:8000"

# List of Riot-IDs we want to fetch data for
accounts = [{"puuid":"k-v-KRRk3NShmFqebAQEUgFOuYnRFJejaiPQbZedOPGLMcsKZ7vaXdrijId9I3reVO6czKcykBEwFg","gameName":"John","tagLine":"Noob","matchHistory":["NA1_4947745468","NA1_4947732447","NA1_4943444677","NA1_4943410111","NA1_4940025948","NA1_4940015814","NA1_4939984787","NA1_4938616985","NA1_4938588751","NA1_4938111336","NA1_4938103745","NA1_4938086915","NA1_4938066248","NA1_4938050295","NA1_4938040499","NA1_4938034973","NA1_4938020225","NA1_4937763971","NA1_4937723423","NA1_4937675505","NA1_4936681471","NA1_4936648258","NA1_4936363363","NA1_4936347867","NA1_4936318608","NA1_4935618009","NA1_4935606950","NA1_4932801486","NA1_4932778985","NA1_4932697923","NA1_4932447241","NA1_4932414897","NA1_4931968834","NA1_4931942846","NA1_4931911850","NA1_4930842642","NA1_4930800517","NA1_4930755885","NA1_4930473492","NA1_4930454037","NA1_4930419322","NA1_4930405200","NA1_4930016908","NA1_4929772015","NA1_4929744247","NA1_4929728573","NA1_4929649051","NA1_4929627245","NA1_4929600653","NA1_4928491184","NA1_4928477705","NA1_4928444880","NA1_4926503378","NA1_4926458187","NA1_4926126918","NA1_4925961069","NA1_4925930901","NA1_4925901468","NA1_4925507525","NA1_4925073941","NA1_4924541729","NA1_4924379714","NA1_4924344638","NA1_4923976893","NA1_4923569229","NA1_4923453581","NA1_4921891046","NA1_4921871079","NA1_4920981346","NA1_4920952126","NA1_4920928436","NA1_4920905503","NA1_4920882286","NA1_4920763845","NA1_4919678352","NA1_4919656171","NA1_4919640644","NA1_4919624179","NA1_4919595360","NA1_4919576042","NA1_4919558426","NA1_4919535178","NA1_4917673815","NA1_4917623935","NA1_4917605842","NA1_4917575219","NA1_4917410581","NA1_4917399801","NA1_4917374444","NA1_4917358567","NA1_4917347941","NA1_4917323191","NA1_4917298880","NA1_4917263114","NA1_4916863117","NA1_4916836499","NA1_4916810865","NA1_4916753884","NA1_4912509610","NA1_4947761921"]}]
riot_ids = [{"gameName": "John", "tagLine": "Noob" }]

load_dotenv()

# MongoDB Credentials and Riot API Key
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
db_name = "LOL"

print(RIOT_API_KEY)

uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.hevxxit.mongodb.net/LOL?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

accounts_collection = client[db_name]["accounts"]
matches_collection = client[db_name]["matches"]

def populate_accounts_arr():
    accounts = []
    for account in accounts_collection.find():
        accounts.append(Account(puuid = account["puuid"], gameName = account["gameName"], tagLine = account["tagLine"], matchHistory = account["matchHistory"]))
    return accounts

def get_all_puuids():
    """Get all the puuids from the MongoDB collection."""
    return accounts_collection.distinct("puuid")

async def update_match_history(puuid: str):
    account_data = accounts_collection.find_one({"puuid": puuid})
    print(account_data)
    if account_data is None:
        raise HTTPException(status_code=404, detail="Account not found")
    # Fetch new match IDs from Riot API
    match_ids = await get_match_ids_by_puuid(account_data["puuid"], account_data.get("lastUpdated", 0))
    # Process which matches are new and append to match history
    # Get current match history
    current_match_history = account_data.get("matchHistory", [])
    # Determine which ones to add
    matches_to_add = [match_id for match_id in match_ids if match_id not in current_match_history]
    if len(matches_to_add) == 0:
        return {"message": "No new matches found"}
    # Append new match IDs to existing match history
    updated_match_history = matches_to_add + current_match_history
    # Update database with new match history
    accounts_collection.update_one({"puuid": puuid}, {"$set": {"matchHistory": updated_match_history}})
    accounts_collection.update_one({"puuid": puuid}, {"$set": {"lastUpdated": int(time.time())}})

    return {"updated match history": updated_match_history}

async def match_exists(match_id: str) -> bool:
    # check if match exists in db
    result = matches_collection.find_one({"metadata.matchId": match_id})
    return result is not None

async def populate_matches_by_account(puuid: str):
    # Account exists in database, fetch match history and populate database with match info
    account_data = accounts_collection.find_one({"puuid": puuid})
    match_ids = account_data["matchHistory"]

    for match_id in match_ids:
        # Check if accounts.matches contains match_id
        if await match_exists(match_id):
            print("Match already exists")
            continue
        match_info = await get_match_by_id(match_id)
        if match_info is None:
            raise HTTPException(status_code=404, detail="Match not found")
        if match_info.info.queueId not in [420, 440]:
            continue
        match_info_dict = match_info.dict()
        match_info_dict["puuid"] = account_data["puuid"]
        matches_collection.insert_one(match_info_dict)

    # Update lastUpdated Unix timestamp
    accounts_collection.update_one({"puuid": account_data["puuid"]}, {"$set": {"lastUpdated": int(time.time())}})

    return {"message": "Matches added to database"}

# def populate_matches_by_account(account):
#     """
#     Make an API call to populate matches for a given Riot ID.

#     :param account: A dictionary containing account details.
#     """
#     try:
#         response = requests.post(f"{SERVER_URL}/matches/by-account", json=account)
#         if response.status_code == 200:
#             print(f"Successfully populated matches for Riot-ID: {account['gameName']} | {account['tagLine']}")
#         else:
#             print(f"Failed to populate matches for Riot-ID: {account['gameName']} | {account['tagLine']}. Status Code: {response.status_code}, Response: {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")

# def update_match_history(account):
#     """
#     Make an API call to update the match history for a given account.

#     :param account: A dictionary containing account details.
#     """
#     try:
#         response = requests.post(f"{SERVER_URL}/accounts/match-history", json=account)
#         if response.status_code == 200:
#             print(f"Successfully updated match history for Riot-ID: {account['gameName']} | {account['tagLine']}")
#         else:
#             print(f"Failed to update match history for Riot-ID: {account['gameName']} | {account['tagLine']}. Status Code: {response.status_code}, Response: {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")

def delete_matches_field():
    # Just delete the 'matches' field from an account if it exists, because we have a matches collection
    try:
        response = requests.delete(f"{SERVER_URL}/accounts/matches")
        if response.status_code == 200:
            print(f"Successfully deleted matches field for Riot-ID: ")
        else:
            print(f"Failed to delete matches field for Riot-ID:. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def populate_matches_by_riot_id(riot_id):
    """
    Make an API call to the /matches/by-riot-id endpoint to populate matches for a given Riot-ID.

    :param riot_id: A dictionary containing Riot-ID details.
    """
    # First update the account with the latest match history


    try:
        response = requests.post(f"{SERVER_URL}/matches/by-riot-id", json=riot_id)
        if response.status_code == 200:
            print(f"Successfully populated matches for Riot-ID: {riot_id['gameName']} | {riot_id['tagLine']}")
        else:
            print(f"Failed to populate matches for Riot-ID: {riot_id['gameName']} | {riot_id['tagLine']}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")   

def delete_nonranked_matches():
    """
    Make an API call to the /matches/delete-nonranked endpoint to delete non-ranked matches.
    """
    try:
        # response = requests.delete(f"{SERVER_URL}/matches/non-ranked")
        response = requests.delete(f"{SERVER_URL}/accounts/delete-non-ranked")
        if response.status_code == 200:
            print("Successfully deleted non-ranked matches")
        else:
            print(f"Failed to delete non-ranked matches. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

async def main():
    puuids_arr = get_all_puuids()
    print(puuids_arr)
    for puuid in puuids_arr:
        await update_match_history(puuid)
        await populate_matches_by_account(puuid)

if __name__ == "__main__":
    asyncio.run(main())
