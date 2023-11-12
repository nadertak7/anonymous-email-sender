# Import Modules
import streamlit as st
import re 
from datetime import datetime

# Set config
st.set_page_config(page_title = "Email Sender", page_icon = "closed-mailbox-with-raised-flag", layout = "wide")

# Import Bespoke Modules from /bespokefunctions/
from bespokefunctions import (  pagestyle as ps, 
                                sendmail as sm, 
                                db, 
                                checkfields as cf, 
                                sessionstatecalcs as ssc
                                )

# From bespokefunctions/hidestreamlitstyle.py
ps.stylePage()

# Initialise Variables
emailsent = False
# Initialise Session State Variables from bespokefunctions/sessionstatecalcs.py
ssc.initialiseSessionStates()

# Title
with st.container():
    left_column, middle_column, right_column = st.columns([0.2, 0.6, 0.4])
    with middle_column:
        st.markdown("## Send an email anonymously 📫")
        st.write("\n")

# Form
with st.container():
    left_column, middle_column, right_column = st.columns([0.2, 0.7, 0.1])
    with middle_column: 
        with st.form("Email Form", clear_on_submit = False):
            email = st.text_input("Their Email Address:", placeholder="Email Address", max_chars = 320)
            subject = st.text_input("Your Subject:", placeholder = "Subject", max_chars = 70)
            message = st.text_area("Your Message:", placeholder = "Message", max_chars = 3000)
            submitted = st.form_submit_button("Send")

# Below code is executed upon submission

# Collects submitted timestamp for metrics
if submitted: 
    submitted_timestamp = (datetime .now()
                                    .strftime("%Y-%m-%d %H:%M:%S"))

with st.container():
    left_column, middle_column, right_column = st.columns([0.2, 0.4, 0.4])
    with middle_column:
        # Protects email sends if not all fields are filled
        if submitted and cf.checkFields(email, subject, message) == False:
            st.error("🛑 One or more fields are not filled out. Please try again.")
        # Protects email sends (via regex) if email address is invalid
        elif submitted and not re.match("[^@]+@[^@]+\.[^@]+", email):
            st.error("🛑 Invalid email. Please try again.")
        # Below block of code executes when all field rules are met
        elif submitted and cf.checkFields(email, subject, message) == True: 
            try:
                # From bespokefunctions/sendmail.py
                sm.sendMail(email, subject, message)
                # From bespokefunctions/db.py
                db.sendToDb(email, subject, message) 
                # Triggers function ssc.calculateSessionStateVars below
                emailsent = True
                # Lets user know if code operations are successful or not
                st.success("✅ Successfully Sent!") 
            except:
                st.error("🛑 Something Went Wrong.")

# Metrics 
with st.container():
    st.write("---")
    st.markdown("### About this app")
    left_column, middle_column, right_column = st.columns([0.4, 0.2, 0.4])
    with left_column:
        st.markdown("##### Current Session")
        # Fetches values from session state calculations in bespokefuncitons/sessionstatecalcs.py
        if emailsent: 
            ssc.calculateSessionStateVars(subject, message, submitted_timestamp)
        # Shows session state variable values 
        st.code(f"Emails Sent: {st.session_state["submit_count_session"]}")
        st.code(f"Last Successful Submission: {st.session_state["last_submitted_timestamp"]}")
        st.code(f"Average Subject Length (Characters): {st.session_state["avg_subject_char_len_session"]}")
        st.code(f"Average Message Length (Characters): {st.session_state["avg_message_char_len_session"]}")
    with right_column:
        st.markdown("##### Total usage statistics (Global)")
        # Fetches values from db queries in bespokefunctions/db.py
        send_count, last_message_sent, avg_subject_length, avg_message_length = db.readFromDb()
        # Shows query results (Post-processed in bespokefunctions/db.py)
        st.code(f"Emails Sent: {send_count}")
        st.code(f"Last Message Sent: {last_message_sent}")
        st.code(f"Average Subject Length (Characters): {avg_subject_length}")
        st.code(f"Avg Message Length (Characters): {avg_message_length}")