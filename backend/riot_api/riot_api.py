import asyncio
import httpx
from dotenv import load_dotenv
import os
from app.models import Match


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

async def get_match_ids_by_puuid(puuid: str, lastUpdated: int = 0):
    # url should depend on lastUpdated time.
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={lastUpdated}&type=ranked&count=100"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    async with httpx.AsyncClient() as client:
        try: 
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()
            print("Match IDs found!")
            return resp.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code}")
    return []

async def get_match_by_id(matchId: str):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()  # Raises error for 4xx or 5xx responses
            print("Match found!")
            return Match(**resp.json())  # Assuming Match is a valid class/model you have defined elsewhere
        except httpx.HTTPStatusError as e:
            # Check if the error is because of rate limiting
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", "10"))  # Default to 1 second if header is missing
                print(f"Rate limited. Retrying after {retry_after} seconds")
                await asyncio.sleep(retry_after)  # Sleep for the duration of the rate limit
                return await get_match_by_id(matchId)  # Recursively retry fetching the match
            else:
                # Handle other HTTP errors
                print(f"HTTP error occurred: {e.response.status_code}")
    return None
