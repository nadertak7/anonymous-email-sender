import smtplib 
import os
from email.message import EmailMessage
def sendMail(email, subject, message):
    
    # Define Constants
    SENDER_EMAIL_ID = str(os.environ.get('SENDER_EMAIL_ID'))
    SENDER_PASSWORD = str(os.environ.get('SENDER_PASSWORD'))

    # Post-process Email
    emailmessage = EmailMessage()
    emailmessage["Subject"] = subject
    emailmessage["From"] = SENDER_EMAIL_ID
    emailmessage["To"] = email
    emailmessage.set_content(message)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(SENDER_EMAIL_ID, SENDER_PASSWORD)
        smtp.send_message(emailmessage)
        smtp.quit()
