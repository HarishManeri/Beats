import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import hashlib

# ... (keep all the helper functions the same until show_login_page)

def show_login_page():
    st.title("Heart Disease Prediction System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()  # Updated from experimental_rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_username = st.text_input("New Username", key="register_username")
        new_password = st.text_input("New Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif register_user(new_username, new_password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Username already exists")

def main():
    st.set_page_config(page_title="Heart Disease Prediction", layout="wide")
    
    # Initialize database
    init_db()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_login_page()
        return
    
    # Main navigation
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    page = st.sidebar.selectbox("Navigation", ["New Analysis", "History", "Profile"])
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()  # Updated from experimental_rerun()
    
    # ... (rest of the main function remains the same)

if __name__ == "__main__":
    main()
