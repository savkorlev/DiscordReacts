from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random


def open_emoji_panel(action_chain, current_message, message_id, driver):
    
    action_chain.move_to_element(current_message)
    action_chain.perform()
    action_chain.reset_actions()
    driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id} > div > div.buttonContainer-1502pf > div.buttons-3dF5Kd > div > [aria-label=\"Add Reaction\"]").click()
    # TODO: maybe try not to pass message_id here and get it from current_message object instead


def put_emojies(action_chain, emoji_list, driver):
    
    # press and hold the shift button
    action_chain.key_down(Keys.SHIFT)
    action_chain.perform()
    
    # put emojies in order
    for i in range(len(emoji_list)):
        time.sleep(random.uniform(0.5, 1.5)) # !!! 0.5 is the slowest time so the emojis register in the correct order
        driver.find_element(By.CSS_SELECTOR, f"[data-name=\"{emoji_list[i]}\"]").click()
    
    # release the shift button
    action_chain.reset_actions() # note: action_chain.perform() cannot be right before this line instead of where it is right now
    action_chain.key_up(Keys.SHIFT)
    action_chain.perform()
    action_chain.reset_actions()


def click_jump_button(action_chain, tray_message, jump_button):
    
    action_chain.move_to_element(tray_message)
    action_chain.perform()
    action_chain.reset_actions()
    jump_button.click()

def find_jump_button(action_chain, tray_message):
    action_chain.move_to_element(tray_message) # TODO: move_to_element_with_offset didn't work out, is there any other way to skip the jump button?
    action_chain.perform()
    action_chain.reset_actions()
    jump_button = tray_message.find_element(By.CSS_SELECTOR, "div.buttonsContainer-Nmgy7x")
    return jump_button

def handle_new_message_exceptions(first_channel, action_chain, tray_message, jump_button):
    first_channel.click()
    handle_old_message_exceptions(action_chain, tray_message, jump_button)

def handle_old_message_exceptions(action_chain, tray_message, jump_button):
    time.sleep(random.uniform(0.0, 1.0))
    click_jump_button(action_chain, tray_message, jump_button)
    time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out
