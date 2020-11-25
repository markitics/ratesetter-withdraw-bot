from selenium import webdriver

def get_webdriver(browser_name='Safari'):
    print("Will use %s" % browser_name)
    if browser_name == 'Chrome':
        return get_chrome_driver()
    return get_safari_driver()

def get_chrome_driver():
    # Options only necessary for Chrome
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    # chrome_options.add_argument('--headless') 
    # --headles makes actions invisible
    # without --headless, I can follow the script's progress
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # Chrome Driver must be downloaded from https://www.selenium.dev/documentation/en/webdriver/driver_requirements/
    return webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)

def get_safari_driver():
    # Safari is pre-installed
    return webdriver.Safari()

