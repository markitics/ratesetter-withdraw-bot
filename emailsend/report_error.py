
from emailsend.common import send_email
from config import WEBMASTER_EMAIL

def send_error_email(error=None):
    """
        Optional error argument is a python error object.
    """
    subject, body  = populate_subject_and_body(error)
    # custom_recipients = "MarkOnly <m@rkmoriarty.com>, MarkAwe <mark@awesound.com>"
    send_email(subject, body, recipients=WEBMASTER_EMAIL)


def populate_subject_and_body(error=None):
    """
        Optional error argument is a python error object.
    """
    subject = '⚠️ RateSetter bot fail 😯 '
    # subject = 'Attempting withdrawal %s: ' % (payout_number)
    body = ''
    if error:
        try:
            error_msg = error.msg # 
            # so now we can look up .message
        except:
            error_msg = error
        # print("error is ")
        # print(error)
        print("error.__dict__ is ")
        print(error.__dict__)
        if type(error_msg) == str:
            body += error_msg + " \n\n"
    body += "Check the script. "\
        + "One particular attempt failed, "\
        + "but we're hopefully still iterating through the while loop. "
    return subject, body