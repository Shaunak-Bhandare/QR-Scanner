import streamlit as st
from streamlit_login_auth_ui.widgets import __login__
from streamlit_extras.switch_page_button import switch_page

    
# Create an initial session state to store data
if 'data' not in st.session_state:
    st.session_state.data = None
    
if st.session_state.aanjs == True:
    if st.button('Retrieve Data'):
        st.write('Retrieved Data:', st.session_state.data)
        
if st.session_state.aanjs == False:

    __login__obj = __login__(auth_token = "courier_auth_token",
                        company_name = "Shims",
                        width = 200, height = 250,
                        logout_button_name = 'Logout', hide_menu_bool = True,
                        hide_footer_bool = True,
                        lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

    LOGGED_IN= __login__obj.build_login_ui()
    st.session_state.aanjs =LOGGED_IN
