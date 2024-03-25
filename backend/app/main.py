import time
from fastapi import FastAPI, HTTPException
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.mongo_client import MongoClient
from typing import Union
from pymongo.server_api import ServerApi
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
from app.models import Account, AccountCreationRequest
from riot_api.riot_api import get_puuid_by_riot_id, get_match_ids_by_puuid, get_match_by_id
import os

load_dotenv()

# MongoDB Credentials and Riot API Key
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
db_name = "LOL"

print(RIOT_API_KEY)

uri = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.hevxxit.mongodb.net/LOL?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()

# Collection objects
db = client[db_name]
accounts_collection = db["accounts"]
matches_collection = db["matches"]

# RATE LIMITING

# Check for existence of account in database
async def account_exists(gameName: str, tagLine: str) -> bool:
    db = client[db_name]
    accounts_collection = db["accounts"]
    # Check if account exists in database
    result = accounts_collection.find_one({"gameName": gameName, "tagLine": tagLine})
    return result is not None

async def match_exists(match_id: str) -> bool:
    # check if match exists in db
    result = matches_collection.find_one({"metadata.matchId": match_id})
    return result is not None

async def account_match_exists(match_id: str, account: Account) -> bool:
    # check if match exists in account
    result = accounts_collection.find_one({"puuid": account["puuid"], "matches.metadata.matchId": match_id})
    return result is not None

# Given Riot Id populate database with account info (PUUID), Match History
@app.post("/accounts/", response_model=AccountCreationRequest)
async def create_account(request: AccountCreationRequest):
    if await account_exists(request.gameName, request.tagLine):
        # Don't want exception here, just return the account
        account_data = accounts_collection.find_one({"gameName": request.gameName, "tagLine": request.tagLine})
        account = Account(puuid = account_data["puuid"], gameName = account_data["gameName"], tagLine = account_data["tagLine"], matchHistory = account_data["matchHistory"])
        return account
    puuid = await get_puuid_by_riot_id(request.gameName, request.tagLine)
    print(puuid)
    match_ids = await get_match_ids_by_puuid(puuid)
    print(match_ids)
    # Create an account object
    if (puuid is None) or (len(match_ids) == 0):
        raise HTTPException(status_code=404, detail="Account not found")
    account = Account(puuid=puuid, gameName=request.gameName, tagLine=request.tagLine, matchHistory=match_ids)
    db = client[db_name]
    accounts_collection = db["accounts"]
    accounts_collection.insert_one(account.dict())
    return account

@app.get("/accounts/")
async def read_accounts():
    accounts = []
    for account in accounts_collection.find():
        accounts.append(Account(puuid = account["puuid"], gameName = account["gameName"], tagLine = account["tagLine"], matchHistory = account["matchHistory"]))
    return accounts

@app.post("/accounts/match-history/")
async def update_match_history(request: Account):
    print("request: ", request)
    account_data = accounts_collection.find_one({"puuid": request.puuid})
    if account_data is None:
        raise HTTPException(status_code=404, detail="Account not found")
    print(account_data)
    # Fetch new match IDs from Riot API
    match_ids = await get_match_ids_by_puuid(account_data["puuid"], account_data.get("lastUpdated", 0))
    # Process which matches are new and append to match history

    # Get current match history
    current_match_history = account_data.get("matchHistory", [])
    # Determine which ones to add
    matches_to_add = [match_id for match_id in match_ids if match_id not in current_match_history]
    # Append new match IDs to existing match history
    updated_match_history = matches_to_add + current_match_history
    # Update database with new match history
    accounts_collection.update_one({"puuid": request.puuid}, {"$set": {"matchHistory": updated_match_history}})
    accounts_collection.update_one({"puuid": request.puuid}, {"$set": {"lastUpdated": int(time.time())}})

    return {"updated match history": updated_match_history}

# Given match history, populate database with match info (participants, game mode, etc.)
@app.post("/matches/by-id")
async def create_match(match_ids : list[str]):
    for match_id in match_ids:
        # Check if we already have the match in the database
        if await match_exists(match_id):
            continue
        match_info = await get_match_by_id(match_id)
        if match_info is None:
            raise HTTPException(status_code=404, detail="Match not found")
        matches_collection.insert_one(match_info.dict())
    return {"message": "Matches added to database"}

