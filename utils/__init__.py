import time
from config import MIN_PAYOUT 
from datetime import datetime
import random # to randomise waiting and which account we look at
import string # for randomString


def approx(n_seconds, fraction=0.2):
    # wait that many seconds, plus or minus 20%
    min_wait = n_seconds * (1 - fraction) # 0.8
    max_wait = n_seconds * (1 + fraction) # 1.2
    random_bit = (max_wait-min_wait) * random.random()
    return min_wait + random_bit

def wait_approx(n_seconds):
    # print("Wait for about %s seconds" % n_seconds)
    time.sleep(approx(n_seconds))

def nowtime():
    return datetime.utcnow()

def nowstring():
    # return "%s-%02d-%02d %02d:%02d %s"  % (time.year, time.month, time.day, time.hour, time.minute, time.tzinfo)
    # return nowtime.strftime('%Y-%m-%d %H:%M:%s')
    return when_including_seconds(nowtime())

def when_including_seconds(time):
    # return "%s-%s-%s @ %s:%s:%s %s" % (time.year, time.month, time.day,
    #             time.hour, time.minute, time.second, time.tzinfo)
    return "%s-%02d-%02d @ %02d:%02d:%02d UTC"  % (time.year, time.month, time.day,
                time.hour, time.minute, time.second) # , time.tzinfo


def when_yyyymmddhhmm(time):
    # return "%s-%s-%s @ %s:%s:%s %s" % (time.year, time.month, time.day,
    #             time.hour, time.minute, time.second, time.tzinfo)
    return "%s-%02d-%02d %02d:%02d"  % (time.year, time.month, time.day,
                time.hour, time.minute) # , time.tzinfo


def calculate_payout_amount(gbp_available, payout_number):
    """
        Input gbp_available is a float like 14.46 (representing GBP 14.46).
        gbp_available is the maximum we're allowed withdraw right now.

        Function returns a value slightly less than the gbp_availabe, 
        where the number after the decimal point (number of pennies)
        matches the payout_number.
        This is to make withdrawals easier to track in our bank statement.
        Withdrawal amounts will look like XX.01, XX.02, XX.03, XX.04, etc. 
    """
    if gbp_available > MIN_PAYOUT + 1.00:
        print("We have an amount worth withdrawing")
    else:
        print("Nothing worth withdrawing")
        return 0
    pennies_to_withdraw = payout_number % 100
    # payout_number might be >100
    pennies_available = int((gbp_available % 1) * 100) # 
    if pennies_available > pennies_to_withdraw:
        # if 14.55 is available and we're on payout #8, request 14.08
        payout_amount = round(int(gbp_available) + pennies_to_withdraw/100, 2)
    else: # if 14.05 is available but we're on payout #8, request 13.08
        payout_amount = round(int(gbp_available-1) + pennies_to_withdraw/100, 2)
    return payout_amount


def randomString(length):
    """
        Input 'length' is length of string in characters.
        Characters are lower case letters and digits (no upper case characters).
        Output looks like "jwin9k58r" when length is 9.
        Avoid l, i, o, 0, 1.
        23 possible letters and 8 possible digits.
        Choice of 32 different characters:
        31^3 =         29  k
        31^4 =        923  k
        31^5 =     28      million
        31^6 =    888      million
        31^7 = 27          billion
    """
    # Some people sometimes confuse 1 and l, so avoid both:
    eligible_lettes = string.ascii_lowercase.replace('i', '').replace('l', '').replace('o', '') 
    # = 'abcdefghjkmnpqrstuvwxyz', no 'i', 'l', 'o'
    # Also avoid 'o' and '0'
    eligible_numbers = '23456789' # no 0, 1
    eligible_chars = eligible_lettes + eligible_numbers # 'abc...jkmn..xyz234..789' # no i/l/o/0/1
    return ''.join(random.choice(eligible_chars) for i in range(length))
