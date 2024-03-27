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
ASSIST_SCORE = 2.5
DEATH_SCORE = -3.85
OBJECTIVE_SCORE = 0.45
ENEMY_OBJECTIVE_SCORE = -0.34
STRUCTURE_SCORE = 0.50
ENEMY_STRUCTURE_SCORE = -0.47

client = MongoClient(uri)

accounts_collection = client[db_name]["accounts"]
matches_collection = client[db_name]["matches"]

def get_account_by_puuid(collection, puuid):
    """Get account details by puuid."""
    return collection.find_one({"puuid": puuid})

def get_all_puuids(collection):
    """Get all the puuids from the MongoDB collection."""
    return collection.distinct("puuid")

def get_matches_by_puuid(collection, puuid):
    """Get all matches for a given puuid."""
    return collection.find({"puuid": puuid})

def get_match_history_by_puuid(puuid):
    """Get the match history for a given puuid."""
    account = get_account_by_puuid(accounts_collection, puuid)
    if account is None:
        return None
    return account.get("matchHistory", [])

def get_patch_from_game_version(game_version: str) -> str:
    return '.'.join(game_version.split('.')[:2])

def get_match_by_id(collection, matchId):
    """Get a match by its matchId."""
    return collection.find_one({"metadata.matchId": matchId})

def find_participant_by_puuid(match, puuid):
    """Find a participant in a match by puuid."""
    for participant in match["info"]["participants"]:
        if participant["puuid"] == puuid:
            return participant
    return None

def find_player_kills(participant):
    """Find the number of kills for a given participant."""
    return participant["kills"]

def find_player_deaths(participant):
    """Find the number of deaths for a given participant."""
    return participant["deaths"]

def find_player_assists(participant):
    """Find the number of assists for a given participant."""
    return participant["assists"]

def find_player_win(participant):
    """Find if the player won the match."""
    return participant["win"]

def find_player_position(participant):
    """Find the position of the player in the match."""
    # Your logic here
    return participant["individualPosition"]

def find_player_dragon_kills(participant):
    """Find the number of dragon kills for a given participant."""
    # Your logic here
    return participant["dragonKills"]

def find_player_baron_kills(participant):
    """Find the number of baron kills for a given participant."""
    # Your logic here
    return participant["baronKills"]

def find_player_turret_kills(participant):
    """Find the number of tower kills for a given participant."""
    # Your logic here
    return participant["turretTakedowns"]

def find_player_inhibitor_kills(participant):
    """Find the number of inhibitor kills for a given participant."""
    # Your logic here
    return participant["inhibitorTakedowns"]

def find_opponent(individualPosition: str, match, puuid):
    """Find the opponent position based on the player's position."""
    # Your logic here
    for participant in match["info"]["participants"]:
        if participant["individualPosition"] == individualPosition and participant["puuid"] != puuid:
            return participant

def calculate_op_score(kills, deaths, assists, dragon_kills, baron_kills, turret_kills, inhibitor_kills, enemy_turret_kills, enemy_inhibitor_kills, enemy_dragon_kills, enemy_baron_kills):
    """Calculate the OP score for a given match."""
    # Your scoring logic here
    score = DEFAULT_SCORE + (KILL_SCORE * kills) + (DEATH_SCORE * deaths) + (ASSIST_SCORE * assists) + (OBJECTIVE_SCORE * (dragon_kills + baron_kills)) + (STRUCTURE_SCORE * (turret_kills + inhibitor_kills)) + (ENEMY_OBJECTIVE_SCORE * (enemy_dragon_kills + enemy_baron_kills)) + (ENEMY_STRUCTURE_SCORE * (enemy_turret_kills + enemy_inhibitor_kills))
    return score

