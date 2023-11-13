import streamlit as st 

# Initialise session state variables
def initialiseSessionStates():
    if 'submit_count_session' not in st.session_state:
        st.session_state["submit_count_session"] = 0
    if 'total_subject_char_len_session' not in st.session_state:
        st.session_state["total_subject_char_len_session"] = 0
    if 'avg_subject_char_len_session' not in st.session_state:
        st.session_state["avg_subject_char_len_session"] = 0
    if 'total_message_char_len_session' not in st.session_state:
        st.session_state["total_message_char_len_session"] = 0
    if 'avg_message_char_len_session' not in st.session_state:
        st.session_state["avg_message_char_len_session"] = 0
    if 'last_submitted_timestamp' not in st.session_state:
        st.session_state["last_submitted_timestamp"] = None
    if 'attachment_list_session' not in st.session_state:
        st.session_state["attachment_list_session"] = []
    if 'attachment_count_session' not in st.session_state:
        st.session_state["attachment_count_session"] = 0
    if 'total_attachment_size_mb_session' not in st.session_state:
        st.session_state["total_attachment_size_mb_session"] = 0
    if 'avg_attachment_size_mb_session' not in st.session_state:
        st.session_state["avg_attachment_size_mb_session"] = 0

def calculateSessionStateVars(subject, message, submitted_timestamp, uploaded_file = None):
    # Without a session state these variables would reset to 0 with every submission
    
    # Adds 1 to count of emails sent in session. 
    st.session_state["submit_count_session"] += 1
    
    # Updates last form submission timestamp
    st.session_state["last_submitted_timestamp"] = submitted_timestamp
    
    # Calculates average subject character length
    st.session_state["total_subject_char_len_session"] += len(subject)
    st.session_state["avg_subject_char_len_session"] = round((st.session_state["total_subject_char_len_session"] / st.session_state["submit_count_session"]), 2)
    
    # Calculates average message character length
    st.session_state["total_message_char_len_session"] += len(message)
    st.session_state["avg_message_char_len_session"] = round((st.session_state["total_message_char_len_session"] / st.session_state["submit_count_session"]), 2)
    
    if len(uploaded_file) != 0:
        # Counts total attachments sent in session
        st.session_state["attachment_list_session"] += [file.name for file in uploaded_file]
        st.session_state["attachment_count_session"] = len(st.session_state["attachment_list_session"])

        # Calculates average attachment size in session
        st.session_state["total_attachment_size_mb_session"] += sum([file.size for file in uploaded_file]) / 1024 ** 2
        st.session_state["avg_attachment_size_mb_session"] = round(st.session_state["total_attachment_size_mb_session"] / st.session_state["attachment_count_session"], 2)

    # Packs session states into tuple to be unpacked in homepage
    return(st.session_state["submit_count_session"], 
           st.session_state["last_submitted_timestamp"],
           st.session_state["avg_subject_char_len_session"],
           st.session_state["avg_message_char_len_session"],
           st.session_state["attachment_count_session"],
           st.session_state["avg_attachment_size_mb_session"]
           )