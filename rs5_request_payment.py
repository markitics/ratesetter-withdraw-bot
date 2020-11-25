from config import MIN_PAYOUT, WAIT_SECONDS
from utils import wait_approx

def request_payout(driver, payout_amount):
    """
        Assume we're on the right 'withdraw' page.
        Assume the input argument like 14.46 is a sensible amount to be requesting.
    """
    # Enter the amount in the input field
    # moneyInnput = driver.find_element_by_css_selector("input[@class='moneyDecimalFormat']")
    moneyInnput = driver.find_element_by_class_name('moneyDecimalFormat')
    moneyInnput.clear()
    moneyInnput.send_keys(str(payout_amount))
    driver.execute_script("$(`.cta-btn-large`)[0].click()")
    # driver.execute_script("$(`a:contains('Next')`)[0].click()")
    wait_approx(WAIT_SECONDS)
    driver.execute_script("$(`a:contains('Confirm')`)[0].click()")
    # confirm_link = driver.find_element_by_partial_link_text('Confirm')
    # Press Next
    wait_approx(WAIT_SECONDS)
    # extract ref number
    # driver.execute_script("$(`a:contains('Confirm')`)[0].click()")
    # driver.find_element_by_xpath
    try:
        cell = driver.find_elements_by_xpath('//table/tbody/tr[4]/td[2]')[0]
        # cell = driver.find_elements_by_xpath('//table[@class="novo-table-content"]/tbody/tr[4]/td[2]')[0]
        ref = cell.text.replace('\n', '').strip()
    except:
        ref = ''
    # .text
    return {'payout_amount': payout_amount, 'ref': ref}