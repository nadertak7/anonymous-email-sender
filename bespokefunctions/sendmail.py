# Import Modules
import smtplib 
import os
from email.message import EmailMessage

# Takes input variables in homepage and environemnt variables to post-process and fire out email
def sendMail(email, subject, message):    
    # Define Constants (only needs local scope (for now))
    SENDER_EMAIL_ID = str(os.environ.get('SENDER_EMAIL_ID'))
    SENDER_PASSWORD = str(os.environ.get('SENDER_PASSWORD'))

    # Post-process input variables
    emailmessage = EmailMessage()
    emailmessage["Subject"] = subject
    emailmessage["From"] = SENDER_EMAIL_ID
    emailmessage["To"] = email
    emailmessage.set_content(message)

    # Establish connection to mail server
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        # Encrypt
        smtp.starttls()
        # Login
        smtp.login(SENDER_EMAIL_ID, SENDER_PASSWORD)
        # Sends message
        smtp.send_message(emailmessage)
        # Quit
        smtp.quit()
