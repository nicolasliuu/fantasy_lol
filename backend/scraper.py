from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import re

# Apply notification preferences
options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def close_popup():
    try:
        wait = WebDriverWait(driver, 10)
        # Targeting the 'vm-footer-close' div for the close button
        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".vm-footer-close")))
        close_button.click()
        print("Popup closed successfully.")
    except Exception as e:
        print(f"Error closing popup: {e}")

def extract_player_data_from_row(row):
    """
    Extracts and returns data from a given row.
    Adjust selectors based on actual HTML structure.
    """
    data = {}
    data['op_score'] = row.find('div', class_='score').text.strip()
    kda_elements = row.find('td', class_='kda')
    if kda_elements:
        kda_div_elements = kda_elements.find_all('div')
        if kda_div_elements:
            data['KDA'] = kda_div_elements[0].text.strip()
            data['Ratio'] = kda_div_elements[1].text.strip()
        else:
            print("No <div> elements found within the <td>.")
    cs_elements = row.find('td', class_='cs')
    if cs_elements:
        cs_div_elements = cs_elements.find_all('div')
        if cs_div_elements:
            data['CS'] = cs_div_elements[0].text.strip()
            data['CS_per_min'] = cs_div_elements[1].text.strip()
        else:
            print("No <div> elements found within the <td>.")
    else:
        print("No <td> element with class 'cs' found.")
    return data

def extract_user_data(username):
    url = f'https://www.op.gg/summoners/na/{username}'
    driver.get(url)
    close_popup()

    # Locate and click the update button correctly, assuming you find the correct selector or ID
    try:
        update_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'the-correct-selector-for-update')))
        update_button.click()
    except Exception as e:
        print(f"Error clicking update button: {e}")
    
    # Ensure the page has updated by waiting for a specific element that signifies the update is complete

    games_info = []
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'Game')) > 0
    )
    games = driver.find_elements(By.CLASS_NAME, 'Game')

    print(len(games), "\n")
    count = 1
    
    for game in games:
        print(count, "\n")
        count+=1
        # Using WebDriver to click the detail button now
        try:
            details_button = game.find_element(By.CSS_SELECTOR, '.btn-detail')
            driver.execute_script("arguments[0].scrollIntoView(true);", details_button)
            # Example: Waiting for a footer or overlay to not be visible or present
            WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CSS_SELECTOR, "div.vm-footer-content")))

            details_button.click()
            # Wait for details to expand; adjust condition as needed
            WebDriverWait(driver, 5).until(
                lambda d: "some-condition-to-check-details-expanded"
            )
            print(f"Details button clicked for game {count - 1} \n")
        except Exception as e:
            print(f"Error clicking details button: {e}")
            continue
        

        # Using BeautifulSoup to parse the game's HTML
        game_html = game.get_attribute('outerHTML')
        with open(f"game_html.txt{count - 1}", "w") as f:
            print(game_html, file = f)
        soup = bs(game_html, 'html.parser')
        game_info = {
            'game_mode': soup.find('div', class_='game-type').text.strip(),
            'date': soup.find('div', class_='time-stamp').div.text.strip(),
            'result': soup.find('div', class_='result').text.strip(),
            'length': soup.find('div', class_='length').text.strip(),
            # Add more fields as necessary
        }

        # Wait for scoreboard (table element exists) to load
        WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.TAG_NAME, "table") is not None
        )

        # We want the parent element of the GAME div because it will contain the scoreboard after clicking the details button
        game_parent = game.find_element(By.XPATH, '..')
        game_parent_html = game_parent.get_attribute('outerHTML')

        # See contents of game_parent
        with open(f"game_parent_html{count - 1}.txt", "w") as f:
            print(game_parent_html, file = f)

        # After clicking details button, parse the rows of players to find the one we're interest in:

        soup_container = bs(game_parent_html, 'html.parser')
    
        player_rows = soup_container.find_all('tr', class_="overview-player")

        with open("player_rows.txt", "w") as f:
            print(player_rows, file = f)
        print("HERE")

        # Assume 'player_identifier' uniquely identifies the player's row, like their name or summoner ID
        player_identifier = f'{username}'

        position = 0

        # Iterate over rows to find the player's position
        for index, row in enumerate(player_rows):
            if player_identifier in str(row):
                position = index + 1  # Positions start at 1, not 0
                break

        if position == 0:
            print(f"Player {username} not found in game {count - 1}")
            input()
            continue

        # Assuming there are exactly 10 players listed in order, 5 per team
        # Calculate opponent's position assuming the player is in the first team
        opponent_position = position + 5 if position <= 5 else position - 5

        if position == 1:
            game_info['position'] = 'Top'
        elif position == 2:
            game_info['position'] = 'Jungle'
        elif position == 3:
            game_info['position'] = 'Mid'
        elif position == 4:
            game_info['position'] = 'ADC'
        elif position == 5:
            game_info['position'] = 'Support'
        else:
            game_info['position'] = 'Unknown'

        # Now, extract data for the player
        player_data = extract_player_data_from_row(player_rows[position - 1])
        player_op_score = player_data['op_score']
        player_kda = player_data['KDA']
        player_cs = player_data['CS']

        # Extract data for the opponent
        opponent_op_score = extract_player_data_from_row(player_rows[opponent_position - 1])['op_score']

        # Assuming you've defined extract_data_from_row correctly, 
        # player_op_score and opponent_op_score now contain the scraped data.

        print("Player Data:", player_op_score)
        print("Opponent Data:", opponent_op_score)

        # Append the data to the game_info dictionary
        game_info['player_op_score'] = player_op_score
        game_info['opponent_op_score'] = opponent_op_score
        game_info['KDA'] = player_kda
        game_info['KDA Ratio'] = player_data['Ratio']
        game_info['CS'] = player_cs
        game_info['CS_per_min'] = player_data['CS_per_min']


        games_info.append(game_info)

    input()
    driver.quit()
    return games_info




games_info = extract_user_data("Kurriyan-NA1")

#Output
for game in games_info:
    print(game)
        