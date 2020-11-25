
from emailsend.common import send_email
from config import RS_EMAIL

def email_notification(payout_number, payout_amount, account_index, refnum='', loans=[]):
    subject, body  = populate_subject_and_body(payout_number, \
                    payout_amount, account_index, refnum, loans)
    html_body = body
    photo_url = 'https://picsum.photos/seed/%s-%s/160' % (account_index, payout_amount)
    html_body += "<br><br>Email ends with a random image:<br><img src='%s'/>" % photo_url
    html = "<html><head></head><body>%s</body></html>" % html_body.replace('\n', '<br>')
    send_email(subject, body, html=html) # sends to ALL_EMAIL_RECIPIENTS as per common.py

def populate_subject_and_body(payout_number, payout_amount, account_index, refnum='', loans=[]):
    subject = '🎉 RS withdrawal → 🏦'
    # If running the script a few times for different people, handy to see the person's name in subject line too
    if 'alice' in RS_EMAIL:
        subject += " Alice"
    elif 'bob' in RS_EMAIL:
        subject += " Bob"
    else:
        subject += " %s" % RS_EMAIL.split('@')[0]
    # subject = 'Attempting withdrawal %s: ' % (payout_number)
    body = "Withdrawal #%s: GBP %s requested from " % (payout_number, round(payout_amount, 2))
    if account_index == 0:
        body += "Everyday account. "
        body += "\n\nThis is visible as 'Next Day Money Withdrawal request' "
    elif account_index == 1:
        body += "ISA account. "
        body += "\n\nThis is visible as 'Money moved to your other RS Account' "
    else:
        body += "account #%s. " % account_index
        body += "\nYou could log in to check if you see this withdrawal "
    body += "here: https://members.ratesetter.com/your_lending/account_history.aspx"
    if refnum:
        body += "\n\nRef: %s. " % refnum
    # photo_url = 'https://picsum.photos/seed/%s/160' % refnum
    # get the same photo every time for that seed
    # body += "<img src='%s'/>" % photo_url
    if loans:
        body += "\n\nOutstanding loans:"
        for loan in loans:
            body += "\n  %s" % loan
    return subject, body