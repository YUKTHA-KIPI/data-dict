import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from PIL import Image
# # Note: Don't remove the custom code---------------------------------------------------------
# #set layout width to wide
# st.set_page_config(page_title="Learn more", layout="wide")

# #hide streamlit ui
# st.markdown("""
#             <style>
#                 #MainMenu {visibility: hidden;}
#                 footer {visibility: hidden;}
#                 header {visibility: hidden;}
#                 .block-container {
#                     padding-top: 0rem;
#                     padding-bottom: 0rem;
#                 }
#             </style>
#             """, unsafe_allow_html=True)

#custom code
def run_custom_code():

    st.markdown("""
    <style id="customstyle">
    .stApp{    
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-image: url("assets\brand\flex_bg.png"); 
    }
    </style>
    """, unsafe_allow_html=True)
    
    components.html("""

    
    """,
        height=0,
        width=0,
    )
    
    return 1
# Note: Don't remove the custom code---------------------------------------------------------

# Note: Don't change the structure of the template---------------------------------------------------------
#menu
selected = ""
def streamlit_menu():
    selected = option_menu(
        menu_title=None,
        options=["Sign in"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "25px", "background-color": "transparent"},
            "icon": {"color": "#990033", "font-size": "16px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "right",
                "margin": "0px",
                "font-weight": "100",
                "background-color": "transparent"
            },
            "nav-link-selected": { "color":"#990033", "font-weight": "100", "background-color": "transparent"},
        },
    )
    return selected


#body content
def get_home_content():
    
    #top navigation
    with st.container():
        logo, empty1, empty2, menu = st.columns([4, 1, 1, 2], gap="large")

        with logo:
            ''
            logoimage = Image.open(r'assets\brand\flex.png')
            st.image(logoimage)

        with menu:
            selected = streamlit_menu()
            if selected == 'Sign in':
                st.session_state['sign_in_state'] = True

    #empty container
    with st.container():
        st.markdown('''
        
            <p id="non_card_element" style="font-size:16px; visibility: hidden; background-color: transparent;">Home Card Helper</p>

            ''', unsafe_allow_html=True)

    #empty container
    with st.container():
        st.markdown('''
        
            <p id="non_card_element" style="font-size:16px; visibility: hidden; background-color: transparent;">Home Card Helper</p>

            ''', unsafe_allow_html=True)
    
    # Note: Don't remove the card helper---------------------------------------------------------
    st.markdown('''
    
        <p id="maincardhelper_authentication" style="font-size:16px; visibility: hidden;">Home Card Helper</p>

        ''', unsafe_allow_html=True)
    # Note: Don't remove the card helper---------------------------------------------------------
    h2 = st.markdown('''
        
        <h1 style="font-size: 30px; margin-top: 20px; padding: 5px 5px 0 5px;">Data Dictionary</h1>
        <h3 style="font-size: 20px; margin: 0; padding: 0 5px 5px 5px;"><br/>Enables users to find tables and its attributes in Snowflake</h3>

        <p style="font-size: 18px; margin: 0 30px 0 0; padding: 25px 25px 0 5px; text-align: justify;">The simple data dictionary which will help 
        flexcare customers to find the tables and its attributes in snowflake easily without much hassle.
        </p>

        ''', unsafe_allow_html=True)


    return 

def learn_more_page():
    
    with st.container():
        get_home_content()
        if selected == "Sign in":
            pass
        # Note: Don't remove the run custom code call---------------------------------------------------------   
        run_custom_code()
        # Note: Don't remove the run custom code call---------------------------------------------------------   
    # Note: Don't change the structure of the template---------------------------------------------------------
