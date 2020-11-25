# Context

RateSetter is a startup that offered savings acconts based on peer-to-peer lending. But, they ran into financial difficulty and now you can't withdraw your money; there's a queuing system.

<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-queue.png" width="800px" style="border: 1px solid black;">
<br/>
<br/>
<br/>

Understandably, everyday investors <a href="https://twitter.com/search?q=to%3Aratesetter&src=typed_query&f=live">aren't happy</a>.<br/>
<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-tweets-2.png" width="400px" style="border: 1px solid black;">
<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-tweets-1.png" width="400px" style="border: 1px solid black;"> <br/>
<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-tweets-3.png" width="400px" style="border: 1px solid black;">
<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-tweets-4.png" width="400px" style="border: 1px solid black;">

# Purpose of this script: withdraw (some) money ASAP

You want to withdraw as much money from your RateSetter account as possible, but due to their queuing system, you're unable to withdraw your money. You've requested to "release funds", but there are thousands of people ahead of you. You really need to withdraw some of your money asap. Or, you're nervous the company will go under, so you'd rather just have your money back!

<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-stablisation-period.png" width="800px">

> _"The time it is taking investors to access their funds is taking longer than usual"_ ... it can take months! 😮

The goal is to periodically check your RateSetter account, and frequently withdraw small amounts of money.

## Effectiveness

After running the script for about two weeks, the bot made 40 withdrawals. Most withdrawals were close to the minimum (around £2), but we had one withdrawal of ~£7,900. Two others wereover £100.

<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-bot-success.png" width="800px">

## How it works

Due to the way RateSetter works, money is frequently moving between accounts.

The amount of your money "On Loan" changes periodically.

**Key insight/loophole**: If a few pounds are temporarily in "Holding account" or "On market", we can withdraw that money right away. Typically, this is a small amount, like just a few pounds – but it seems to vary.

<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/RateSetter-withdraw-box.png" width="800px" style="border: 1px solid black;">

It's hardly worth logging into RateSetter very often to check if there's £2 here, or £5 there, to be withdrawn. And if we don't log in, the money is quickly loaned out again.

