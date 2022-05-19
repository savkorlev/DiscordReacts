from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import tools
import time
import random


def process_new_message(driver, message_id, action_chain, emoji_list, wait, first_channel):
    
    current_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"#chat-messages-{message_id}"))) # TODO: inculde this to a loop as in the version above and make it wait less
    
    # open the reaction panel and put emojies. If there was an animation bug - wait
    are_emojies_placed = False
    # avoid locked messages - no more than 5 attempts
    number_of_attempts = 0
    
    while not are_emojies_placed and number_of_attempts < 6:
        
        number_of_attempts += 1
        
        try:
            tools.open_emoji_panel(action_chain, current_message, message_id, driver)
        except NoSuchElementException:
            time.sleep(0.5)
            continue
        
        try:
            tools.put_emojies(action_chain, emoji_list, driver)
            are_emojies_placed = True
        except NoSuchElementException:
            time.sleep(0.5)
            pass
    
    # return back to the search results
    first_channel.click()


def process_old_message(driver, message_id, action_chain, tray_message, jump_button, emoji_list):
    
    # open the reaction panel and put emojies. If there was an animation bug - click the jump button and wait
    are_emojies_placed = False
    # avoid locked messages - no more than 5 attempts
    number_of_attempts = 0
    
    while not are_emojies_placed and number_of_attempts < 6: 
        
        number_of_attempts += 1
        
        try:
            current_message = driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id}")
        except NoSuchElementException:
            time.sleep(random.uniform(0.0, 0.5))
            tools.click_jump_button(action_chain, tray_message, jump_button)
            time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out
            continue
        
        try:
            tools.open_emoji_panel(action_chain, current_message, message_id, driver)
        except NoSuchElementException:
            time.sleep(random.uniform(0.0, 0.5))
            tools.click_jump_button(action_chain, tray_message, jump_button)
            time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out
            continue
        
        try:
            tools.put_emojies(action_chain, emoji_list, driver)
            are_emojies_placed = True
        except NoSuchElementException:
            time.sleep(random.uniform(0.0, 0.5))
            tools.click_jump_button(action_chain, tray_message, jump_button)
            time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out
            pass

# TODO: maybe separate one big try to multiple small try's
