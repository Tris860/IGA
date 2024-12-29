from flask_mail import Message
from . import mail  # Import the mail instance from your __init__.py


def send_email(subject, recipients, body):
   try:
     msg = Message(subject, recipients=recipients)
     msg.body = body
     mail.send(msg)
     return[True]
   except Exception as e:
       print(e)
       return [False,e]