import streamlit as st

def calculate_heart_risk(age, systolic_bp, cholesterol, diabetes, smoking):
    risk_score = 0
    
    # Age risk
    if age > 65:
        risk_score += 20
    elif age > 55:
        risk_score += 15
    elif age > 45:
        risk_score += 10
        
    # Blood pressure risk
    if systolic_bp >= 180:
        risk_score += 25
    elif systolic_bp >= 160:
        risk_score += 20
    elif systolic_bp >= 140:
        risk_score += 15
        
    # Cholesterol risk
    if cholesterol > 240:
        risk_score += 20
    elif cholesterol > 200:
        risk_score += 15
        
    # Diabetes risk
    if diabetes == 'Yes':
        risk_score += 20
        
    # Smoking risk
    if smoking == 'Yes':
        risk_score += 20
        
    return min(risk_score, 100)  # Cap at 100%

def main():
    st.title('Heart Disease Risk Calculator')
    
    # Input fields
    age = st.number_input('Age', 18, 120, 50)
    systolic_bp = st.number_input('Systolic Blood Pressure', 90, 200, 120)
    cholesterol = st.number_input('Total Cholesterol', 100, 300, 180)
    diabetes = st.selectbox('Diabetes', ['No', 'Yes'])
    smoking = st.selectbox('Smoking', ['No', 'Yes'])
    
    # Calculate button
    if st.button('Calculate Risk'):
        risk_score = calculate_heart_risk(age, systolic_bp, cholesterol, diabetes, smoking)
        
        # Display results
        st.header('Risk Assessment Results')
        
        # Progress bar for risk
        st.progress(risk_score/100)
        
        # Risk level text
        if risk_score < 30:
            st.success(f'Low Risk: {risk_score}%')
        elif risk_score < 60:
            st.warning(f'Moderate Risk: {risk_score}%')
        else:
            st.error(f'High Risk: {risk_score}%')
            
        # Recommendations
        st.subheader('Recommendations:')
        if systolic_bp >= 140:
            st.write('- Monitor your blood pressure regularly')
        if cholesterol > 200:
            st.write('- Consider lifestyle changes to lower cholesterol')
        if smoking == 'Yes':
            st.write('- Consider smoking cessation programs')
        if diabetes == 'Yes':
            st.write('- Maintain regular diabetes checkups')

if __name__ == '__main__':
    main()
