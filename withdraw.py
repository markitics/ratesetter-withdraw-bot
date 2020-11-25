
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils import wait_approx, nowstring, calculate_payout_amount, randomString, nowtime 
from utils.timing import as_duration
from rs1_login import go_to_overview_page
from rs2_check_loan_amounts import check_on_loan_amounts
from rs3_load_withdraw_page import go_to_withdraw_page
from rs4_check_available_amount import read_available_gbp_and_go_to_bank_page_if_possible
from rs5_request_payment import request_payout
from emailsend.withdrawal_alert import email_notification
from emailsend.im_alive import confirm_still_running
from emailsend.report_error import send_error_email
from driver import get_webdriver

import os
import time
from config import OVERVIEW_URL, NUMBER_OF_ACCOUNTS, SEND_EMAILS, \
            EMAIL_EVERY_N_ATTEMPTS, WAIT_SECONDS, NEXT_PAYOUT_NUMBER, RS_EMAIL, LOGIN_URL


# Keep track of these variables for the email
payout_number = NEXT_PAYOUT_NUMBER # if it crashes, we'll manually set this to be higher
account_index = 1 # goes between 0 and NUMBER_OF_ACCOUNTS
# payouts = []
loans = [None]*NUMBER_OF_ACCOUNTS

# try:
#     driver
# except NameError:
#     driver = get_webdriver()
#     print("well, it WASN'T defined after all!")
# else:
#     print("sure, it was defined.")

browser_name = 'Chrome' # if 'bob' in RS_EMAIL else 'Safari'
print("Will check for %s, looking for payout %s" % (RS_EMAIL, payout_number))
driver = get_webdriver(browser_name)
if browser_name == 'Safari':
    # Chrome can be manipulated while it runs, but Safari can't, so do zooming now.
    driver.set_window_size(1200, 1000) # width, height
    driver.get(LOGIN_URL) # we need to have some page loaded before we zoom
    # print("Resizing window, no this won't work once next page loads, hrm...")
    # wait_approx(4)
    # driver.execute_script("document.body.style.zoom='70%'") # useless before first page loads


def cycle_account_index(account_index):
    account_index += 1
    account_index = account_index % NUMBER_OF_ACCOUNTS
    return account_index


def try_withdraw(attempt_number=1):
    global account_index 
    account_index = cycle_account_index(account_index)
    global payout_number
    go_to_overview_page(driver)
    global loans
    loansnow = check_on_loan_amounts(driver)
    print("Outstanding amounts are: %s" % (loansnow))
    if attempt_number == 1:
        loans = loansnow
    elif loansnow == loans:
        # print("There's been no update, could return False if we've already checked ALL accounts.")
        if attempt_number > 3*NUMBER_OF_ACCOUNTS: # 3 is an arbitrary buffer, could do anything >=1x 
            print("On overview page, can already see there's been no update, amount 'on loan' unchanged for each account. ")
            # SHOULD BE safe to stop clicking through now, 
            # just keep re-loading the overview age and look for one of the 'on loan' amounts to change.
            # return False
            # BUT, one major withdrawal was missed - do I have a bug in the hacky loansnow==loans logic?
            # Just in case, crack on every time and try to withdraw (don't return False here)
    else:
        print("Great! The amount 'on loan' has changed.")
        # Warning, we don't want to set loans = loansnow,
        # in case 'on loan' has changed for more than one account
        # This try_withdraw loop only attempts to withdraw from ONE account,
        # so only update that loan amount in the global variable loans
        for i in range(0, NUMBER_OF_ACCOUNTS):
            # Focus on the right account, by checking which loan amount has changed
            if loansnow[i] != loans[i]:
                account_index = i
                loans[i] = loansnow[i]
                break # so rest of global loans list isn't updated yet
    go_to_withdraw_page(driver, account_index)
    # iff there's more than GBP 0.00 available,
    # it gives us a choice between "release funds" or "withdraw to bank account"
    amount_gbp = read_available_gbp_and_go_to_bank_page_if_possible(driver) # may be 0
    if not amount_gbp:
        print("Trying for payout_number %s: not yet; amount_gbp is zero" % payout_number)
        return False
    payout_amount = calculate_payout_amount(amount_gbp, payout_number) # may be 0
    if payout_amount:
        print("payout_number %s: We should put %s into the field and submit" % (payout_number, payout_amount))
        result = request_payout(driver, payout_amount)
        if SEND_EMAILS:
            email_notification(payout_number, payout_amount, \
                account_index, refnum=result['ref'], loans=loans)
        payout_number += 1
        return True
    else:
        # print("No need to request a payout now")
        return False
    # print("That was attempt_number %s" % attempt_number)



def keep_trying(initial_email=True):
    start_time = nowtime()
    attempt_number = 1
    while attempt_number<1000000:
        try:
            # global attempt_number
            requested_withdrawal = try_withdraw(attempt_number=attempt_number)
            if requested_withdrawal:
                print("Attempted withdrawal! That was attempt_number %s" % attempt_number)
            else:
                print("No withdrawal. That was attempt_number %s" % attempt_number)
            if SEND_EMAILS:
                if (attempt_number == 1 and initial_email) or (attempt_number % EMAIL_EVERY_N_ATTEMPTS == 0):
                    print("SEND EMAIL to confirm the script is still running")
                    global loans
                    global payout_number
                    confirm_still_running(loans=loans, \
                        attempt_number=attempt_number, payout_number=payout_number,
                        start_time=start_time)
            now_time = nowtime()
            delta = now_time - start_time
            delta_string = as_duration(delta.total_seconds())
            print("%s attempts in %s" % (attempt_number, delta_string))
            print("Now %s" % nowstring())
            print(' ')
            wait_approx(WAIT_SECONDS)
            attempt_number += 1
        except Exception as error:
            if SEND_EMAILS:
                send_error_email(error)
            wait_approx(WAIT_SECONDS * 2)


