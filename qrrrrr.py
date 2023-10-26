# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 18:09:37 2023

@author: Shaunak M Bhandare
"""

import streamlit as st
import qrcode
import cv2

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

# Define pages
pages = ["Validation", "Secure Content"]
page = st.sidebar.selectbox("Select a page", pages)

# Validation page
if page == "Validation":
    st.title("User Validation")
    user_data = st.text_input("Enter 10-character data:")
    if st.button("Validate"):
        if validate_user_data(user_data):
            st.success("User validation successful.")
            st.markdown("Move to the 'Secure Content' page to access protected content.")
        else:
            st.error("User validation failed: Data length does not match the required 10 characters.")

# Secure content page
if page == "Secure Content":
    st.title("Secure Page")
    st.markdown("This is a protected page that can only be accessed by validated users.")
    st.markdown("Welcome to the Secure Page")

# QR code detection
if page == "Validation":
    uploaded_image = st.file_uploader("Upload an image containing a QR code", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        image = cv2.imread(uploaded_image)
        detector = cv2.QRCodeDetector()
        decoded_info, _points, _straight_qrcode = detector.detectAndDecode(image)
        if decoded_info:
            st.success(f"Decoded QR Code Data: {decoded_info}")
            if validate_user_data(decoded_info):
                st.success("User login successful.")
            else:
                st.error("User login failed: Data length does not match the required 10 characters.")
        else:
            st.error("No QR code detected in the uploaded image.")
