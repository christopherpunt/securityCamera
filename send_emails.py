'''
What: send_emails.py allows emails to be sent to and smtp email server
        given the proper parameters described in the sendEmails function.
        This function is used to send an notification email when the
        securityCamera does not recognize a face.
Who: Chris Punt and Nate Herder
When: 04/29/2020
Why: CS 300 Calvin University
'''

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# SendEmails is used to send emails
# sender: sender email address
# receiver: receiver email address
# subject: email subject
# body: email body
# attachment: attachment to be added to email
# smtp: smtp server address
# port: port for smtp server
def sendEmail(sender, receiver, subject, body, attachment, smtp, port):

    fromaddr = sender
    toaddr = receiver
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject # "Failed Authentication Alert"

    body = body

    msg.attach(MIMEText(body, 'plain'))

    filename = attachment
    attachment = open(attachment, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP(smtp, port)
    server.starttls()

    try:
        #retrieve the email password from environment variable
        password = os.getenv('EMAIL_PASSWORD')
        server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    except:
        print("Unable to login to email. Environment Variable EMAIL_PASSWORD \
            required.")
        server.quit()