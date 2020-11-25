from email.message import EmailMessage
# User settings
from config import EMAIL_HOST, EMAIL_PASSWORD, EMAIL_USER, \
    EMAIL_PORT, SENDER, ALL_EMAIL_RECIPIENTS

def send_email(subject, body, sender=SENDER, recipients=ALL_EMAIL_RECIPIENTS, html=''):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = recipients
    message['Subject'] = subject
    message.set_content(body)
    message
    if html:
        message.add_alternative(html, subtype="html")
    import smtplib, ssl
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo() # Can be omitted
    context = ssl.create_default_context()
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    # server.sendmail(EMAIL_USER, receiver_email, message)
    server.send_message(message)


