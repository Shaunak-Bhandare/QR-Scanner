import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

st.set_page_config(initial_sidebar_state="collapsed")

with open('./data.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

tab1, tab2 = st.tabs(["📈 Register", "🗃 Login"])

tab1.subheader("Create a new account")

tab2.subheader("Login to your account")

with tab1:
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

with tab2:
    authenticator.login('Login', 'main')
    
    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
        
    elif st.session_state["authentication_status"] is False:
        st.markdown(
            """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
            unsafe_allow_html=True,
        )
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    
with open('./data.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)