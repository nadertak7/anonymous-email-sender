import streamlit as st 
import os 
from datetime import datetime
from sqlalchemy import text

# Establish connection
conn = st.connection('mysql', type='sql')

# Define constants
SENDER_EMAIL_ID = str(os.environ.get('SENDER_EMAIL_ID'))

def sendToDb(email, subject, message):
    # Query that is executed when submit button is pressed
    query = text(   '''
                    INSERT INTO     email_sent_log (email_sender, 
                                                    email_receiver, 
                                                    email_subject, 
                                                    email_contents, 
                                                    created_at)
                    VALUES (        :sender_email_id, 
                                    :email, 
                                    :subject, 
                                    :message, 
                                    :created_at)
                                    ''')

    # Values inputted in said query
    values = {
        'sender_email_id': SENDER_EMAIL_ID,
        'email': email,
        'subject': subject,
        'message': message,
        'created_at': datetime.now()
    }
    
    # Streamlit's way of performing queries that write to a database
    with conn.session as session:
        session.execute(query, values)
        session.commit()

def readFromDb():
    # Database queries 
    send_count = conn.query(''' 
                            SELECT      COUNT(*)
                            FROM        email_sent_log 
                            ''', ttl = 0)
    last_message_sent = conn.query('''
                                    SELECT      DATE_FORMAT(MAX(created_at), '%Y-%m-%d %T')
                                    FROM        email_sent_log
                                   ''', ttl = 0)
    avg_char_lengths = conn.query('''
                                SELECT 		AVG(CHAR_LENGTH(email_contents)) message_char_length,
                                            AVG(CHAR_LENGTH(email_subject))subject_char_length
                                FROM		email_sent_log 
                                ''')
    
    # Post-Process Query Results
    send_count = int(send_count.values[0])
    last_message_sent = str(last_message_sent.values[0])[2:-2]
    avg_subject_length = avg_char_lengths.iloc[0]["subject_char_length"].round(2)
    avg_message_length = avg_char_lengths.iloc[0]["message_char_length"].round(2)

    # Pack variables into tuple, to be unpacked in homepage
    return (send_count, 
            last_message_sent, 
            avg_subject_length, 
            avg_message_length
            )