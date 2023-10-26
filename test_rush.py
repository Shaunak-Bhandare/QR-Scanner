# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 19:21:19 2023

@author: Shaunak M Bhandare
"""

import streamlit as st
from streamlit_login_auth_ui.widgets import __login__

import qrcode
import cv2
import numpy as np
from streamlit_extras.switch_page_button import switch_page


# Function to generate a QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Function to validate user data
def validate_user_data(data):
    if len(data) == 10:
        return True
    else:
        return False
    
def detect_and_decode_qr_codes(image):
    qr_code_detector = cv2.QRCodeDetector()
    decoded_text = ""
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect and decode QR codes
    retval, decoded_info, points, straight_qrcode = qr_code_detector.detectAndDecodeMulti(gray_image)
    
    if retval:
        for qr_code_text in decoded_info:
            decoded_text += qr_code_text + "\n"
    
    return decoded_text


__login__obj = __login__(auth_token = "courier_auth_token",
                    company_name = "Shims",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = False,
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN= __login__obj.build_login_ui()
st.session_state.aanjs =LOGGED_IN
# username= __login__obj.get_username()

if LOGGED_IN == True:
    
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox("", ["Validation", "Secure Content"])
    
    
    st.title("QR Code Detector")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)
        
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        st.session_state.data = None
        if st.button("Detect QR Codes"):
            decoded_text = detect_and_decode_qr_codes(image)
            st.session_state.data = decoded_text
            
            if decoded_text:
                st.subheader("Decoded QR Codes:")
                st.text(decoded_text)
                switch_page("about")
            else:
                st.info("No QR codes found in the image.")
