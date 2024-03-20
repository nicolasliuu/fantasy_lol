import httpx
from dotenv import load_dotenv
import os
from models import Match

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
region = "americas"

# For rate limiting purposes, 20 per 1 second 100 per 2 minutes


async def get_puuid_by_riot_id(gameName: str, tagLine: str):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()  # Raises exception for 4XX/5XX responses
            print("PUUID found!")
            return resp.json()["puuid"]
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
        # except Exception as e:
        #     print(f"An error occurred: {e}")
    return None

async def get_match_ids_by_puuid(puuid: str):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=100"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
    return []

async def get_match_by_id(matchId: str):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            # Assuming you have a function to deserialize JSON to your Match model
            return Match(**resp.json())
    return None
