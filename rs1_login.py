from utils import wait_approx 
from selenium.webdriver.common.keys import Keys
# import os
# RS_EMAIL = os.environ.get('RS_EMAIL')
from config import RS_EMAIL, RS_PASSWORD, LOGIN_URL

def go_to_overview_page(driver):
    # Safari webdriver is built-in!
    driver.get(LOGIN_URL)
    wait_approx(8)
    # driver.get(OVERVIEW_URL)
    meta_description = driver.find_element_by_xpath("//meta[@name='description']").get_attribute('content')
    # print(meta_description)
    if 'Sign in' in meta_description:
        # move to second monitor
        # driver.maximize_window()
        emailInput = driver.find_element_by_id("txtEmailNew")
        emailInput.clear()
        emailInput.send_keys(RS_EMAIL)
        pwInput = driver.find_element_by_css_selector("input[type='password']")
        pwInput.clear()
        pwInput.send_keys(RS_PASSWORD)
        # Submit the form:
        pwInput.send_keys(Keys.RETURN)
        print("Wait a few seconds for log in to complete...")
        wait_approx(8)
    else:
        # print("Already signed in, we've been redirected to overview")
        wait_approx(1)

