from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random

# USER INPUT
email = input("1/7. Enter your account's email:")
password = input("2/7. Enter your account's password:")
target_person = "from: " + input("3/7. Enter the target person's identifier (example: SampleUser#1234):") + " "
target_server = input("4/7. Enter the target server (example: Sample Server):")
number_of_emojis = input("5/7. Enter the number of emojis to put (example: 4):")
emoji_list = []
for i in range(int(number_of_emojis)):
    if i == 0:
        emoji_list.append(input(f"6/7. Enter the name of the {i + 1} emoji (example: regional_indicator_s. WARNING: order does matter):"))
    else:
        emoji_list.append(input(f"Enter the name of the {i + 1} emoji:"))
number_of_pages = input("7/7. Enter the number of pages to parse (example: 4. To enter all messages type: max. Each page contains 25 messages):")

# set up
chrome_options = webdriver.ChromeOptions()
# hide the automated browser notification
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.maximize_window() # TODO: minimize window
driver.get("https://discord.com/channels/@me")
wait = WebDriverWait(driver, 300)
ac_versatile = ActionChains(driver)

# authorization
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.inputWrapper-1YNMmM.inputWrapper-3ESIDR > input"))).send_keys(email)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.block-3uVSn4.marginTop20-2T8ZJx > div:nth-child(2) > div > input"))).send_keys(password)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F"))).click()
# delete the redundant attributes to save space
del(email)
del(password)

# turn off motion animations
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.button-12Fmur:nth-child(3)"))).click()
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.item-3XjbnG:nth-child(17)"))).click()
wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.container-2nx-BQ")))[1].click()
ac_versatile.send_keys(Keys.ESCAPE)
ac_versatile.perform()
ac_versatile.reset_actions()

# navigate to the target server
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"[aria-label*=\"{target_server}\"]"))).click() 

# get permissions to every visible nsfw channel
all_server_channels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.containerDefault-YUSmu3 > div.iconVisibility-vptxma.wrapper-NhbLHG > div.content-1gYQeQ > a"))) # TODO: try to select only those servers that have little sign above the # (pseudo selectors)
for channel in all_server_channels:
    channel.click()
    list_of_red_buttons = driver.find_elements(By.CSS_SELECTOR, "button.action-3eQ5Or.button-f2h6uQ.lookFilled-yCfaCM.colorRed-rQXKgM.sizeLarge-3mScP9.grow-2sR_-F")
    if len(list_of_red_buttons) != 0:
        list_of_red_buttons[0].click()
# saving the first channel in a list of all channels so we can go back to it if needed
first_channel = all_server_channels[0]
if len(all_server_channels) == 1:
    time.sleep(0.5)
del(channel)
del(all_server_channels)
del(list_of_red_buttons)

# search for the target person
search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.search-39IXmY > div > div > div.DraftEditor-root > div.DraftEditor-editorContainer > div > div > div > div")))
search_bar.click()
search_bar.send_keys(target_person)
search_bar.send_keys(Keys.RETURN)
del(search_bar)

# get the total number of pages to parse
if number_of_pages != "max":
    number_of_pages = int(number_of_pages)
else:
    number_of_pages = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.roundButton-2_R5PN.pageButton-1GMGeJ:nth-child(6) > span'))).text)
# TODO: now the user MUST have more than 5 pages of messages. Fix it

