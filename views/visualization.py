import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ui import hero_section

@st.cache_data
def load_data():
    try:
        # Load dataset (using relative path assuming execution from root)
        df = pd.read_csv("cardio_train.csv", sep=";")
        return df
    except Exception:
        return None

def render_visualization():
    hero_section(title="Data Insights", subtitle="Explore the underlying dataset and risk factor correlations.")
    
    df = load_data()
    if df is None:
        st.warning("⚠️ Dataset 'cardio_train.csv' not found. Visualization unavailable.")
        return

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Distribution", "❤️ Correlations", "📈 Age Analysis"])

    with tab1:
        st.subheader("Dataset Overview")
        st.write(f"Total Records: **{len(df)}**")
        st.dataframe(df.head(), use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            # Target Distribution
            fig_target = px.pie(df, names='cardio', title='Target Distribution (Cardio Disease)', 
                                color_discrete_sequence=['#66bb6a', '#ef5350'],
                                labels={'cardio': 'Disease Presence'})
            fig_target.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_target, use_container_width=True)
        
        with c2:
            # Gender Distribution
            fig_gender = px.bar(df['gender'].value_counts().reset_index(), x='gender', y='count', 
                                title='Gender Distribution (1=Women, 2=Men)',
                                color='gender', color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gender, use_container_width=True)

    with tab2:
        st.subheader("Risk Factors vs. Disease")
        
        # Cholesterol vs Cardio
        fig_col = px.histogram(df, x="cholesterol", color="cardio", barmode="group",
                               title="Cholesterol Levels vs Cardio Disease",
                               labels={"cholesterol": "Cholesterol Level (1: Low, 2: Normal, 3: High)", "cardio": "Disease (0: No, 1: Yes)"},
                               color_discrete_sequence=['#90caf9', '#ffab91'])
        st.plotly_chart(fig_col, use_container_width=True)

        # Weight vs Height Scatter (BMI Proxy)
        fig_scatter = px.scatter(df.sample(2000), x="weight", y="height", color="cardio",
                                 title="Height vs Weight (Sample of 2000 points)",
                                 opacity=0.6,
                                 color_discrete_sequence=['green', 'red'])
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab3:
        st.subheader("Age Impact")
        # Age is in days, convert to years
        df['age_years'] = (df['age'] / 365.25).round().astype(int)
        
        fig_age = px.histogram(df, x="age_years", color="cardio",
                               title="Age Distribution by Disease Status",
                               color_discrete_sequence=['#a5d6a7', '#ef9a9a'],
                               nbins=20)
        st.plotly_chart(fig_age, use_container_width=True)
