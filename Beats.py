import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import hashlib

# Database setup
def init_db():
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS assessments
                 (username TEXT, date TEXT, data TEXT, risk_scores TEXT)''')
    conn.commit()
    conn.close()

# Password hashing
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# User authentication
def authenticate(username, password):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

# User registration
def register_user(username, password):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Calculate BMI
def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

# Risk calculation
def calculate_risk_scores(data):
    risks = {
        "heart_attack": 0,
        "stroke": 0,
        "cardiac_arrest": 0,
        "heart_failure": 0
    }
    
    # Heart Attack Risk
    if data['systolic_bp'] > 140: risks['heart_attack'] += 20
    if data['smoking'] == 'Yes': risks['heart_attack'] += 25
    if float(data['total_cholesterol']) > 200: risks['heart_attack'] += 15
    if data['diabetes'] == 'Yes': risks['heart_attack'] += 20
    if data['family_history'] == 'Yes': risks['heart_attack'] += 20
    
    # Stroke Risk
    if data['systolic_bp'] > 140: risks['stroke'] += 25
    if data['smoking'] == 'Yes': risks['stroke'] += 20
    if data['previous_stroke'] == 'Yes': risks['stroke'] += 30
    if data['age'] > 65: risks['stroke'] += 25
    
    # Cardiac Arrest Risk
    if data['previous_heart_attack'] == 'Yes': risks['cardiac_arrest'] += 30
    if data['chest_pain'] == 'Yes': risks['cardiac_arrest'] += 25
    
    # Heart Failure Risk
    if data['age'] > 65: risks['heart_failure'] += 20
    if data['hypertension'] == 'Yes': risks['heart_failure'] += 25
    if data['diabetes'] == 'Yes': risks['heart_failure'] += 20
    
    # Normalize risks
    for key in risks:
        risks[key] = min(risks[key], 100)
    
    return risks

# Lab analysis
def analyze_labs(data):
    analysis = []
    
    # Cholesterol Analysis
    if float(data['total_cholesterol']) > 240:
        analysis.append({
            'test': 'Total Cholesterol',
            'value': data['total_cholesterol'],
            'status': 'High',
            'recommendation': 'Consider lifestyle changes and consult doctor'
        })
    
    if float(data['ldl']) > 160:
        analysis.append({
            'test': 'LDL Cholesterol',
            'value': data['ldl'],
            'status': 'High',
            'recommendation': 'Reduce saturated fat intake and increase exercise'
        })
    
    if float(data['hdl']) < 40:
        analysis.append({
            'test': 'HDL Cholesterol',
            'value': data['hdl'],
            'status': 'Low',
            'recommendation': 'Increase physical activity and consider dietary changes'
        })
    
    if float(data['blood_sugar']) > 126:
        analysis.append({
            'test': 'Blood Sugar',
            'value': data['blood_sugar'],
            'status': 'High',
            'recommendation': 'Monitor blood sugar regularly and consult endocrinologist'
        })
    
    return analysis

def display_risk_meter(risk_score, title):
    st.subheader(title)
    st.progress(risk_score / 100)
    st.write(f"Risk Score: {risk_score}%")
    
    if risk_score < 30:
        st.success("Low Risk")
    elif risk_score < 70:
        st.warning("Moderate Risk")
    else:
        st.error("High Risk")

def collect_patient_data():
    data = {}
    
    st.subheader("Demographics")
    col1, col2 = st.columns(2)
    with col1:
        data['age'] = st.number_input("Age", 18, 120)
        data['gender'] = st.selectbox("Gender", ["Male", "Female"])
        data['weight'] = st.number_input("Weight (kg)", 30.0, 200.0)
        data['height'] = st.number_input("Height (cm)", 100.0, 250.0)
    
    st.subheader("Vital Signs")
    col1, col2 = st.columns(2)
    with col1:
        data['systolic_bp'] = st.number_input("Systolic BP", 70, 250)
        data['diastolic_bp'] = st.number_input("Diastolic BP", 40, 150)
        data['heart_rate'] = st.number_input("Heart Rate (bpm)", 40, 200)
    
    st.subheader("Laboratory Results")
    col1, col2 = st.columns(2)
    with col1:
        data['total_cholesterol'] = st.number_input("Total Cholesterol", 0.0, 500.0)
        data['hdl'] = st.number_input("HDL", 0.0, 100.0)
        data['ldl'] = st.number_input("LDL", 0.0, 300.0)
        data['blood_sugar'] = st.number_input("Blood Sugar", 0.0, 500.0)
    
    st.subheader("Medical History")
    col1, col2 = st.columns(2)
    with col1:
        data['smoking'] = st.selectbox("Smoking", ["No", "Yes"])
        data['diabetes'] = st.selectbox("Diabetes", ["No", "Yes"])
        data['hypertension'] = st.selectbox("Hypertension", ["No", "Yes"])
        data['previous_heart_attack'] = st.selectbox("Previous Heart Attack", ["No", "Yes"])
        data['previous_stroke'] = st.selectbox("Previous Stroke", ["No", "Yes"])
        data['family_history'] = st.selectbox("Family History of Heart Disease", ["No", "Yes"])
    
    st.subheader("Current Symptoms")
    col1, col2 = st.columns(2)
    with col1:
        data['chest_pain'] = st.selectbox("Chest Pain", ["No", "Yes"])
        data['shortness_breath'] = st.selectbox("Shortness of Breath", ["No", "Yes"])
        data['fatigue'] = st.selectbox("Fatigue", ["No", "Yes"])
    
    return data

def save_assessment(username, data, risk_scores):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("INSERT INTO assessments VALUES (?, ?, ?, ?)",
              (username, datetime.now().isoformat(),
               str(data), str(risk_scores)))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect('health_app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM assessments WHERE username=? ORDER BY date DESC", (username,))
    history = c.fetchall()
    conn.close()
    return history

def show_login_page():
    st.title("Heart Disease Prediction System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
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
        st.experimental_rerun()
    
    if page == "New Analysis":
        st.title("Heart Disease Risk Assessment")
        data = collect_patient_data()
        
        if st.button("Calculate Risk"):
            risk_scores = calculate_risk_scores(data)
            analysis = analyze_labs(data)
            
            # Display results
            st.title("Analysis Results")
            
            # Display risk meters
            col1, col2 = st.columns(2)
            with col1:
                display_risk_meter(risk_scores['heart_attack'], "Heart Attack Risk")
                display_risk_meter(risk_scores['stroke'], "Stroke Risk")
            with col2:
                display_risk_meter(risk_scores['cardiac_arrest'], "Cardiac Arrest Risk")
                display_risk_meter(risk_scores['heart_failure'], "Heart Failure Risk")
            
            # Display lab analysis
            st.subheader("Laboratory Analysis")
            for item in analysis:
                with st.expander(f"{item['test']} - {item['status']}"):
                    st.write(f"Value: {item['value']}")
                    st.write(f"Recommendation: {item['recommendation']}")
            
            # Save assessment
            save_assessment(st.session_state.username, data, risk_scores)
            
            # BMI Calculation
            bmi = calculate_bmi(data['weight'], data['height'])
            st.subheader("BMI Analysis")
            st.write(f"Your BMI: {bmi}")
            if bmi < 18.5:
                st.warning("Underweight")
            elif bmi < 25:
                st.success("Normal weight")
            elif bmi < 30:
                st.warning("Overweight")
            else:
                st.error("Obese")
    
    elif page == "History":
        st.title("Assessment History")
        history = get_user_history(st.session_state.username)
        
        if not history:
            st.write("No previous assessments found")
        else:
            for entry in history:
                with st.expander(f"Assessment - {entry[1]}"):
                    st.write("Risk Scores:")
                    risk_scores = eval(entry[3])
                    for risk, score in risk_scores.items():
                        st.write(f"{risk}: {score}%")
    
    elif page == "Profile":
        st.title("User Profile")
        st.write(f"Username: {st.session_state.username}")
        # Add more profile features as needed

if __name__ == "__main__":
    main()
