import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Function to detect and decode QR codes
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

# Create a custom session state
def create_session_state():
    return {
        "locked": False,
    }

session_state = create_session_state()

# Define the correct QR code content (you can replace this with your own QR code)
default_qr_code = "testqr.png"


st.title("QR Code-Based Login System")

if session_state["locked"]:
    st.info("You are logged in.")
else:
    st.info("You are not logged in.")

if not session_state["locked"]:
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)
        
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Scan QR Code"):
            decoded_text = detect_and_decode_qr_codes(image)
            print(decoded_text)
            
            if decoded_text == default_qr_code:
                session_state["locked"] = True
                st.success("QR code matched. You are now logged in!")
            else:
                st.error("QR code did not match. You cannot log in.")
elif st.button("Logout"):
    session_state["locked"] = False
    st.success("You have successfully logged out.")

# Content to display after login
if session_state["locked"]:
    st.subheader("Welcome! You are logged in.")
    st.write("You can now access the secure content here.")
