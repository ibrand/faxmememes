import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

def send_email(email_recipient,
               email_subject,
               email_message,
               attachment_location = ''):

    email_sender = os.environ['SENDER_EMAIL']

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = email_subject

    if email_message:
        msg.attach(MIMEText(email_message, 'plain'))

    if attachment_location != '':
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP(host="mail.gandi.net", port=587)
        server.ehlo()
        server.starttls()
        server.login(os.environ['SENDER_EMAIL'], os.environ['SENDER_PASSWORD'])
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        print('email sent')
        server.quit()
    except:
        print("SMTP server connection error")
    return True

send_email(os.environ['RECEIVER_EMAIL'],
           'Your weekly meme digest',
           '',
           'memes/tyler.jpeg')