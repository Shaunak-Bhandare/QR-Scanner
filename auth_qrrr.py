import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit.components.v1 as components
from hasher import Hasher
from authenticate import QRCodeAuthenticator  # Import the QRCodeAuthenticator class

_RELEASE = True

if not _RELEASE:
    # Loading config file
    with open('../config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
        print(config)

    # Create a QRCodeAuthenticator object with your existing authentication configuration
    authenticator = QRCodeAuthenticator(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Streamlit app
    st.title("QR Code-Based Login System")

    # Show the default QR code image
    st.image("path_to_default_qr_code.png", caption="Default QR Code", use_column_width=True)

    # Use the QRCodeAuthenticator instance for login
    name, authentication_status, username = authenticator.login_with_qr_code("Login")

    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
        st.title('Some content')
    elif authentication_status is False:
        st.error('Username/QR code is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and QR code')

    # Creating a password reset widget
    if authentication_status:
        try:
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

    # Creating a new user registration widget
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

    # Creating a forgot password widget
    try:
        username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
        if username_forgot_pw:
            st.success('New password sent securely')
            # Random password to be transferred to the user securely
        else:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

    # Creating a forgot username widget
    try:
        username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
        if username_forgot_username:
            st.success('Username sent securely')
            # Username to be transferred to the user securely
        else:
            st.error('Email not found')
    except Exception as e:
        st.error(e)

    # Creating an update user details widget
    if authentication_status:
        try:
            if authenticator.update_user_details(username, 'Update user details'):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)

    # Saving config file
    with open('../config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
