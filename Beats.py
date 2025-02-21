import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def calculate_risk_scores(data):
    risks = {
        "Heart Attack": 0,
        "Stroke": 0,
        "Cardiac Arrest": 0,
        "Heart Failure": 0
    }
    
    # Heart Attack Risk Factors
    if data['systolic_bp'] > 140: risks['Heart Attack'] += 15
    if data['diastolic_bp'] > 90: risks['Heart Attack'] += 10
    if data['smoking'] == 'Yes': risks['Heart Attack'] += 20
    if float(data['cholesterol']) > 200: risks['Heart Attack'] += 15
    if data['diabetes'] == 'Yes': risks['Heart Attack'] += 15
    if data['family_history'] == 'Yes': risks['Heart Attack'] += 10
    if data['obesity'] == 'Yes': risks['Heart Attack'] += 10
    if data['physical_activity'] == 'Low': risks['Heart Attack'] += 5
    
    # Stroke Risk Factors
    if data['systolic_bp'] > 140: risks['Stroke'] += 20
    if data['smoking'] == 'Yes': risks['Stroke'] += 15
    if data['diabetes'] == 'Yes': risks['Stroke'] += 15
    if data['age'] > 65: risks['Stroke'] += 20
    if data['afib'] == 'Yes': risks['Stroke'] += 20
    if data['previous_stroke'] == 'Yes': risks['Stroke'] += 10
    
    # Cardiac Arrest Risk
    if data['previous_heart_attack'] == 'Yes': risks['Cardiac Arrest'] += 25
    if data['heart_failure'] == 'Yes': risks['Cardiac Arrest'] += 20
    if data['arrhythmia'] == 'Yes': risks['Cardiac Arrest'] += 20
    if data['chest_pain'] == 'Yes': risks['Cardiac Arrest'] += 15
    if data['shortness_of_breath'] == 'Yes': risks['Cardiac Arrest'] += 20
    
    # Heart Failure Risk
    if data['age'] > 65: risks['Heart Failure'] += 15
    if data['hypertension'] == 'Yes': risks['Heart Failure'] += 20
    if data['diabetes'] == 'Yes': risks['Heart Failure'] += 15
    if data['obesity'] == 'Yes': risks['Heart Failure'] += 15
    if data['coronary_artery_disease'] == 'Yes': risks['Heart Failure'] += 20
    if data['sleep_apnea'] == 'Yes': risks['Heart Failure'] += 15
    
    # Normalize all risks to 100%
    for key in risks:
        risks[key] = min(risks[key], 100)
    
    return risks

def analyze_vitals_and_labs(data):
    analysis = []
    
    # Blood Pressure Analysis
    if data['systolic_bp'] >= 180 or data['diastolic_bp'] >= 120:
        analysis.append({
            'parameter': 'Blood Pressure',
            'value': f"{data['systolic_bp']}/{data['diastolic_bp']}",
            'status': 'Crisis',
            'risk_level': 'High',
            'recommendation': 'Seek immediate medical attention'
        })
    elif data['systolic_bp'] >= 140 or data['diastolic_bp'] >= 90:
        analysis.append({
            'parameter': 'Blood Pressure',
            'value': f"{data['systolic_bp']}/{data['diastolic_bp']}",
            'status': 'High',
            'risk_level': 'Moderate',
            'recommendation': 'Consult healthcare provider and consider lifestyle changes'
        })

    # Cholesterol Analysis
    if float(data['cholesterol']) > 240:
        analysis.append({
            'parameter': 'Cholesterol',
            'value': data['cholesterol'],
            'status': 'High',
            'risk_level': 'High',
            'recommendation': 'Consult doctor and consider diet modifications'
        })
    
    # Blood Sugar Analysis
    if float(data['blood_sugar']) > 126:
        analysis.append({
            'parameter': 'Blood Sugar',
            'value': data['blood_sugar'],
            'status': 'High',
            'risk_level': 'High',
            'recommendation': 'Monitor blood sugar and consult endocrinologist'
        })
    
    # Heart Rate Analysis
    if float(data['heart_rate']) > 100:
        analysis.append({
            'parameter': 'Heart Rate',
            'value': data['heart_rate'],
            'status': 'Elevated',
            'risk_level': 'Moderate',
            'recommendation': 'Monitor and consult healthcare provider if persistent'
        })
    
    return analysis

def get_lifestyle_recommendations(data):
    recommendations = []
    
    if data['smoking'] == 'Yes':
        recommendations.append({
            'category': 'Smoking',
            'recommendation': 'Consider smoking cessation programs',
            'details': 'Smoking significantly increases cardiovascular risk'
        })
    
    if data['physical_activity'] == 'Low':
        recommendations.append({
            'category': 'Physical Activity',
            'recommendation': 'Increase physical activity to 150 minutes per week',
            'details': 'Regular exercise helps reduce cardiovascular risk'
        })
    
    if data['obesity'] == 'Yes':
        recommendations.append({
            'category': 'Weight Management',
            'recommendation': 'Consider weight management program',
            'details': 'Weight loss can significantly improve heart health'
        })
    
    if data['stress'] == 'High':
        recommendations.append({
            'category': 'Stress Management',
            'recommendation': 'Consider stress reduction techniques',
            'details': 'High stress levels can impact heart health'
        })
    
    return recommendations

