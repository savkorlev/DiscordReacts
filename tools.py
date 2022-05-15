from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import random


def put_emojies(action_chain, list_with_emojis, wait):
    
    # press and hold the shift button
    action_chain.key_down(Keys.SHIFT)
    action_chain.perform() # note: this line cannot be commented
    
    # put emojies in order
    for i in range(len(list_with_emojis)):
        time.sleep(random.uniform(0.5, 1.0)) # !!! 0.5 is the slowest time so the emojis register in the correct order
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-name=\"{list_with_emojis[i]}\"]"))).click()
    
    # release the shift button
    action_chain.reset_actions()
    action_chain.key_up(Keys.SHIFT)
    action_chain.perform()
    action_chain.reset_actions()


def open_emoji_panel(action_chain, current_message, message_id, driver):
    
    action_chain.move_to_element(current_message)
    action_chain.perform()
    action_chain.reset_actions()
    try:
        driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id} > div > div.buttonContainer-1502pf > div.buttons-3dF5Kd > div > [aria-label=\"Add Reaction\"]").click()
    except (NoSuchElementException, ElementClickInterceptedException):
        pass
    # TODO: maybe try not to pass message_id here and get it from current_message object instead


def click_jump_button(action_chain, tray_message, jump_button):
    
    action_chain.move_to_element(tray_message)
    action_chain.perform()
    action_chain.reset_actions()
    jump_button.click()
