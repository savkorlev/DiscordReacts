from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import tools
import messages
import prereact
import time
import random


# USER INPUT
email = input("1/8. Enter your account's email:")
password = input("2/8. Enter your account's password:")
target_person = "from: " + input("3/8. Enter the target person's identifier (example: SampleUser#1234):") + " "
target_server = input("4/8. Enter the target server (example: Sample Server):")
number_of_emojis = input("5/8. Enter the number of emojis to put (example: 4):")
emoji_list = []
for i in range(int(number_of_emojis)):
    if i == 0:
        emoji_list.append(input(f"6/8. Enter the name of the {i + 1} emoji (example: regional_indicator_s. WARNING: order does matter):"))
    else:
        emoji_list.append(input(f"Enter the name of the {i + 1} emoji:"))
number_of_pages = input("7/8. Enter the number of pages to parse (example: 4. To enter all messages type: max. Each page contains 25 messages):")
screen_resolution = input("8/8. Enter your screen resolution (example: 1920x1080):").split("x")

# set up
chrome_options = webdriver.ChromeOptions()
# hide the automated browser notification
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument('--window-size=1920,1080')
# activating headless mode
chrome_options.add_argument(f'--window-size={screen_resolution[0]},{screen_resolution[1]}')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=\'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36\'')
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.maximize_window() # driver.set_window_size(1920, 1080)
driver.get("https://discord.com/channels/@me")
wait = WebDriverWait(driver, 300)
ac_versatile = ActionChains(driver)

# authorization
prereact.authorize(wait, email, password)

# turn off motion animations
prereact.turn_off_animations(wait, ac_versatile)

# navigate to the target server and get permissions
first_channel = prereact.navigation_and_permissions(wait, target_server, driver)

# search for the target person
prereact.search_for_person(wait, target_person)

# get the total number of pages to parse
number_of_pages = prereact.get_number_of_pages(wait, number_of_pages)

# delete the redundant variables
del(chrome_options)
del(email)
del(number_of_emojis)
del(password)
del(target_person)
del(target_server)
del(screen_resolution)

for i in range(number_of_pages):
    # get all messages of the target person in the current page
    tray_of_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.container-rZM65Y")))
    
    # find a message from the tray of messages in the actual chat by its id
    for tray_message in tray_of_messages:
        
        message_id = tray_message.find_element(By.CSS_SELECTOR, "div > div > div").get_attribute("id")[14:]
        
        is_jump_button_clicked = False
        
        while not is_jump_button_clicked:
            
            time.sleep(random.uniform(0.0, 1.5))
            
            try:
                jump_button = tools.find_jump_button(ac_versatile, tray_message)
            except NoSuchElementException:
                continue
            
            try:
                jump_button.click()
                is_jump_button_clicked = True
            except ElementNotInteractableException:
                pass
        
        time.sleep(0.5) # !!! because of discord weird animation bugs this line makes script to work even faster by omitting double jump clicks
        
        # voice chat message
        if len(driver.find_elements(By.CSS_SELECTOR, "button.joinButton-2KP9ZZ")) != 0:
            messages.process_new_message(driver, message_id, ac_versatile, tray_message, jump_button, emoji_list, first_channel)
            
        # any other message
        else:
            messages.process_old_message(driver, message_id, ac_versatile, tray_message, jump_button, emoji_list)
    
    # go to the next page
    driver.find_element(By.CSS_SELECTOR, 'button[rel=\'next\']').click()

driver.quit()
