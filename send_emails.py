import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendEmail(sender, receiver, subject, body, attachment):

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

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "chrisNateSecurityCamera")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()