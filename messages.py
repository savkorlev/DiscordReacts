from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import tools
import time


def process_old_message(driver, message_id, action_chain, tray_message, jump_button, emoji_list, wait):
    
    # select an exact message by its id in the actual chat
    is_current_message_found = False
    while not is_current_message_found:
        try:
            current_message = driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id}")
            is_current_message_found = True
        except NoSuchElementException:
            tools.click_jump_button(action_chain, tray_message, jump_button)
    
    # open the reaction panel. If there was an animation bug - repeat
    is_emoji_panel_opened = False
    while not is_emoji_panel_opened: 
        try:
            driver.find_element(By.CSS_SELECTOR, f"[data-name=\"{emoji_list[0]}\"]")
            is_emoji_panel_opened = True
        except NoSuchElementException:
            tools.click_jump_button(action_chain, tray_message, jump_button)
            time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out 
            tools.open_emoji_panel(action_chain, current_message, message_id, driver)

    # put emojies
    tools.put_emojies(action_chain, emoji_list, wait) # why there were no errors even while it was tabulated one additional position to the right


def process_new_message(driver, message_id, action_chain, emoji_list, wait, first_channel):
    
    current_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"#chat-messages-{message_id}")))
    is_emoji_panel_opened = False
    while not is_emoji_panel_opened:
        try:
            driver.find_element(By.CSS_SELECTOR, f"[data-name=\"{emoji_list[0]}\"]")
            is_emoji_panel_opened = True
        except NoSuchElementException:
            time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out 
            tools.open_emoji_panel(action_chain, current_message, message_id, driver)

    # put emojies
    tools.put_emojies(action_chain, emoji_list, wait) # why there were no errors even while it was tabulated one additional position to the right
    
    # return back to the search results
    first_channel.click()
