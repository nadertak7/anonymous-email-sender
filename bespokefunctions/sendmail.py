# Import Modules
import smtplib 
import os
from email.message import EmailMessage

# Takes input variables in homepage and environemnt variables to post-process and fire out email
def sendMail(email, subject, message, uploaded_file = None):    
    # Define Constants (only needs local scope (for now))
    SENDER_EMAIL_ID = str(os.environ.get('SENDER_EMAIL_ID'))
    SENDER_PASSWORD = str(os.environ.get('SENDER_PASSWORD'))

    # Post-process input variables
    emailmessage = EmailMessage()
    emailmessage["Subject"] = subject
    emailmessage["From"] = SENDER_EMAIL_ID
    emailmessage["To"] = email
    emailmessage.set_content(message)

    # Handles attachments 
    if uploaded_file is not None:
        for file in uploaded_file:
            attachment_data = file.read()
            attachment_name = file.name
            emailmessage.add_attachment(attachment_data, maintype = "application", subtype ="octet-stream", filename = attachment_name)

    # Establish connection to mail server
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # Encrypt
    smtp.starttls()
    # Login
    smtp.login(SENDER_EMAIL_ID, SENDER_PASSWORD)
    # Sends message
    smtp.send_message(emailmessage)
    # Quit
    smtp.quit()
