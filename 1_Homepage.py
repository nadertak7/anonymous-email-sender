# Import Modules
import streamlit as st
import re 
from datetime import datetime 

# Set config
st.set_page_config(page_title = "Email Sender", page_icon = "closed-mailbox-with-raised-flag", layout = "wide")

# Import Bespoke Modules (from emailapp/bespokefunctions/)
from bespokefunctions import pagestyle as ps, sendmail as sm, db, checkfields as cf

# From bespokefunctions/hidestreamlitstyle.py
ps.stylePage()

# Initialise session state variables
if 'submit_count_session' not in st.session_state:
    st.session_state["submit_count_session"] = 0

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
                # Adds 1 to count of emails sent in session. Without a session state this would reset to 0 with every submission
                st.session_state["submit_count_session"] += 1
                st.success("✅ Successfully Sent!") 
            except:
                st.error("🛑 Something Went Wrong.")


with st.container():
    st.write("---")
    st.markdown("### About this app")
    left_column, middle_column, right_column = st.columns([0.4, 0.2, 0.4])
    with left_column:
        st.markdown("##### Current Session")
        st.code(f"Emails Sent: {st.session_state["submit_count_session"]}")
    with right_column:
        st.markdown("##### Total usage statistics (Global)")
        # Fetches values from db queries in bespokefunctions/db.py
        send_count, last_message_sent = db.readFromDb()
        # Shows query results in most readable format (converts from one-value dataframe)
        st.code(f"Emails Sent: {int(send_count.values[0])}")
        st.code(f"Last Message Sent: {str(last_message_sent.values[0])[2:-2]}")