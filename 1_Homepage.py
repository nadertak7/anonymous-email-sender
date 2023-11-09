# Import Modules
import streamlit as st
import re 

# Import Bespoke Modules (from emailapp/bespokefunctions/)
from bespokefunctions import pagestyle as ps
from bespokefunctions import sendmail as sm

# Set config
st.set_page_config(page_title = "Email Sender", page_icon = "closed-mailbox-with-raised-flag", layout = "wide")

# App-specific functions
def checkFields():
    if not (email and subject and message):
        return False
    else: 
        return True

# From bespokefunctions/hidestreamlitstyle.py
ps.stylePage()

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
            subject = st.text_input("Your Subject:", placeholder = "Subject", max_chars = 100)
            message = st.text_area("Your Message:", placeholder = "Message", max_chars = 3000)
            with st.container():
                left_column, middle_column, right_column = st.columns([0.4, 0.2, 0.4])
                submitted = st.form_submit_button("Send", on_click = checkFields)

with st.container():
    left_column, middle_column, right_column = st.columns([0.2, 0.4, 0.4])
    with middle_column:
        # Protects email sends if not all fields are filled
        if submitted and checkFields() == False:
            st.error("⚠ One or more fields are not filled out. Please try again.")
        # Protects email sends (via regex) if email address is invalid
        elif submitted and not re.match("[^@]+@[^@]+\.[^@]+", email):
            st.error("⚠ Invalid email. Please try again.")
        # Below block of code executes when all field rules are met
        elif submitted and checkFields() == True: 
            try:
                # From bespokefunctions/sendmail.py
                sm.sendMail(email, subject, message)
                st.success("✅ Successfully Sent!") 
            except:
                st.error("⚠ Something Went Wrong.")

    
        