This is the whole point of the bot: immediately spot when there are a few pounds not "on loan", and withdraw them before they're tied up with another borrower.  
If any money is temporarily in "On Holding" or "On Market": the bot will automatically click the "Withdraw" button for you, and then enter the maximum possible amount on the next screen. (Actually, it'll enter an amount a few pennies less than the maximum amount – see "Identifying the withdrawals" section below.) Finally, the bot will send you an email to confirm each time a withdrawal is made.

The bot should keep running on your computer, taking a minute or so to go through one cycle of clicks. At the end of the cycle, it returns to the 'Overview' page, to check for any change. It checks, and can withdraw from, all accounts (e.g., your "Everyday" account and "ISA" account.)

## Identifying the withdrawals in your bank account

To avoid being overwhelmed/confused by a vast number of small (~£2) withdrawals clogging up your bank statement, the bot will set the number of pennies to match the withdrawal number.  
For example, if £25.40 becomes available to withdraw, and the bot is looking to make withdrawal number 12, then only £25.12 will be withdrawn – not the full £25.40 that's available.  
The next time, the bot will withdraw £xx.13.  
This should make it easier to identify the withdrawal amounts hitting your bank account.

<img src="https://markmoriarty.s3.amazonaws.com/img/code/ratesetter/ratesetter-one-off-withdrawal.png" width="800px" style="border: 1px solid black;"> 
<br/>
<br/>

## Set a minimum withdrawal amount

In my experience using this bot, most of the first 25 withdrawals were about £2. One was about £200. Then one was ~£7,900. Boom, the effectiveness of the bot has been validated – this was withdrawn immediately.

If you'd prefer to only look out moments when there's a decent amount of money to withdraw, you should adjust the `MIN_PAYOUT` value in `config.py`.

If `MIN_PAYOUT = 1.00`, then you could have withdrawals as low as £1.01, £1.02, £1.03, etc.

Because the number of pennies matches the withdrawal number, if `MIN_PAYOUT = 2.00`, and we're on payout number 12, but only £2.05 is available to withdraw, then no withdrawal will be made. (There would need to be at least £2.12 available to withdraw.)

I'd recommend leaving the `MIN_PAYOUT` low (e.g., 1.00) to start out (so you see the bot being as active as possible). Then if the small withdrawal amounts are annoying, you can increase this threshold (e.g., to 20). Not, if you make any changes to config.py, you need to stop the bot and re-start the bot, for changes to take effect.

# Instructions

## Set up Safari to allow automation

[Enable](https://support.apple.com/en-ie/guide/safari/sfri20948/mac) the "Develop" menu.  
(If you don’t see the Develop menu in the menu bar, choose Safari > Preferences, click Advanced, then select “Show Develop menu in menu bar”.)  
In the "Develop" menu, click to "Allow Remote Automation".

<img src="https://cdn2.awesound.com/ext/guide/develop-safari-remote-automation.png" height=600>

## Or, use with a different browser

This script (Selenium) works with Chrome, Firefox, Safari (or others). The advantage of Safari is that the web driver is pre-installed on Mac.
But pre-installing the Selenium driver for other browsers is very easy too.  
If you're using anything other than Safari: follow the selenium docs to download the driver for your preferred browser.  
[https://selenium-python.readthedocs.io/installation.html#drivers](https://selenium-python.readthedocs.io/installation.html#drivers)

```python
# Example using Chrome
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument('--headless')
# --headles makes actions invisible
# without --headless, I can follow the script's progress
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('/usr/local/bin/chromedriver', options=chrome_options)
# put path to executable chromedriver as first argument (wherever you downloaded it)
```

Personally, I prefer using Chrome as it's less fidgety (e.g., zoom out or re-size the window).

## Download the code

Run the following in your terminal:

Create a virtual environment with python 3

```
virtualenv rsbot -p python3
cd rsbot
. bin/activate
```

Download the code to your computer

```
git clone https://github.com/markitics/ratesetter-withdraw-bot

```

Install dependencies

```
cd ratesetter-withdraw-bot
pip install -r requirements.txt
```

(I'm typing this from memory - you may need to go up/down a folder to have requirements.txt installed to the virtual environment correctly.)

## Edit the code to personalise for your account

You must personalise:

- Your RateSetter login details
- The email account to send alert emails, or set `SEND_EMAILS` to `False` to not bother with emails. As the script runs, there is a printed output of each attempt, so you don't really need emails if you prefer.

You can optionally personalise:

- How often emails are sent
- The minimum amount worth withdrawing. (I recommend setting this as £1 or £2 to start, to maximise the number of withdrawals; you can increase this threshold later.)

You must create a new file called config.py  
Create a new file config.py, beside config.example.py.
That is, the new file should be in the same directory as config.example.py

Put your own email and password here.
Leave config.example.py untouched, for reference.

Don't be intimidated!  
If you **don't need** email alerts, the `config.py` can be simple enough:

```python
# RateSetter login details
LOGIN_URL = 'https://members.ratesetter.com/login.aspx'
RS_PASSWORD='ratesetterpass123'
RS_EMAIL, NEXT_PAYOUT_NUMBER =  'myname@gmail.com', 1

# RateSetter thresholds
OVERVIEW_URL = 'https://members.ratesetter.com/overview.aspx#'
MIN_PAYOUT = 1.00 # If set to 4.00, min payout is 4.00 + payout_number in pennies
# Reminder: if there's 1.25 available, MIN_PAYOUT 1.00, but we're on payout number 30: no money will be withdrawn.
NUMBER_OF_ACCOUNTS = 2 # e.g., ISA and Everyday
WAIT_SECONDS = 30 # between page loads / clicks
# remember with wait_approx, this is +/- 20%

# Email settings
SEND_EMAILS = False
```

If you **do want email alerts**, your finished `config.py` file will look something like this:

```python
# config.py

# RateSetter login details
LOGIN_URL = 'https://members.ratesetter.com/login.aspx'
RS_PASSWORD='ratesetterpass123'
RS_EMAIL, NEXT_PAYOUT_NUMBER =  'myname@gmail.com', 1 # adjust payout number if you re-start the bot

# RateSetter thresholds
# WITHDRAW_URL = 'https://members.ratesetter.com/your_lending/payments/one_off_withdraw.aspx'
OVERVIEW_URL = 'https://members.ratesetter.com/overview.aspx#'
MIN_PAYOUT = 1.00 # If set to 4.00, min payout is 4.00 + payout_number in pennies
# Reminder: if there's 1.25 available, MIN_PAYOUT 1.00, but we're on payout number 30: no money will be withdrawn.
NUMBER_OF_ACCOUNTS = 2 # e.g. one Everyday and one ISA account = 2 accounts
WAIT_SECONDS = 30 # between page loads / clicks
# remember with wait_approx, this is +/- 20%

SEND_EMAILS=True # set to False (capital F) if you'd like to skip everything below this line
EMAIL_EVERY_N_ATTEMPTS = 200 # Send email regardless of success/fail, so we know bot is still running
# WEBMASTER_EMAIL will receive these alerts

# Email settings
# Email login: for the email that will send you alerts (e.g., gmail)
EMAIL_HOST="smtp.gmail.com"
EMAIL_USER='myname@gmail.com' # might be the same as RS_EMAIL, but might be different
EMAIL_PASSWORD="gmailpass456"
EMAIL_USE_SSL=False # if using port 465
EMAIL_PORT=587 # trying to use TLS
EMAIL_USE_TLS=True # if using port 587
# Note, in order to use your own gmail, you must first allow "insecure apps":
# https://myaccount.google.com/lesssecureapps
# Otherwise the bot's login attempt will fail.
# If you have two-factor authentication set up for Google, this won't work.
# Once you start the bot, check your spam folder. (In gmail, for 'in:spam'.)
# Gmail can see that emails are being sent by a bot, and they look repetitive...
# ...so there's a decent chance your emails will wind up in spam.

# Email alert details - option 1: You're running this script on behalf of a friend
SENDER = "RateSetterBot <%s>" % EMAIL_USER
ACCOUNT_OWNER_EMAIL= RS_EMAIL.replace('@', '+rsalert@')

# Who should receive the alert emails?
# WEBMASTER_EMAIL will receive the alerts, "Bot ran into a problem" and periodically, "Bot is still running"
# ACCOUNT_OWNER_EMAIL will receive emails, "Successful withdrawal has been made"

# Email alert details - option 1: You're running this script for yourself
WEBMASTER_EMAIL = ACCOUNT_OWNER_EMAIL # notified when script hits an error, and occasional
ALL_EMAIL_RECIPIENTS = ACCOUNT_OWNER_EMAIL

# Email alert details - option 2: You're running this script on behalf of a friend
WEBMASTER_EMAIL = "Mark <techyfriend+rsalert@gmail.com>"
ALL_EMAIL_RECIPIENTS = ', '.join([WEBMASTER_EMAIL, ACCOUNT_OWNER_EMAIL])

```

## Alert emails

Who should receive the alert emails?  
`WEBMASTER_EMAIL` will receive the alerts, "Bot ran into a problem" and periodically, "Bot is still running"
`ACCOUNT_OWNER_EMAIL` will receive emails, "Successful withdrawal has been made"

Delete (or comment out) option 1 or option 2 from `config.py`

```
# Email alert details - option 1: You're running this script for yourself
WEBMASTER_EMAIL = ACCOUNT_OWNER_EMAIL # notified when script hits an error, and occasional
ALL_EMAIL_RECIPIENTS = ACCOUNT_OWNER_EMAIL

# Email alert details - option 2: You're running this script on behalf of a friend
WEBMASTER_EMAIL = "Mark <techyfriend+rsalert@gmail.com>"
ALL_EMAIL_RECIPIENTS = ', '.join([WEBMASTER_EMAIL, ACCOUNT_OWNER_EMAIL])


```

## Run the code

Each day you wish to start the code, you must first do `. bin/activate` to activate the virtual python environment,
before launching the python shell.  
If you are in the `rs-withdraw-bot` folder, the command is:

```
. ../bin/activate  # .. goes up to parent folder
```

Open the python shell

```
python
```

In the python shell,

```
>>> from withdraw import keep_trying
```

Do not copy-paste the `>>>` – that's just a visual clue that you're in the "python shell".

Now a Safari (or Chrome) window should launch.
If it looks like Safari is ready to be controlled, go ahead and run the master command to begin the bot:

```
>>> keep_trying() # will send confirmation email once it starts up
```

OR

```
>>> keep_trying(initial_email=False) # default is True
```

If `initial_email=True`, it will email you after 1 attempt, so you can check the email is sending correctly.

By default, to confirm that it hasn't crashed, the bot will email you again every 200 attempts (every `EMAIL_EVERY_N_ATTEMPTS` attempts) – just to let you know it's alive and working away. You can change this setting in `config.py`.

## Restart the bot if it crashes

Perhaps you turn off your computer, or need to re-start the bot.  
In this case, adjust the `NEXT_PAYOUT_NUMBER` in `config.py` to match the next payout number.

Payouts are numbered 1, 2, 3, etc.  
Payout amounts have the corresponding number of pennies, to make it easier to identify the withdrawals on your bank statement.  
For example, the first few withdrawals might be: £29.01, £2.02, £14.03, £210.04, etc.

If you re-start the bot after withdrawal number 4 has been made, you should set `NEXT_PAYOUT_NUMBER = 5` in `config.py`. Then the next withdrawal amount will be £XX.05.

## Adjust spam settings

You should set up a filter so alert emails don't go to spam.  
[https://www.jotform.com/help/404-how-to-prevent-emails-from-landing-in-gmail-s-spam-folder](https://www.jotform.com/help/404-how-to-prevent-emails-from-landing-in-gmail-s-spam-folder)

## Multiple RateSetter accounts

It's easy to have two separate Chrome windows controlled by two separate bots.  
Get the first one going, then open up a new terminal window.

Adjust the login details in `config.py` to reflect the second account:

```
RS_PASSWORD='ratesetterpass321'
RS_EMAIL, NEXT_PAYOUT_NUMBER =  'spousename@gmail.com', 1
# Adjust payout number (from 1 to a higher number) if you re-start the bot, to match next withdrawal number
```

Save your changes to config before you run the `python` command.

# Author

M@rkMoriarty.com  
Twitter [@MbyM](https://twitter.com/MbyM)

## Notes

This was an ad-hoc fun project, my first time playing with Selenium. I have no plans to maintain this or offer support to strangers.  
Not to be used for commercial use.  
Do not reduce the 'wait' periods; do not abuse the RateSetter website. Actually running the script might in fact be forbidden by RateSetter terms of service – check this yourself.

## Support

Any friend who has a cursory knowledge of python should be able to help you get this script running on your computer. Chances are they'll even improve it – this is very rough-and-ready as is!

# Licence

[CC-BY-NC](https://creativecommons.org/licenses/by-nc/2.5/) – not for commercial use.
