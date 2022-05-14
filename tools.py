from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def put_emojies(action_chain, list_with_emojis, wait):
    # press and hold the shift button
    action_chain.key_down(Keys.SHIFT)
    action_chain.perform() # note: this line cannot be commented
    for i in range(len(list_with_emojis)):
        time.sleep(random.uniform(0.5, 1.5)) # !!! 0.5 is the slowest time so the emojis register in the correct order
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-name=\"{list_with_emojis[i]}\"]"))).click()
    # release the shift button
    action_chain.reset_actions()
    action_chain.key_up(Keys.SHIFT)
    action_chain.perform()
    action_chain.reset_actions()

def wait_and_click(action_chain, current_message, message_id, wait):
    time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out 
    action_chain.move_to_element(current_message)
    action_chain.perform()
    action_chain.reset_actions()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"#chat-messages-{message_id} > div > div.buttonContainer-1502pf > div.buttons-3dF5Kd > div > [aria-label=\"Add Reaction\"]"))).click()
    # TODO: try not to pass message_id here and get it from current_message object instead