from config import NUMBER_OF_ACCOUNTS

def check_on_loan_amounts(driver):
    """
        Assumes we're looking at the overview page
    """
    # for i in range(0, NUMBER_OF_ACCOUNTS):
        # label_div = driver.find_elements_by_xpath('//table[@class="novo-table-content"]/tbody/tr[4]/td[2]')[0]
    cards = driver.find_elements_by_class_name('card')
    loans = []
    for card in cards:
        h3 = card.find_elements_by_css_selector("h3")[1]
        # all_children_by_xpath = header.find_elements_by_xpath(".//*")
        amount = h3.text
        loans.append(amount)
    return loans