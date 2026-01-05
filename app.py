import streamlit as st
from utils.ui import load_css

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Cardio Risk Predictor", 
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Global CSS
load_css("assets/style.css")

# ---------------- IMPORTS ----------------
# Import views after config to ensure set_page_config is first
from views.home import render_home
from views.visualization import render_visualization
from views.about import render_about

# ---------------- BOOTSTRAP ----------------
def main():
    # Sidebar Navigation
    with st.sidebar:
        st.title("❤️ Heart Health")
        
        # You can use st.radio or st.selectbox for standard Streamlit nav
        # For a more modern look, we often style Radio buttons as 'cards' via CSS
        # or use simple clear options.
        page = st.radio(
            "Navigate", 
            ["Home", "Visualizations", "About & Disclaimer"],
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        dark_mode = st.checkbox("Dark Mode Support", value=True, help="Streamlit handles themes automatically based on system settings, but this toggle is a placeholder for custom theme logic if extended.")
        
        st.markdown("---")
        st.markdown("v1.0.0 | Student Project")

    # Routing
    if page == "Home":
        render_home()
    elif page == "Visualizations":
        render_visualization()
    elif page == "About & Disclaimer":
        render_about()

if __name__ == "__main__":
    main()