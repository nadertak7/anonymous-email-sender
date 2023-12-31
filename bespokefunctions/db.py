import streamlit as st 
import os 
from datetime import datetime
from sqlalchemy import text

# Establish connection
conn = st.connection('mysql', type='sql')

# Define constants
SENDER_EMAIL_ID = str(os.environ.get('SENDER_EMAIL_ID'))

def sendToDb(email, 
             subject, 
             message,  
             filter_profanity, 
             subject_contains_profanity, 
             message_contains_profanity,
             uploaded_file = None):
    # Queries that are executed when submit button is pressed
    email_sent_log_query = text(   '''
                    INSERT INTO     email_sent_log( email_sender, 
                                                    email_receiver, 
                                                    created_at)
                    VALUES (        :sender_email_id, 
                                    :email, 
                                    :created_at)
                                    ''')
    
    email_contents_query = text('''
                    INSERT INTO    email_contents(  email_sent_log_id, 
                                                    email_subject,
                                                    email_message)
                        VALUES (    :log_id,
                                    :subject,
                                    :message)
                                    ''')
    
    email_attachments_query = text('''
                    INSERT INTO     email_attachments(  email_sent_log_id,
                                                        email_attachment_name,
                                                        mime_type,
                                                        attachment_size_bytes)
                        VALUES (    :log_id,
                                    :attachment_name,
                                    :mime_type,
                                    :attachment_size)
                                    ''')
    
    email_profanity_query = text('''
                    INSERT INTO     email_profanity(    email_sent_log_id,
                                                        filter_profanity_selected,
                                                        subject_contains_profanity, 
                                                        message_contains_profanity)
                        VALUES (    :log_id,
                                    :filter_profanity, 
                                    :subject_contains_profanity,
                                    :message_contains_profanity)
                                    ''')
    
    # Streamlit's way of performing queries that write to a database
    with conn.session as session:
       
        # Executes email_sent_log insert with values 
        email_sent_log_values = {
            'sender_email_id': SENDER_EMAIL_ID,
            'email': email,
            'created_at': datetime.now()
    }

        email_sent_log_execution = session.execute(email_sent_log_query, 
                                                   email_sent_log_values)
       
        # Initialises email_sent_log ID FK
        log_id = email_sent_log_execution.lastrowid

        # Executes email_contents insert with values 
        email_contents_values = {
            'log_id': log_id,
            'subject': subject,
            'message': message
            }
        
        session.execute(email_contents_query, 
                        email_contents_values)

        # Executes email_attachments insert with values
        for file in uploaded_file:
            email_attachments_values = {
                'log_id': log_id, 
                'attachment_name': file.name,
                'mime_type': file.type,
                'attachment_size': file.size 
                }
            
            session.execute(email_attachments_query, 
                            email_attachments_values)

        # Executes email_profanity insert with values
        email_profanity_values = {
            'log_id': log_id,
            'filter_profanity': filter_profanity,
            'subject_contains_profanity': subject_contains_profanity,
            'message_contains_profanity': message_contains_profanity
        }

        session.execute(email_profanity_query, 
                        email_profanity_values)

        # Commit
        session.commit()

def readFromDb():
    # Database queries. Caching is disabled as queries are not costly. 
    send_info = conn.query(''' 
                            SELECT      COUNT(0) send_count,
                                        COALESCE(DATE_FORMAT(MAX(created_at), '%Y-%m-%d %T'), "None") last_message_sent
                            FROM        email_sent_log 
                            ''', ttl = 0)
    
    # Rounding has been manipulated in MySQL to imitate python's rounding
    avg_char_lengths = conn.query('''
                                 SELECT 		CASE 	WHEN CHAR_LENGTH(message_char_length) = 1
                                                        THEN message_char_length
                                                        WHEN CHAR_LENGTH(message_char_length) = 3
                                                        THEN ROUND(message_char_length, 1)
                                                        ELSE ROUND(message_char_length, 2) 
                                                END 	message_char_length,
                                                CASE 	WHEN CHAR_LENGTH(subject_char_length) = 1
                                                        THEN subject_char_length
                                                        WHEN CHAR_LENGTH(subject_char_length) = 3
                                                        THEN ROUND(subject_char_length, 1)
                                                        ELSE ROUND(subject_char_length, 2) 
                                                END 	subject_char_length
                                FROM (		SELECT 		COALESCE(TRIM(0 FROM AVG(CHAR_LENGTH(TRIM(email_message)))), 0) message_char_length,
                                                        COALESCE(TRIM(0 FROM AVG(CHAR_LENGTH(TRIM(email_subject)))), 0) subject_char_length
											FROM		email_contents ) t
                                ''', ttl = 0)
    
    attachment_info = conn.query('''
                                SELECT		COUNT(0) attachment_count,
                                            COALESCE(AVG(attachment_size_bytes), 0) avg_attachment_size
                                FROM		email_attachments
                                  ''', ttl = 0)
    
    emails_censored_count = conn.query('''
                                SELECT 		COALESCE(CONCAT(	censored_message_count,
                                            ' (',
                                            ROUND(100 * censored_message_count / total_email_count, 2),
                                            '%)'), '0 (0%)') censored_message_count
                                FROM (		SELECT 		SUM(CASE 	WHEN filter_profanity_selected = 1
                                                                    AND (subject_contains_profanity = 1
                                                                    OR message_contains_profanity = 1)
                                                                    THEN 1
                                                                    ELSE 0
                                                                    END) censored_message_count, 
                                                        COUNT(0) total_email_count
                                            FROM 		email_profanity) t

                                ''', ttl = 0)
    
    # Post-Process Query Results
    send_count = send_info.iloc[0]["send_count"]
    last_message_sent = str(send_info.iloc[0]["last_message_sent"])
    attachment_count = int((attachment_info.iloc[0]["attachment_count"]))
    avg_attachment_size_mb = round(attachment_info.iloc[0]["avg_attachment_size"] / 1024 ** 2, 2)
    avg_subject_length = (avg_char_lengths.iloc[0]["subject_char_length"])
    avg_message_length = (avg_char_lengths.iloc[0]["message_char_length"])
    emails_censored_count = str(emails_censored_count.values[0])[2:-2]

    # Pack variables into tuple, to be unpacked in homepage
    return (send_count, 
            last_message_sent, 
            attachment_count,
            avg_attachment_size_mb,
            avg_subject_length, 
            avg_message_length,
            emails_censored_count)