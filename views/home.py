import streamlit as st
import pandas as pd
import joblib
from utils.ui import hero_section

# Load Model (Cached)
@st.cache_resource
def load_model():
    model_path = "cardio_rf_model.pkl" 
    try:
        artifact = joblib.load(model_path)
        # Handle if the pkl is just the model or a dict
        if isinstance(artifact, dict) and "model" in artifact:
            return artifact["model"], artifact["features"]
        else:
            # Fallback if it's just the model, though original app used dict
            return artifact, None
    except FileNotFoundError:
        return None, None

def render_home():
    # Hero Section
    hero_section(
        title="Heart Disease Risk Predictor",
        subtitle="Advanced Machine Learning Model to assess cardiovascular health risk instantly."
    )

    # Load Model
    model, feature_names = load_model()
    
    if model is None:
        st.error("Error: Model file 'cardio_rf_model.pkl' not found. Please ensure it is in the project directory.")
        return

    st.write("")  # Spacing

    # Container for the form
    with st.container():
        st.markdown("### 📋 Patient Vitals")
        
        # 2 Column Layout for inputs
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("#### Demographics")
            age = st.number_input("Age (years)", 1, 120, 50)
            gender = st.selectbox("Gender", ["Male", "Female"])
            height = st.number_input("Height (cm)", 100, 250, 170)
            weight = st.number_input("Weight (kg)", 30, 200, 75)

        with col2:
            st.markdown("#### Medical Readings")
            ap_hi = st.number_input("Systolic BP (High)", 80, 250, 120, help="Normal range: 90-120")
            ap_lo = st.number_input("Diastolic BP (Low)", 40, 150, 80, help="Normal range: 60-80")
            cholesterol = st.selectbox("Cholesterol Level", [1, 2, 3], format_func=lambda x: {1: "1: Normal", 2: "2: Above Normal", 3: "3: High"}[x])
            glucose = st.selectbox("Glucose Level", [1, 2, 3], format_func=lambda x: {1: "1: Normal", 2: "2: Above Normal", 3: "3: High"}[x])

        st.markdown("---")
        
        # Lifestyle factors
        st.markdown("#### Lifestyle & Habits")
        c1, c2, c3 = st.columns(3)
        with c1:
            smoke = st.checkbox("🚭 Smoker")
        with c2:
            alco = st.checkbox("🍷 Alcohol Consumer")
        with c3:
            active = st.checkbox("🏃 Physically Active", value=True)

        st.write("")
        
        # Predict Button
        predict_btn = st.button("Analyze Risk Profile", type="primary", use_container_width=True)

    if predict_btn:
        # Logic from original app
        gender_val = 1 if gender == "Male" else 2 
        bmi = weight / ((height / 100) ** 2)
        
        # Prepare row using logic (age in days conversion as per original)
        row = {
            "age": age * 365.25,
            "gender": gender_val,
            "height": height,
            "weight": weight,
            "ap_hi": ap_hi,
            "ap_lo": ap_lo,
            "cholesterol": cholesterol,
            "gluc": glucose,
            "smoke": 1 if smoke else 0,
            "alco": 1 if alco else 0,
            "active": 1 if active else 0,
            "age_years": age,
            "bmi": bmi
        }

        # Dataframe creation
        df = pd.DataFrame([row])
        if feature_names:
            df = df[feature_names]

        # Predict
        try:
            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0][1]

            st.write("")
            st.markdown("### 🔍 Risk Assessment Result")
            
            # Result Display
            result_col1, result_col2 = st.columns([1, 2])
            
            with result_col1:
                if prediction == 1:
                    st.markdown("""
                        <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; border: 1px solid #ef5350; text-align: center;">
                            <h1 style="color: #c62828; margin:0;">High Risk</h1>
                            <p style="color: #c62828; margin:0; font-size: 1.2rem;">Action Required</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border: 1px solid #66bb6a; text-align: center;">
                            <h1 style="color: #2e7d32; margin:0;">Low Risk</h1>
                            <p style="color: #2e7d32; margin:0; font-size: 1.2rem;">Keep it up!</p>
                        </div>
                    """, unsafe_allow_html=True)

            with result_col2:
                st.progress(probability, text=f"Calculated Probability: {probability*100:.1f}%")
                st.info(f"**BMI Indicator**: {bmi:.1f} - " + ("Normal" if 18.5 <= bmi <= 25 else "Check BMI chart"))
                if prediction == 1:
                    st.warning("⚠️ The model suggests a high likelihood of cardiovascular issues. Please consult a cardiologist.")
                else:
                    st.success("✅ The model suggests a low likelihood of cardiovascular issues. Maintain a healthy lifestyle.")

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
