
# from emailsend.common import sender, recipients
from emailsend.common import send_email
from config import EMAIL_EVERY_N_ATTEMPTS, WEBMASTER_EMAIL, RS_EMAIL
from utils import nowstring, nowtime, when_yyyymmddhhmm 

def confirm_still_running(loans, attempt_number, payout_number, start_time):
    subject, body  = populate_subject_and_body(loans, \
                        attempt_number, payout_number, start_time)
    html_body = body
    # For fun (and to make emails unique), add an image
    photo_url = 'https://picsum.photos/seed/%s-%s/160' % (start_time, attempt_number)
    html_body += "<br><br>Email ends with an image:<br><img src='%s'/>" % photo_url
    html = "<html><head></head><body>%s</body></html>" % html_body.replace('\n', '<br>')
    recipients = WEBMASTER_EMAIL
    send_email(subject=subject, body=body, html=html, recipients=WEBMASTER_EMAIL) # default sender, recipients

def populate_subject_and_body(loans, attempt_number, payout_number, start_time):
    subject = "👩‍💻 RS bot still running 🏃‍♀️ for %s" % RS_EMAIL.split('@')[0]
    batch_id = when_yyyymmddhhmm(start_time)
    now_time = nowtime()
    delta_seconds = (now_time - start_time).total_seconds()
    avg_cycle_time_seconds = round(delta_seconds / attempt_number, 1)
    body = "💷 Outstanding loan amounts:"
    for loan in loans:
        body += "\n %s" % loan
    body += "\n\n🕵️‍  Searching for bot withdrawal #%s" % payout_number
    body += "\n🔁  Batch %s, cycle #%s" % (batch_id, attempt_number)
    body += "\n\nℹ️  This message is just a confirmation that the bot is still alive and hasn't crashed. "
    body += "\nYou'll receive an email like this periodically "
    body += "(every %s attempts / every ~%s minutes). " \
                % (EMAIL_EVERY_N_ATTEMPTS, round(EMAIL_EVERY_N_ATTEMPTS*avg_cycle_time_seconds / 60))
    body += "Each attempt takes about %s seconds." % avg_cycle_time_seconds
    body += "\nIf these messages stop, perhaps the bot has run into an error or stopped accidentally. "
    body += "Or, check your spam folder. "
    body += "\n\n⌚️ Server time: %s" % nowstring()
    # get the same photo every time for that seed
    return subject, body
