import streamlit as st
from utils.ui import hero_section

def render_about():
    hero_section(title="About The Project", subtitle="Cardiovascular Disease Prediction System")

    with st.container():
        st.markdown("""
        ### 🎯 Project Objective
        The goal of this project is to predict the presence of cardiovascular disease in patients based on their medical history and demographic details. 
        Early detection of heart disease can save lives by enabling timely intervention and lifestyle changes.

        ### 🏗 Architecture
        - **Frontend**: Streamlit (Python)
        - **Backend Logic**: Python
        - **Model**: Random Forest Classifier
        - **Data Processing**: Pandas & Scikit-learn
        
        ### 📚 Dataset
        The dataset consists of 70,000 records of patients data, including:
        - **Objective Features**: Age, Height, Weight, Gender
        - **Examination Features**: Systolic BP, Diastolic BP, Cholesterol, Glucose
        - **Subjective Features**: Smoking, Alcohol, Physical Activity

        ### ⚠️ Disclaimer
        > This application is for **educational purposes only**. The predictions made by this model are based on statistical patterns and should **not** replace professional medical advice. 
        > Always consult a qualified healthcare provider for diagnosis and treatment.
        """)

    st.divider()

    st.markdown("### 👨‍💻 Developed By")
    st.markdown("**Meet Jotaniya**")
   #st.caption("Student Project | B.Tech CSE | 2024")
