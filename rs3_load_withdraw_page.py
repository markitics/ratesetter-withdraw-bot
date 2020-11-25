import random
from utils import wait_approx 
from config import NUMBER_OF_ACCOUNTS, WAIT_SECONDS

def go_to_withdraw_page(driver, account_index=1):
    # Next, click "View" on the relevant account
    # OLD WAY: Randomly pick an account to look at
    # Assume we're interested in the second account
    # account_index = int(random.random() * (NUMBER_OF_ACCOUNTS-1) + .7) 
    # if NUMBER_OF_ACCOUNTS == 2, then this is 0 or 1, biased toward the latter
    # NEW WAY: Feed in the integer index. Elsewhere, set this to alternate.
    print("Look at account #%s" % account_index)
    driver.execute_script("$('.cta-btn-large')[%s].click();" % account_index)
    wait_approx(WAIT_SECONDS)
    # Ignore the table on this page
    # print('Click the "Withdraw" button')
    driver.execute_script("$(`a:contains('Withdraw')`)[0].click()")
    wait_approx(WAIT_SECONDS)
    # print("Next step: check if 'to bank' is an option")