for i in range(number_of_pages):
    # get all messages of the target person in the current page
    tray_of_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.container-rZM65Y")))
    
    # find a message from the tray of messages in the actual chat by its id
    for tray_message in tray_of_messages:
        message_id = tray_message.find_element(By.CSS_SELECTOR, "div > div > div").get_attribute("id")[14:]
        ac_versatile.move_to_element(tray_message) # TODO: move_to_element_with_offset didn't work out, is there any other way to skip the jump button?
        ac_versatile.perform()
        ac_versatile.reset_actions()
        jump_button = tray_message.find_element(By.CSS_SELECTOR, "div.buttonsContainer-Nmgy7x")
        jump_button.click()
        
        # for now dodging the new discord voice channel messages
        if len(driver.find_elements(By.CSS_SELECTOR, "button.joinButton-2KP9ZZ")) != 0:
            current_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"#chat-messages-{message_id}")))
            ac_versatile.context_click(current_message)
            ac_versatile.perform()
            ac_versatile.reset_actions()
            while len(driver.find_elements(By.CSS_SELECTOR, f"[data-name=\"{emoji_list[0]}\"]")) == 0:
                while len(driver.find_elements(By.CSS_SELECTOR, "#message-add-reaction")) == 0:
                    time.sleep(0.5)
                    ac_versatile.context_click(current_message)
                    ac_versatile.perform()
                    ac_versatile.reset_actions()
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#message-add-reaction"))).click()
            # press and hold the shift button
            ac_versatile.key_down(Keys.SHIFT)
            ac_versatile.perform() # note: this line cannot be commented
            for i in range(len(emoji_list)):
                time.sleep(random.uniform(0.5, 1.0)) # !!! 0.5 is the slowest time so the emojis register in the correct order
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-name=\"{emoji_list[i]}\"]"))).click()
            # release the shift button
            ac_versatile.reset_actions()
            ac_versatile.key_up(Keys.SHIFT)
            ac_versatile.perform()
            ac_versatile.reset_actions()
            first_channel.click()

        else:
            # select an exact message by its id in the actual chat
            while len(driver.find_elements(By.CSS_SELECTOR, f"#chat-messages-{message_id}")) == 0:
                ac_versatile.move_to_element(tray_message)
                ac_versatile.perform()
                ac_versatile.reset_actions()
                jump_button.click()
            current_message = driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id}")
    
            # right click a message. If there was an animation bug - repeat
            ac_versatile.context_click(current_message)
            ac_versatile.perform()
            ac_versatile.reset_actions()
            while len(driver.find_elements(By.CSS_SELECTOR, f"[data-name=\"{emoji_list[0]}\"]")) == 0:
                while len(driver.find_elements(By.CSS_SELECTOR, "#message-add-reaction")) == 0:
                    ac_versatile.move_to_element(tray_message)
                    ac_versatile.perform()
                    ac_versatile.reset_actions()
                    jump_button.click()
                    time.sleep(0.5) # !!! 0.3 is the slowest time so the animation doesn't bug out
                    ac_versatile.context_click(current_message)
                    ac_versatile.perform()
                    ac_versatile.reset_actions()
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#message-add-reaction"))).click()
            
            # press and hold the shift button
            ac_versatile.key_down(Keys.SHIFT)
            ac_versatile.perform() # note: this line cannot be commented
            for i in range(len(emoji_list)):
                time.sleep(random.uniform(0.5, 1.0)) # !!! 0.5 is the slowest time so the emojis register in the correct order
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"[data-name=\"{emoji_list[i]}\"]"))).click()
            # release the shift button
            ac_versatile.reset_actions()
            ac_versatile.key_up(Keys.SHIFT)
            ac_versatile.perform()
            ac_versatile.reset_actions()

    # go to the next page
    driver.find_element(By.CSS_SELECTOR, 'button[rel=\'next\']').click()

# driver.quit()

# TODO: new messages

# # ULTRA FAST VERSION___________________________________________________________
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait

# # USER INPUT
# email = input("1/7. Enter your account's email:")
# password = input("2/7. Enter your account's password:")
# target_person = "from: " + input("3/7. Enter the target person's identifier (example: SampleUser#1234):") + " "
# target_server = " " + input("4/7. Enter the target server (example: Sample Server):")
# number_of_emojis = input("5/7. Enter the number of emojis to put (example: 4):")
# emoji_list = []
# for i in range(int(number_of_emojis)):
#     if i == 0:
#         emoji_list.append(input(f"6/7. Enter the name of the {i + 1} emoji (example: regional_indicator_s. WARNING: order does matter):"))
#     else:
#         emoji_list.append(input(f"Enter the name of the {i + 1} emoji:"))
# number_of_pages = input("7/7. Enter the number of pages to parse (example: 4. To enter all messages type: max. Each page contains 25 messages):")

# # set up
# chrome_options = webdriver.ChromeOptions()
# # hide the automated browser notification
# chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
# driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
# driver.maximize_window()
# driver.get("https://discord.com/channels/@me")
# wait = WebDriverWait(driver, 300)
# ac_versatile = ActionChains(driver)

