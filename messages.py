from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import tools


def process_new_message(driver, message_id, action_chain, tray_message, jump_button, emoji_list, first_channel):
        
    # open the reaction panel and put emojies. If there was an animation bug - wait
    are_emojies_placed = False
    # avoid locked messages - no more than 5 attempts
    number_of_attempts = 0
    
    while not are_emojies_placed and number_of_attempts < 6:
        
        number_of_attempts += 1
        
        try: 
            current_message = driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id}")
        except NoSuchElementException:
            tools.handle_new_message_exceptions(first_channel, action_chain, tray_message, jump_button)
            continue
        
        try:
            tools.open_emoji_panel(action_chain, current_message, message_id, driver)
        except NoSuchElementException:
            tools.handle_new_message_exceptions(first_channel, action_chain, tray_message, jump_button)
            continue
        
        try:
            tools.put_emojies(action_chain, emoji_list, driver)
            are_emojies_placed = True
        except NoSuchElementException:
            tools.handle_new_message_exceptions(first_channel, action_chain, tray_message, jump_button)
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
            tools.handle_old_message_exceptions(action_chain, tray_message, jump_button)
            continue
        
        try:
            tools.open_emoji_panel(action_chain, current_message, message_id, driver)
        except NoSuchElementException:
            tools.handle_old_message_exceptions(action_chain, tray_message, jump_button)
            continue
        
        try:
            tools.put_emojies(action_chain, emoji_list, driver)
            are_emojies_placed = True
        except NoSuchElementException:
            tools.handle_old_message_exceptions(action_chain, tray_message, jump_button)
            pass
