import requests

# We fetch data from the RIOT API to store in the database

# Use API call functions to fetch data from the RIOT API

SERVER_URL = "http://127.0.0.1:8000"

# List of Riot-IDs we want to fetch data for
accounts = [{"puuid":"k-v-KRRk3NShmFqebAQEUgFOuYnRFJejaiPQbZedOPGLMcsKZ7vaXdrijId9I3reVO6czKcykBEwFg","gameName":"John","tagLine":"Noob","matchHistory":["NA1_4947745468","NA1_4947732447","NA1_4943444677","NA1_4943410111","NA1_4940025948","NA1_4940015814","NA1_4939984787","NA1_4938616985","NA1_4938588751","NA1_4938111336","NA1_4938103745","NA1_4938086915","NA1_4938066248","NA1_4938050295","NA1_4938040499","NA1_4938034973","NA1_4938020225","NA1_4937763971","NA1_4937723423","NA1_4937675505","NA1_4936681471","NA1_4936648258","NA1_4936363363","NA1_4936347867","NA1_4936318608","NA1_4935618009","NA1_4935606950","NA1_4932801486","NA1_4932778985","NA1_4932697923","NA1_4932447241","NA1_4932414897","NA1_4931968834","NA1_4931942846","NA1_4931911850","NA1_4930842642","NA1_4930800517","NA1_4930755885","NA1_4930473492","NA1_4930454037","NA1_4930419322","NA1_4930405200","NA1_4930016908","NA1_4929772015","NA1_4929744247","NA1_4929728573","NA1_4929649051","NA1_4929627245","NA1_4929600653","NA1_4928491184","NA1_4928477705","NA1_4928444880","NA1_4926503378","NA1_4926458187","NA1_4926126918","NA1_4925961069","NA1_4925930901","NA1_4925901468","NA1_4925507525","NA1_4925073941","NA1_4924541729","NA1_4924379714","NA1_4924344638","NA1_4923976893","NA1_4923569229","NA1_4923453581","NA1_4921891046","NA1_4921871079","NA1_4920981346","NA1_4920952126","NA1_4920928436","NA1_4920905503","NA1_4920882286","NA1_4920763845","NA1_4919678352","NA1_4919656171","NA1_4919640644","NA1_4919624179","NA1_4919595360","NA1_4919576042","NA1_4919558426","NA1_4919535178","NA1_4917673815","NA1_4917623935","NA1_4917605842","NA1_4917575219","NA1_4917410581","NA1_4917399801","NA1_4917374444","NA1_4917358567","NA1_4917347941","NA1_4917323191","NA1_4917298880","NA1_4917263114","NA1_4916863117","NA1_4916836499","NA1_4916810865","NA1_4916753884","NA1_4912509610","NA1_4947761921"]}]
riot_ids = [{"gameName": "John", "tagLine": "Noob" }]

def populate_accounts_arr():
    """
    Make an API call to populate accounts.
    """
    try:
        response = requests.get(f"{SERVER_URL}/accounts")
        if response.status_code == 200:
            print("Successfully populated accounts")
        else:
            print(f"Failed to populate accounts. Status Code: {response.status_code}, Response: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def populate_matches_by_account(account):
    """
    Make an API call to populate matches for a given Riot ID.

    :param account: A dictionary containing account details.
    """
    try:
        response = requests.post(f"{SERVER_URL}/matches/by-account", json=account)
        if response.status_code == 200:
            print(f"Successfully populated matches for Riot-ID: {account['gameName']} | {account['tagLine']}")
        else:
            print(f"Failed to populate matches for Riot-ID: {account['gameName']} | {account['tagLine']}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def update_match_history(account):
    """
    Make an API call to update the match history for a given account.

    :param account: A dictionary containing account details.
    """
    try:
        response = requests.post(f"{SERVER_URL}/accounts/match-history", json=account)
        if response.status_code == 200:
            print(f"Successfully updated match history for Riot-ID: {account['gameName']} | {account['tagLine']}")
        else:
            print(f"Failed to update match history for Riot-ID: {account['gameName']} | {account['tagLine']}. Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

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

if __name__ == "__main__":
    delete_matches_field()
    # accounts = populate_accounts_arr()
    # for account in accounts:
    #     update_match_history(account)
    #     riot_id = {"gameName": account["gameName"], "tagLine": account["tagLine"]}
    #     populate_matches_by_riot_id(riot_id)
    # for riot_id in riot_ids:
    #     populate_matches_by_riot_id(riot_id)
    # delete_nonranked_matches()