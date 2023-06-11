import yagmail
import os
from dotenv import load_dotenv



def send_mail(receiver, subject, content):
    load_dotenv()

    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    with yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD) as yag:
        yag.send(receiver, subject, content)

# send_mail("thecodizt@gmail.com", "Hello", "Hi")        