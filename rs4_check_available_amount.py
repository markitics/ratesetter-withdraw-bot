from utils import wait_approx
from config import WAIT_SECONDS


def read_available_gbp_and_go_to_bank_page_if_possible(driver):
    """
        Assumes we're looking at the 'Withdraw' main page for a particular account.
        Returns 0 if there's no money to withdraw.
        Navigates to the 'to bank' page if possible, where we have the text input to request an amount.
    """
    try:
        driver.execute_script("$(`a:contains('to bank account')`)[0].click()")
        wait_approx(WAIT_SECONDS)
        # print("Now we're on the 'One-Off Withdrawal' page")
        table = driver.find_elements_by_class_name('novo-table-content')
        cell = driver.find_elements_by_xpath('//table[@class="novo-table-content"]/tbody/tr[4]/td[2]')[0]
        amount_string = cell.text.replace('\n', '').strip()
        print("Amount available to withdraw to bank is %s" % amount_string)
        amount_gbp = round(float(amount_string[1:]), 2)
    except IndexError:
        print("No money is available to withdraw.")
        amount_gbp = 0
    return amount_gbp
 