import streamlit as st 

# Initialise session state variables
def initialiseSessionStates():
    default_session_state = {
        "submit_count_session": 0,
        "total_subject_char_len_session": 0,
        "avg_subject_char_len_session": 0,
        "total_message_char_len_session": 0,
        "avg_message_char_len_session": 0,
        "last_submitted_timestamp": None,
        "attachment_list_session": [],
        "attachment_count_session": 0,
        "total_attachment_size_mb_session": 0,
        "avg_attachment_size_mb_session": 0,
        "emails_censored_count_session": 0,
        "emails_censored_perc_session": 0,
    }

    for key, default_value in default_session_state.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
def calculateSessionStateVars(subject, 
                              message, 
                              submitted_timestamp, 
                              filter_profanity, 
                              subject_contains_profanity, 
                              message_contains_profanity, 
                              uploaded_file = None):
    # Without a session state these variables would reset to 0 with every submission
    
    # Adds 1 to count of emails sent in session. 
    st.session_state["submit_count_session"] += 1
    
    # Updates last form submission timestamp
    st.session_state["last_submitted_timestamp"] = submitted_timestamp
    
    # Calculates average subject character length
    st.session_state["total_subject_char_len_session"] += len(subject.strip())
    st.session_state["avg_subject_char_len_session"] = round((st.session_state["total_subject_char_len_session"] / st.session_state["submit_count_session"]), 2)
    
    # Calculates average message character length
    st.session_state["total_message_char_len_session"] += len(message.strip())
    st.session_state["avg_message_char_len_session"] = round((st.session_state["total_message_char_len_session"] / st.session_state["submit_count_session"]), 2)
    
    if len(uploaded_file) != 0:
        # Counts total attachments sent in session
        st.session_state["attachment_list_session"] += [file.name for file in uploaded_file]
        st.session_state["attachment_count_session"] = len(st.session_state["attachment_list_session"])

        # Calculates average attachment size in session
        st.session_state["total_attachment_size_mb_session"] += sum([file.size for file in uploaded_file]) / 1024 ** 2
        st.session_state["avg_attachment_size_mb_session"] = round(st.session_state["total_attachment_size_mb_session"] / st.session_state["attachment_count_session"], 2)

    # Calculates number of emails censored 
    if filter_profanity and (subject_contains_profanity or message_contains_profanity):
        st.session_state["emails_censored_count_session"] += 1
    
    st.session_state["emails_censored_perc_session"] = round(st.session_state["emails_censored_count_session"] / st.session_state["submit_count_session"] * 100, 2)

    # Packs session states into tuple to be unpacked in homepage
    return(st.session_state["submit_count_session"], 
           st.session_state["last_submitted_timestamp"],
           st.session_state["avg_subject_char_len_session"],
           st.session_state["avg_message_char_len_session"],
           st.session_state["attachment_count_session"],
           st.session_state["avg_attachment_size_mb_session"],
           st.session_state["emails_censored_count_session"],
           st.session_state["emails_censored_perc_session"])