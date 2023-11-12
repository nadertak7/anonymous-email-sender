import streamlit as st 
import os 
from datetime import datetime
from sqlalchemy import text

# Establish connection
conn = st.connection('mysql', type='sql')

# Define constants
SENDER_EMAIL_ID = str(os.environ.get('SENDER_EMAIL_ID'))

def sendToDb(email, subject, message):
    # Queries that are executed when submit button is pressed
    email_sent_log_query = text(   '''
                    INSERT INTO     email_sent_log (email_sender, 
                                                    email_receiver, 
                                                    created_at)
                    VALUES (        :sender_email_id, 
                                    :email, 
                                    :created_at)
                                    ''')
    
    email_contents_query = text('''
                    INSERT INTO    email_contents (email_sent_log_id, 
                                                    email_subject,
                                                    email_message)
                        VALUES (    :log_id,
                                    :subject,
                                    :message)
                                    ''')

    # Values inputted in said query
    email_sent_log_values = {
        'sender_email_id': SENDER_EMAIL_ID,
        'email': email,
        'created_at': datetime.now()
    }

    email_contents_values = {
        'log_id': None,
        'subject': subject,
        'message': message
    }
    
    # Streamlit's way of performing queries that write to a database
    with conn.session as session:
        # Executes email_sent_log insert
        email_sent_log_execution = session.execute(email_sent_log_query, email_sent_log_values)
        # Populates email_contents.email_log_id FK 
        log_id = email_sent_log_execution.lastrowid
        email_contents_values["log_id"] = log_id
        # Executes eamil_contents insert 
        session.execute(email_contents_query, email_contents_values)
        # Commit
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
                                SELECT 		AVG(CHAR_LENGTH(email_message)) message_char_length,
                                            AVG(CHAR_LENGTH(email_subject))subject_char_length
                                FROM		email_contents
                                ''')
    
    # Post-Process Query Results
    send_count = int(send_count.values[0])
    last_message_sent = str(last_message_sent.values[0])[2:-2]
    # ([variable] or 0) returns first truthy value
    avg_subject_length = round((avg_char_lengths.iloc[0]["subject_char_length"] or 0), 2) 
    avg_message_length = round((avg_char_lengths.iloc[0]["message_char_length"] or 0), 2)

    # Pack variables into tuple, to be unpacked in homepage
    return (send_count, 
            last_message_sent, 
            avg_subject_length, 
            avg_message_length
            )