import streamlit as st

# Create an initial session state to store data
if 'data' not in st.session_state:
    st.session_state.data = None

if st.button('Retrieve Data'):
    st.write('Retrieved Data:', st.session_state.data)
