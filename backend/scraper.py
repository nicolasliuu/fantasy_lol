from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

# Apply notification preferences
options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def close_popup():
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close"))).click()
    except Exception as e:
        print(f"Error closing popup: {e}")  

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
        except Exception as e:
            print(f"Error clicking details button: {e}")
            continue
        
        # Using BeautifulSoup to parse the game's HTML
        game_html = game.get_attribute('outerHTML')
        soup = bs(game_html, 'html.parser')
        game_info = {
            'game_mode': soup.find('div', class_='game-type').text.strip(),
            'date': soup.find('div', class_='time-stamp').div.text.strip(),
            'result': soup.find('div', class_='result').text.strip(),
            'length': soup.find('div', class_='length').text.strip(),
            # Add more fields as necessary
        }
        games_info.append(game_info)

    print("HELLO")

    input()
    driver.quit()
    return games_info

games_info = extract_user_data("John-Noob")
for game in games_info:
    print(game)
    