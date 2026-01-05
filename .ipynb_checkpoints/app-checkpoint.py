import streamlit as st
import joblib  # Use joblib instead of pickle
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Cardio Risk Predictor", page_icon="❤️")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    # Load using joblib to correctly parse the dictionary
    model_path = "cardio_rf_model.pkl" 
    artifact = joblib.load(model_path)
    
    # Extract the model and features from the dictionary
    model = artifact["model"]
    feature_names = artifact["features"]
    
    return model, feature_names

# Initialize
model, feature_names = load_model()

# ---------------- SIMPLE UI ----------------
st.title("❤️ Heart Disease Predictor")
st.write("Enter the patient details below:")

# Creating a clean 2-column layout for inputs
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", 1, 120, 50)
    gender = st.selectbox("Gender", ["Male", "Female"])
    height = st.number_input("Height (cm)", 100, 250, 170)
    weight = st.number_input("Weight (kg)", 30, 200, 75)

with col2:
    ap_hi = st.number_input("Systolic BP (High)", 80, 250, 120)
    ap_lo = st.number_input("Diastolic BP (Low)", 40, 150, 80)
    cholesterol = st.selectbox("Cholesterol", [1, 2, 3], help="1: Normal, 2: Above Normal, 3: High")
    glucose = st.selectbox("Glucose", [1, 2, 3], help="1: Normal, 2: Above Normal, 3: High")

st.write("---")
c1, c2, c3 = st.columns(3)
smoke = c1.checkbox("Smoking")
alco = c2.checkbox("Alcohol")
active = c3.checkbox("Active", value=True)

if st.button("Predict Risk", use_container_width=True):
    # 1. Feature Engineering
    # Map inputs to match training data
    # Note: Using gender mapping Male=1, Female=2 (Common in Cardio datasets)
    gender_val = 1 if gender == "Male" else 2 
    bmi = weight / ((height / 100) ** 2)
    
    # Prepare the data dictionary
    # 'age' is usually in days in this dataset, 'age_years' is years
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

    # 2. Create DataFrame and align columns
    df = pd.DataFrame([row])
    df = df[feature_names] # Ensure correct order

    # 3. Prediction
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    # 4. Simple Result Display
    st.divider()
    if prediction == 1:
        st.error(f"### Result: High Risk ({probability*100:.1f}%)")
    else:
        st.success(f"### Result: Low Risk ({probability*100:.1f}%)")
    
    st.info(f"Calculated BMI: {bmi:.2f}")