# Given account info, populate db with match info that is not already in the db
@app.post("/matches/by-account")
async def create_matches_by_account(request: Account):
    account_data = accounts_collection.find_one({"puuid": request.puuid})
    if account_data is None:
        raise HTTPException(status_code=404, detail="Account not found")
    match_ids = account_data["matchHistory"]
    for match_id in match_ids:
        # Check if we already have the match in the database
        if await match_exists(match_id):
            continue
        match_info = await get_match_by_id(match_id)
        if match_info is None:
            raise HTTPException(status_code=404, detail="Match not found")
        matches_collection.insert_one(match_info.dict())
    return {"message": "Matches added to database"}

# Populate db with match info for an unadded account, using only Riot Id
@app.post("/matches/by-riot-id")
async def create_matches_by_riot_id(request: AccountCreationRequest):
    if not await account_exists(request.gameName, request.tagLine):
        # Account does not exist in database, create it
        puuid = await get_puuid_by_riot_id(request.gameName, request.tagLine)
        # Also create an object for the account
        match_ids = await get_match_ids_by_puuid(puuid)
        # Create an account object
        if (puuid is None) or (len(match_ids) == 0):
            raise HTTPException(status_code=404, detail="Account not found")
        account = Account(puuid=puuid, gameName=request.gameName, tagLine=request.tagLine, matchHistory=match_ids, lastUpdated = 0)
        accounts_collection.insert_one(account.dict())
    # Account exists in database, fetch match history and populate database with match info
    account_data = accounts_collection.find_one({"gameName": request.gameName, "tagLine": request.tagLine})
    match_ids = account_data["matchHistory"]

    for match_id in match_ids:
        # Check if accounts.matches contains match_id
        if await match_exists(match_id):
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

# Need to figure out how to handle rate limiting

# Get account by Riot Id
@app.get("/accounts/{gameName}/{tagLine}", response_model=Account)
async def read_account(gameName: str, tagLine: str):

    account_data = accounts_collection.find_one({"gameName": gameName, "tagLine": tagLine})
    if account_data is None:
        raise HTTPException(status_code=404, detail="Account not found")
    account = Account(puuid = account_data["puuid"], gameName = account_data["gameName"], tagLine = account_data["tagLine"], matchHistory = account_data["matchHistory"])
    return account

# Delete matches that are not ranked
@app.delete("/matches/non-ranked")
async def delete_non_ranked_matches():
    # Delete queueId != 420, != 440
    matches_collection.delete_many({"info.queueId": {"$nin": [420, 440]}})
    return {"message": "Non-ranked matches deleted"}

@app.delete("/accounts/delete-non-ranked")
async def delete_non_ranked_matches_from_accounts():
    # Delete documents where queueId is not 420 and not 440
    accounts_collection.update_many(
        {},
        {
            "$pull": {
                "matches": {
                    "info.queueId": {"$nin": [420, 440]}
                }
            }
        }
    )
    return {"message": "Non-ranked matches deleted from accounts"}

@app.delete("/accounts/matches")
async def delete_matches_field_from_account():
    accounts_collection.update_many({}, {"$unset": {"matches": ""}})
    return {"message": "Matches field deleted from accounts"}


async def main():
    # Properly awaiting the coroutine and printing its result
    puuid = await get_puuid_by_riot_id("John", "Noob")
    # if puuid is None:
    #     raise HTTPException(status_code=404, detail="PUUID not found")
    # print(puuid)
    # match_ids = await get_match_ids_by_puuid(puuid)
    # print(match_ids)
    # match_info = await get_match_by_id(match_ids[5])
    # print(match_info)
    # accounts_collection.update_many({}, {"$unset": {"matches": ""}})
    # print("Deleted matches field from accounts")

# This runs the main() coroutine and waits for it to finish
if __name__ == "__main__":
    asyncio.run(main())