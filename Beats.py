import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

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
    
    # Normalize risks
    for key in risks:
        risks[key] = min(risks[key], 100)
    
    return risks

def analyze_labs(data):
    analysis = []
    
    if float(data['total_cholesterol']) > 240:
        analysis.append({
            'test': 'Total Cholesterol',
            'value': data['total_cholesterol'],
            'status': 'High',
            'recommendation': 'Consider lifestyle changes and consult doctor'
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
        data['blood_sugar'] = st.number_input("Blood Sugar", 0.0, 500.0)
    
    st.subheader("Medical History")
    col1, col2 = st.columns(2)
    with col1:
        data['smoking'] = st.selectbox("Smoking", ["No", "Yes"])
        data['diabetes'] = st.selectbox("Diabetes", ["No", "Yes"])
        data['previous_stroke'] = st.selectbox("Previous Stroke", ["No", "Yes"])
        data['family_history'] = st.selectbox("Family History of Heart Disease", ["No", "Yes"])
    
    return data

def main():
    st.title("Heart Disease Risk Assessment")
    
    # Collect patient data
    data = collect_patient_data()
    
    if st.button("Calculate Risk"):
        # Calculate risks
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
        if analysis:
            for item in analysis:
                with st.expander(f"{item['test']} - {item['status']}"):
                    st.write(f"Value: {item['value']}")
                    st.write(f"Recommendation: {item['recommendation']}")
        else:
            st.write("All laboratory values are within normal range.")
        
        # BMI Calculation
        bmi = round(data['weight'] / ((data['height']/100) ** 2), 1)
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

if __name__ == "__main__":
    main()
