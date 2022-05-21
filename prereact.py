from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def authorize(wait, email, password):
    
    # authorization
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.inputWrapper-1YNMmM.inputWrapper-3ESIDR > input"))).send_keys(email)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.block-3uVSn4.marginTop20-2T8ZJx > div:nth-child(2) > div > input"))).send_keys(password)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.marginBottom8-emkd0_.button-1cRKG6.button-f2h6uQ.lookFilled-yCfaCM.colorBrand-I6CyqQ.sizeLarge-3mScP9.fullWidth-fJIsjq.grow-2sR_-F"))).click()


def turn_off_animations(wait, action_chain):
    
    # turn off motion animations
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flex-2S1XBF > [aria-label=\"User Settings\"]"))).click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-controls=\"accessibility-tab\"]"))).click()
    wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.container-2nx-BQ")))[2].click()
    action_chain.send_keys(Keys.ESCAPE)
    action_chain.perform()
    action_chain.reset_actions()


def navigation_and_permissions(wait, target_server, driver):
    
    # navigate to the target server
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"[aria-label*=\"{target_server}\"]"))).click() 
    
    # get permissions to every visible nsfw channel
    all_server_channels = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.containerDefault-YUSmu3 > div.iconVisibility-vptxma.wrapper-NhbLHG > div.content-1gYQeQ > a"))) # TODO: try to select only those servers that have little sign above the # (pseudo selectors)
    for channel in all_server_channels:
        channel.click()
        try:
            driver.find_element(By.CSS_SELECTOR, "button.action-3eQ5Or.button-f2h6uQ.lookFilled-yCfaCM.colorRed-rQXKgM.sizeLarge-3mScP9.grow-2sR_-F").click()
        except NoSuchElementException:
            pass
    
    # saving the first channel in a list of all channels so we can go back to it if needed
    first_channel = all_server_channels[0]
    return first_channel


def search_for_person(wait, target_person):
    
    search_bar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.search-39IXmY > div > div > div.DraftEditor-root > div.DraftEditor-editorContainer > div > div > div > div")))
    search_bar.click()
    search_bar.send_keys(target_person)
    search_bar.send_keys(Keys.RETURN)

def get_number_of_pages(wait, number_of_pages):
    
    # get the total number of pages to parse
    if number_of_pages != "max":
        number_of_pages = int(number_of_pages)
    else:
        number_of_pages = int(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.roundButton-2_R5PN.pageButton-1GMGeJ:nth-child(6) > span'))).text)
    return number_of_pages
    # TODO: now the user MUST have more than 5 pages of messages. Fix it