def main():
    st.set_page_config(page_title="Comprehensive Heart Disease Risk Assessment", layout="wide")
    
    st.title("Heart Disease Risk Assessment System")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Risk Assessment", "Results", "Recommendations"])
    
    with tab1:
        st.header("Patient Information")
        
        # Demographics
        col1, col2 = st.columns(2)
        with col1:
            data = {}
            data['age'] = st.number_input("Age", 18, 120, 50)
            data['gender'] = st.selectbox("Gender", ["Male", "Female"])
            data['weight'] = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
            data['height'] = st.number_input("Height (cm)", 100.0, 250.0, 170.0)
            
        # Vital Signs
        st.subheader("Vital Signs")
        col1, col2 = st.columns(2)
        with col1:
            data['systolic_bp'] = st.number_input("Systolic Blood Pressure", 70, 250, 120)
            data['diastolic_bp'] = st.number_input("Diastolic Blood Pressure", 40, 150, 80)
            data['heart_rate'] = st.number_input("Heart Rate (bpm)", 40, 200, 75)
            
        # Laboratory Results
        st.subheader("Laboratory Results")
        col1, col2 = st.columns(2)
        with col1:
            data['cholesterol'] = st.number_input("Total Cholesterol", 100.0, 500.0, 180.0)
            data['blood_sugar'] = st.number_input("Fasting Blood Sugar", 70.0, 400.0, 100.0)
            
        # Medical History
        st.subheader("Medical History")
        col1, col2, col3 = st.columns(3)
        with col1:
            data['smoking'] = st.selectbox("Smoking", ["No", "Yes"])
            data['diabetes'] = st.selectbox("Diabetes", ["No", "Yes"])
            data['hypertension'] = st.selectbox("Hypertension", ["No", "Yes"])
        with col2:
            data['obesity'] = st.selectbox("Obesity", ["No", "Yes"])
            data['previous_heart_attack'] = st.selectbox("Previous Heart Attack", ["No", "Yes"])
            data['previous_stroke'] = st.selectbox("Previous Stroke", ["No", "Yes"])
        with col3:
            data['family_history'] = st.selectbox("Family History of Heart Disease", ["No", "Yes"])
            data['coronary_artery_disease'] = st.selectbox("Coronary Artery Disease", ["No", "Yes"])
            data['heart_failure'] = st.selectbox("Heart Failure", ["No", "Yes"])
            
        # Symptoms
        st.subheader("Current Symptoms")
        col1, col2, col3 = st.columns(3)
        with col1:
            data['chest_pain'] = st.selectbox("Chest Pain", ["No", "Yes"])
            data['shortness_of_breath'] = st.selectbox("Shortness of Breath", ["No", "Yes"])
        with col2:
            data['fatigue'] = st.selectbox("Fatigue", ["No", "Yes"])
            data['arrhythmia'] = st.selectbox("Arrhythmia", ["No", "Yes"])
        with col3:
            data['sleep_apnea'] = st.selectbox("Sleep Apnea", ["No", "Yes"])
            data['stress'] = st.selectbox("Stress Level", ["Low", "Moderate", "High"])
            
        # Lifestyle
        st.subheader("Lifestyle Factors")
        col1, col2 = st.columns(2)
        with col1:
            data['physical_activity'] = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
            data['alcohol'] = st.selectbox("Alcohol Consumption", ["None", "Moderate", "Heavy"])
            
        if st.button("Calculate Risk"):
            st.session_state.data = data
            st.session_state.show_results = True
            
    with tab2:
        if 'show_results' in st.session_state and st.session_state.show_results:
            st.header("Risk Assessment Results")
            
            # Calculate and display risk scores
            risk_scores = calculate_risk_scores(st.session_state.data)
            
            # Display risk meters
            for condition, risk in risk_scores.items():
                st.subheader(condition)
                st.progress(risk/100)
                if risk < 30:
                    st.success(f"{risk}% - Low Risk")
                elif risk < 60:
                    st.warning(f"{risk}% - Moderate Risk")
                else:
                    st.error(f"{risk}% - High Risk")
                    
            # Display analysis
            st.header("Clinical Analysis")
            analysis = analyze_vitals_and_labs(st.session_state.data)
            
            for item in analysis:
                with st.expander(f"{item['parameter']} Analysis"):
                    st.write(f"Value: {item['value']}")
                    st.write(f"Status: {item['status']}")
                    st.write(f"Risk Level: {item['risk_level']}")
                    st.write(f"Recommendation: {item['recommendation']}")
                    
    with tab3:
        if 'show_results' in st.session_state and st.session_state.show_results:
            st.header("Recommendations")
            
            # BMI Analysis
            bmi = calculate_bmi(st.session_state.data['weight'], st.session_state.data['height'])
            st.subheader("BMI Analysis")
            st.write(f"Your BMI: {bmi}")
            if bmi < 18.5:
                st.warning("Underweight - Consider nutritional counseling")
            elif bmi < 25:
                st.success("Normal weight - Maintain healthy lifestyle")
            elif bmi < 30:
                st.warning("Overweight - Consider weight management strategies")
            else:
                st.error("Obese - Consult healthcare provider for weight management")
                
            # Lifestyle Recommendations
            recommendations = get_lifestyle_recommendations(st.session_state.data)
            st.subheader("Lifestyle Recommendations")
            
            for rec in recommendations:
                with st.expander(rec['category']):
                    st.write(f"**Recommendation:** {rec['recommendation']}")
                    st.write(f"**Details:** {rec['details']}")

if __name__ == "__main__":
    main()
