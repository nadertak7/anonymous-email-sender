import streamlit as st

# Hide footer and hamburger menu
def stylePage():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 