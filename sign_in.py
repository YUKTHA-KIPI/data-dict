import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import snowflake.connector
from snowflake.connector.errors import DatabaseError
from PIL import Image
# Note: Don't remove the custom code---------------------------------------------------------
#set layout width to wide
# st.set_page_config(page_title="Learn more", layout="wide")

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


#custom code
def run_custom_code():

    st.markdown("""
    <style id="customstyle">
    .stApp{    
        background-size: 100% 100%;
        background-repeat: no-repeat;
        background-image: url("flex_bg.png"); 
    }
    /* input code */
    input:focus {
        border: 1px solid #B3D943;
    }
    input#usernameinput::placeholder {
        color: #757575;
    }
    input#passwordinput::placeholder {
        color: #757575;
    }
    input#account_identifierinput::placeholder {
        color: #757575;
    }
    input#usernameinput{
        height: 45px;
        background-color: #EEEEEE;
        color: #000000;
        placeholder: "snowflake user name";
        border-radius: 5px;
        caret-color: #000000;
    }
    input#account_identifierinput{
        height: 45px;
        background-color: #EEEEEE;
        color: #000000;
        placeholder: "acme-marketing_test_account";
        border-radius: 5px;
        caret-color: #000000;
    }
    input#passwordinput{
        height: 45px;
        background-color: #EEEEEE;
        color: #000000;
        placeholder: "**********";
        border-radius: 5px;
        caret-color: #000000;
    }
    /* buttons code */
    button#learnmorebutton{
        background-color: #B3D943;
        height: 45px;
        color:#000000;
        border: none;
        border-radius: 5px;
        width: 120px;
    }
    button#learnmorebutton:hover {
        background-color: #000000;
        color:#FFFFFF;
        border: 1px solid #FFFFFF;
        border-radius: 5px;
    }
    button#signinbutton{
        background-color: #B3D943;
        height: 45px;
        width: 100%;
        color:#000000;
        border-radius: 5px;
        visibility: visible;
    }
    button#signinbutton:hover {
        background-color: #000000;
        color:#FFFFFF;
        border: 1px solid #FFFFFF;
        border-radius: 5px;    
    }
    /*card*/
    div#authcardholder{
        background-color: #000000; 
        margin-left: auto;
        margin-right: auto;
        padding: 10px 30px 0 30px;
        border-radius: 15px;
        flex: 20%;
    }
    /*card helper*/
    p#cardhelper_authentication{
        height: 0;
        width: 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    components.html("""

    <script id="jquery" src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script id="customscript">
    const page = window.parent.document;
    $( document ).ready(function() {    
        
        $( page ).find('button').each(function( index ) {
            switch($(this).text()) {
                case 'Learn more':
                    //console.log('Learn more button');
                    $(this).attr("id", "learnmorebutton");
                    break;
                case 'Sign in':
                    //console.log('sign in button');
                    $(this).attr({"id": "signinbutton", "visibility": "hidden"});
                    break;
                default:
                    //$(this).attr("id", "button");
                    // console.log('Not defined');
                    break;
            }
        });
        
        function run_card_holder(ref){
            const columndiv = ref.closest("div[data-testid='column']");
            columndiv.attr({"id": "authcardholder"});
        }
        run_card_holder($( page ).find('p#cardhelper_authentication'));

        $( page ).find('input').each(function( index ) {

            switch($(this).attr('aria-label')) {
                case 'username':
                    $(this).attr({"id": "usernameinput", "placeholder": "someone@kipi.bi"});
                    //console.log('username');
                    break;
                //case 'account_identifier':
                //    $(this).attr({"id": "account_identifierinput", "placeholder": "acme-marketing_test_account"});
                    //console.log('password');
                 //   break;
                case 'password':
                    $(this).attr({"id": "passwordinput", "placeholder": "***************", "type": "password"});
                    //console.log('password');
                    break;
                default:
                    //$(this).attr("id", "input");
                    //console.log($(this).attr('aria-label'));
                    break;
            }

        });

    });
    </script>
    """,
        height=0,
        width=0,
    )
    
    return 1
# Note: Don't remove the custom code---------------------------------------------------------

#authentication
def signin_callback():
    # Connection with Snowflake,
    # If any credential is wrong then it goes in except block
    try:
        with st.spinner('Logging in'):

            # Logic for getting snowflake connector in active session

            con = snowflake.connector.connect(
            user=st.session_state['username'],
            password=st.session_state['password'],
            account="flexcare",
            role="sysadmin",
            # account = "atjpgbj-qp69829",
            warehouse = 'COMPUTE_WH',
            # database="ACCELERATOR_DB",
            # schema="RBAC"
            )        
            st.session_state['active_session'] = con

            #connection_parameters = {
            #    "account": "flexcare",
             #   "user": st.session_state['username'],
              #  "password": st.session_state['password'],
              #  "database":"ACCELERATOR_DB",
               # "schema": "RBAC"
               # }

        #st.session_state['active_session'] = Session.builder.configs(connection_parameters).create()  
        
    except DatabaseError:
        st.session_state['login_clicked'] = True
        st.session_state['active_session'] = None

if 'login_clicked' not in st.session_state:
    st.session_state['login_clicked'] = None

def get_sign_in_form():

    # Note: Don't remove the card helper---------------------------------------------------------
    s1 = st.markdown('''
    
    <p id="cardhelper_authentication" style="font-size:16px; visibility: hidden;">CardHelper</p>

    ''', unsafe_allow_html=True)
    # Note: Don't remove the card helper---------------------------------------------------------

    s2 = st.markdown('''
    
    <p style="font-size:16px;">Username</p>

    ''', unsafe_allow_html=True)
    s3 = st.text_input('username', label_visibility = 'collapsed')
    
    #s4 = st.markdown('''
    
    #<p style="font-size:16px;">Account identifier</p>

    #''', unsafe_allow_html=True)
    #s5 = st.text_input('account_identifier', label_visibility = 'collapsed')
#'account_name' in st.session_state and
    if 'username' in st.session_state and 'password' in st.session_state and ('login_clicked' not in st.session_state or st.session_state['login_clicked']):  
        s8_text = "Credential not valid, Please check username or password "
    else:
        s8_text = ""
        
    s6 = st.markdown(f'''
    <p style="font-size:16px;width:30%;display: inline-block;">Password</p><p style="width:35%;display: inline-block;"></p>
    ''', unsafe_allow_html=True)

    s7 = st.text_input('password',  label_visibility = 'collapsed')

    if s8_text:
        s8 = st.error(f'{s8_text}')
    else:
        s8 = ''
    s9 = st.button('Sign in', on_click=signin_callback)

    st.session_state['username'] = s3
    #st.session_state['account_name'] = s5
    st.session_state['password'] = s7

    s10 = ''

    return s1, s2, s3, s6, s7, s8, s9, s10


def sign_in_page():
    # Note: Don't change the structure of the template---------------------------------------------------------
    #top navigation
    with st.container():
        logo, empty1, empty2, empty3 = st.columns([4, 1, 1, 4], gap="large")

        with logo:
            logoimage = Image.open(r'flex.png')
            st.image(logoimage)


    #empty container
    with st.container():
        st.write('')

#body content
    with st.container():
        div1, div2 = st.columns(2, gap="medium")

        with div1:
            with st.container():
                st.write('')
                st.write('')
                st.markdown('''
                
                <h1 style="font-size:55px;">Data Dictionary<br></h1>
            
                ''', unsafe_allow_html=True)

                st.markdown('''
                
                <h1 style="font-size:25px;">Enables users to find the <br>tables and entities in Snowflake</h1>

                ''', unsafe_allow_html=True)

               # st.markdown('''
                
                #<p>The no code platform takes the user through the data migration journey in a phased<br>process, while providing options to configure the migration at easy step from the GUI</p>

                #''', unsafe_allow_html=True)

                
        with div2:
            with st.container():            
                get_sign_in_form()
                # Note: Don't remove the run custom code call---------------------------------------------------------
                run_custom_code()
                # Note: Don't remove the run custom code call---------------------------------------------------------   

    # Note: Don't change the structure of the template---------------------------------------------------------