if __name__ == "__main__":
    puuids_arr = get_all_puuids(accounts_collection)
        # For each puuid, get match history

    for puuid in puuids_arr:
        match_history = get_match_history_by_puuid(puuid)
        for match_id in match_history:
            match = get_match_by_id(matches_collection, match_id)
            if match is None:
                continue
            if match["processed"] is True:
                continue
            match_patch = get_patch_from_game_version(match["info"]["gameVersion"])
            participant = find_participant_by_puuid(match, puuid)
            if participant is None:
                continue
            player_kills = find_player_kills(participant)
            player_deaths = find_player_deaths(participant)
            player_assists = find_player_assists(participant)
            player_dragons = find_player_dragon_kills(participant)
            player_barons = find_player_baron_kills(participant)
            player_turrets = find_player_turret_kills(participant)
            player_inhibitors = find_player_inhibitor_kills(participant)
            player_win = find_player_win(participant)
            player_position = find_player_position(participant)
            opponent = find_opponent(player_position, match, puuid)
            if opponent is None:
                continue
            opponent_kills = find_player_kills(opponent)
            opponent_deaths = find_player_deaths(opponent)
            opponent_assists = find_player_assists(opponent)
            opponent_dragons = find_player_dragon_kills(opponent)
            opponent_barons = find_player_baron_kills(opponent)
            opponent_turrets = find_player_turret_kills(opponent)
            opponent_inhibitors = find_player_inhibitor_kills(opponent)
            opponent_win = find_player_win(opponent)
            player_score = calculate_op_score(player_kills, player_deaths, player_assists, player_dragons, player_barons, player_turrets, player_inhibitors, opponent_turrets, opponent_inhibitors, opponent_dragons, opponent_barons)
            opponent_score = calculate_op_score(opponent_kills, opponent_deaths, opponent_assists, opponent_dragons, opponent_barons, opponent_turrets, opponent_inhibitors, player_turrets, player_inhibitors, player_dragons, player_barons)
            delta = player_score - opponent_score
            player_kda = (player_kills + player_assists) / max(player_deaths, 1) 
            # Update account with proper running averages of the calculated stats
            account = get_account_by_puuid(accounts_collection, puuid)
            if account is None:
                continue
            if "stats_by_patch" not in account:
                account["stats_by_patch"] = {}
            if match_patch not in account["stats_by_patch"]:
                account["stats_by_patch"][match_patch] = {
                    "kills": 0,
                    "deaths": 0,
                    "assists": 0,
                    "games_played": 0,
                    "kda_ratio": 0,
                    "score": [],
                    "opponent_delta": [],
                    "average_score": 0,
                    "score_std": 0,
                    "average_delta": 0,
                    "opponent_delta_std": 0,
                    "wins": 0,
                    "losses": 0,
                    "win_rate": 0
                }
            account["stats_by_patch"][match_patch]["kills"] += player_kills
            account["stats_by_patch"][match_patch]["deaths"] += player_deaths
            account["stats_by_patch"][match_patch]["assists"] += player_assists
            account["stats_by_patch"][match_patch]["games_played"] += 1
            account["stats_by_patch"][match_patch]["kda_ratio"] = (account["stats_by_patch"][match_patch]["kills"] + account["stats_by_patch"][match_patch]["assists"]) / max(account["stats_by_patch"][match_patch]["deaths"], 1)
            account["stats_by_patch"][match_patch]["score"].append(player_score)
            account["stats_by_patch"][match_patch]["opponent_delta"].append(delta)
            account["stats_by_patch"][match_patch]["average_score"] = sum(account["stats_by_patch"][match_patch]["score"]) / len(account["stats_by_patch"][match_patch]["score"])
            account["stats_by_patch"][match_patch]["score_std"] = (sum([(score - account["stats_by_patch"][match_patch]["average_score"]) ** 2 for score in account["stats_by_patch"][match_patch]["score"]]) / len(account["stats_by_patch"][match_patch]["score"])) ** 0.5
            account["stats_by_patch"][match_patch]["average_delta"] = sum(account["stats_by_patch"][match_patch]["opponent_delta"]) / len(account["stats_by_patch"][match_patch]["opponent_delta"])
            account["stats_by_patch"][match_patch]["opponent_delta_std"] = (sum([(delta - account["stats_by_patch"][match_patch]["average_delta"]) ** 2 for delta in account["stats_by_patch"][match_patch]["opponent_delta"]]) / len(account["stats_by_patch"][match_patch]["opponent_delta"])) ** 0.5
            account["stats_by_patch"][match_patch]["wins"] += 1 if player_win else 0
            account["stats_by_patch"][match_patch]["losses"] += 1 if not player_win else 0
            account["stats_by_patch"][match_patch]["win_rate"] = account["stats_by_patch"][match_patch]["wins"] / account["stats_by_patch"][match_patch]["games_played"]

            # Update match.processed = True
            matches_collection.update_one({"metadata.matchId": match_id}, {"$set": {"processed": True}})
            # Actually update the account in the db
            accounts_collection.update_one({"puuid": puuid}, {"$set": account})

