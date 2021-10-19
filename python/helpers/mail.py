from os import getenv 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

user = getenv('MAIL_USER')
app_key = getenv('MAIL_PWD')

def send_mail(subject, body): 
    message = MIMEMultipart()
    message['From'] = user
    message['To'] = user
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(user, app_key)
    text = message.as_string()
    session.sendmail(user, user, text)
    session.quit()