import streamlit as st
import base64

def load_css(file_name):
    """Loads a CSS file into Streamlit"""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def hero_section(title, subtitle):
    """Renders a Hero section with custom HTML/CSS"""
    st.markdown(f"""
        <div class="hero-container">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)

def card_container(key=None):
    """
    Returns a container that effectively acts as a card provided 
    you wrap your content in it (Styling handled via CSS usually, 
    but Streamlit containers are raw).
    Custom HTML wrapper is often better for visual 'boxed' effect.
    """
    return st.container()
