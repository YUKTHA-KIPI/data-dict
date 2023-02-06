import streamlit as st
st.set_page_config(page_title="Flexcare", layout="wide")

# Note: Don't remove the custom code---------------------------------------------------------
#set layout width to wide

from sign_in import sign_in_page
from Table_display import data_display

def landing_page_ui():
    #hide streamlit ui
    st.markdown("""
                <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    .block-container {
                        padding-top: 0rem;
                        padding-bottom: 0rem;
                    }
                </style>
                """, unsafe_allow_html=True)

    st.markdown("""
                <style>
                    
                    .block-container {
                        padding-top: 0rem;
                        padding-bottom: 0rem;
                    }
                </style>
                """, unsafe_allow_html=True)

    # if 'sign_in_state' not in st.session_state or st.session_state['sign_in_state']:    
    #     sign_in_page()
    # else:
    #     learn_more_page()
    sign_in_page()

if "active_session" not in st.session_state or not st.session_state['active_session']:
    landing_page_ui()    
else:
    data_display()
    #st.header("Landing Page after Successful Sign In")