# # authorization
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.inputWrapper-1YNMmM.inputWrapper-3ESIDR > input"))).send_keys(email)
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.block-3uVSn4.marginTop20-2T8ZJx > div:nth-child(2) > div > input"))).send_keys(password)
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F"))).click()
# # delete the redundant attributes to save space
# del(email)
# del(password)

# # turn off motion animations
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.button-12Fmur:nth-child(3)"))).click()
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-3XjbnG:nth-child(17)"))).click()
# wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.container-2nx-BQ")))[1].click()
# ac_versatile.send_keys(Keys.ESCAPE)
# ac_versatile.perform()
# ac_versatile.reset_actions()

# # navigate to the target server
# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[aria-label=\"{target_server}\"]"))).click() 

# # get permissions to every visible nsfw channel
# all_server_channels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.containerDefault-YUSmu3 > div.iconVisibility-vptxma.wrapper-NhbLHG > div.content-1gYQeQ > a")))
# for channel in all_server_channels:
#     channel.click()
#     list_of_red_buttons = driver.find_elements(By.CSS_SELECTOR, "button.action-3eQ5Or.button-f2h6uQ.lookFilled-yCfaCM.colorRed-rQXKgM.sizeLarge-3mScP9.grow-2sR_-F")
#     if len(list_of_red_buttons) != 0:
#         list_of_red_buttons[0].click()
# del(channel)
# del(all_server_channels)
# del(list_of_red_buttons)

# # search for the target person
# search_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-39IXmY > div > div > div.DraftEditor-root > div.DraftEditor-editorContainer > div > div > div > div")))
# search_bar.click()
# search_bar.send_keys(target_person)
# search_bar.send_keys(Keys.RETURN)
# del(search_bar)

# # get the total number of pages to parse
# if number_of_pages != "max":
#     number_of_pages = int(number_of_pages)
# else:
#     number_of_pages = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.roundButton-2_R5PN.pageButton-1GMGeJ:nth-child(6) > span'))).text)

# for i in range(number_of_pages):
#     # get all messages of the target person in the current page
#     tray_of_messages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.container-rZM65Y")))
    
#     # find a message from the tray of messages in the actual chat by its id
#     for tray_message in tray_of_messages:
#         message_id = tray_message.find_element(By.CSS_SELECTOR, "div > div > div").get_attribute("id")[14:]
#         ac_versatile.move_to_element(tray_message)
#         ac_versatile.perform()
#         ac_versatile.reset_actions()
#         jump_button = tray_message.find_element(By.CSS_SELECTOR, "div.buttonsContainer-Nmgy7x")
#         jump_button.click()
        
#         # select an exact message by its id in the actual chat
#         while len(driver.find_elements(By.CSS_SELECTOR, f"#chat-messages-{message_id}")) == 0:
#             ac_versatile.move_to_element(tray_message)
#             ac_versatile.perform()
#             ac_versatile.reset_actions()
#             jump_button.click()
#         current_message = driver.find_element(By.CSS_SELECTOR, f"#chat-messages-{message_id}")

#         # right click a message. If there was an animation bug - repeat
#         ac_versatile.context_click(current_message)
#         ac_versatile.perform()
#         ac_versatile.reset_actions()
#         while len(driver.find_elements(By.CSS_SELECTOR, f"[data-name=\"{emoji_list[0]}\"]")) == 0:
#             while len(driver.find_elements(By.CSS_SELECTOR, "#message-add-reaction")) == 0:
#                 ac_versatile.move_to_element(tray_message)
#                 ac_versatile.perform()
#                 ac_versatile.reset_actions()
#                 jump_button.click()
#                 ac_versatile.context_click(current_message)
#                 ac_versatile.perform()
#                 ac_versatile.reset_actions()
#             wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#message-add-reaction"))).click()
        
#         # press and hold the shift button
#         ac_versatile.key_down(Keys.SHIFT)
#         ac_versatile.perform() # note: this line cannot be commented
#         for i in range(len(emoji_list)):
#             wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-name=\"{emoji_list[i]}\"]"))).click()
#         # release the shift button
#         ac_versatile.reset_actions()
#         ac_versatile.key_up(Keys.SHIFT)
#         ac_versatile.perform()
#         ac_versatile.reset_actions()

#     # go to the next page
#     driver.find_element(By.CSS_SELECTOR, 'button[rel=\'next\']').click()

# # driver.quit()