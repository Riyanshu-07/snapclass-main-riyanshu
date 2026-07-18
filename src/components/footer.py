import streamlit as st

def home_footer():
    logo_url = "https://i.ibb.co/RTStcBH8/Chat-GPT-Image-Jul-7-2026-at-01-41-15-AM.png"
    st.markdown(
        f"""
        <div style="margin-top:2rem; display:flex; gap:6px; items-align:center; justify-content:center;">
        <p style="font-weight:bold;color:white">created with ❤️ by </p>
        <img src='{logo_url}' style ='max-height:25px'/>
        </div>
        """,unsafe_allow_html=True
    )

def footer_dashboard():
    logo_url = "https://i.ibb.co/RTStcBH8/Chat-GPT-Image-Jul-7-2026-at-01-41-15-AM.png"
    st.markdown(
        f"""
        <div style="margin-top:2rem; display:flex; gap:6px; items-align:center; justify-content:center;">
        <p style="font-weight:bold;color:white">created with ❤️ by </p>
        <img src='{logo_url}' style ='max-height:25px'/>
        </div>
        """,unsafe_allow_html=True
    )
    