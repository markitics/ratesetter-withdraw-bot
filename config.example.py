# Lines starting with # are comments. 
# You can copy the comments to config.py if you want, but there's no need.
# You can also add your own comments by starting a line with #.

# RATESETTER LOGIN DETAILS
LOGIN_URL = 'https://members.ratesetter.com/login.aspx'
RS_PASSWORD='supersecretabcd1234'                           # <-- Change this
# Comment out one of these lines
# RS_EMAIL, NEXT_PAYOUT_NUMBER =  'wife@gmail.com', 29
RS_EMAIL, NEXT_PAYOUT_NUMBER = 'husband@gmail.com', 1       # <-- Change these

# RateSetter thresholds
# WITHDRAW_URL = 'https://members.ratesetter.com/your_lending/payments/one_off_withdraw.aspx'
OVERVIEW_URL = 'https://members.ratesetter.com/overview.aspx#'
MIN_PAYOUT = 1.00 # If set to 4.00, min payout is 4.00 + payout_number in pennies
# Reminder: if there's 1.25 available, MIN_PAYOUT 1.00, but we're on payout number 30: no money will be withdrawn.
# MIN_PAYOUT should not be set to be less than 1.00.
NUMBER_OF_ACCOUNTS = 2      # e.g., one Everyday and one ISA = 2 accounts
WAIT_SECONDS = 30 # between page loads / clicks
# remember with wait_approx, this is +/- 20%
EMAIL_EVERY_N_ATTEMPTS = 200 # Send email to WEBMASTER_EMAIL regardless of success/fail, so we know bot is still running


# EMAIL SETTINGS
# Alternatively, just turn off email alerts altogether, so you can skip this email setup.

# Email login: for the email that will send you alerts (e.g., gmail)
EMAIL_HOST="smtp.gmail.com"
EMAIL_USER='myname@gmail.com'                               # <-- Change this
EMAIL_PASSWORD="myothersecretpassword"                      # <-- Change this
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

# Email alert details 
sender_name = "RateSetterBot"                               # <-- You can leave this, or change it.
# The name can be 'RateSetter Bot', 'My RS script', or anything at all you like.
SENDER = "%s <%s>" % (sender_name, EMAIL_USER)
ACCOUNT_OWNER_EMAIL= RS_EMAIL.replace('@', '+rsalert@')

# Who should receive the alert emails?
# WEBMASTER_EMAIL will receive the alerts, "Bot ran into a problem" and periodically, "Bot is still running"
# ACCOUNT_OWNER_EMAIL will receive emails, "Successful withdrawal has been made"

# Delete (or comment out) either option 1 or option 2:

# Email alert details - option 1: You're running this script for yourself
WEBMASTER_EMAIL = ACCOUNT_OWNER_EMAIL 
ALL_EMAIL_RECIPIENTS = ACCOUNT_OWNER_EMAIL 

# Email alert details - option 2: You're running this script on behalf of a friend
WEBMASTER_EMAIL = "Mark <techyfriend+rsalert@gmail.com>" 
# WEBMASTER_EMAIL is notified when script hits an error, and occasionally to confirm script still running
ALL_EMAIL_RECIPIENTS = ', '.join([WEBMASTER_EMAIL, ACCOUNT_OWNER_EMAIL]) 
# ALL_EMAIL_RECIPIENTS are notified when a withdrawal happens
