import streamlit as st

def home_header():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f"""
        <div style='display:flex; flex-direction: column; align-items:center; justify-content:center;margin-bottom:30px;'>
        <img src = '{logo_url}'style='height:100px'; />
            <h1 styl='text-align:center; color:white;'>SNAP </br>CLASS</h1>
        </div>
        """,unsafe_allow_html=True
    )

def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f"""
        <div style='display:flex;margin-bottom:10px;'>
        <img src = '{logo_url}'style='height:125px';/>
        <h1 style='color:black;font-family: "Climate Crisis", sans-serif;color:#5865F2;font-size:20px;line-height:50px;'>SNAP </br>CLASS</h1>
        </div>
        """,unsafe_allow_html=True
    )