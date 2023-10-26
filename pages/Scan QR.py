import streamlit as st
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

# Sidebar navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Select a page", ["Validation", "Secure Content"])

# Validation page
if selected_page == "Validation":
    st.title("User Validation")
    user_data = st.text_input("Enter 10-character data:")
    if st.button("Validate"):
        if validate_user_data(user_data):
            st.success("User validation successful.")
            st.markdown("Redirect to the 'Secure Content' page to access protected content.")
        else:
            st.error("User validation failed: Data length does not match the required 10 characters.")
    # Streamlit UI
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
        #st.experimental_set_query_params(page="secure_content")

# Secure content page
if selected_page == "Secure Content":
    st.title("Secure Page")
    st.markdown("This is a protected page that can only be accessed by validated users.")
    st.markdown("Welcome to the Secure Page")

