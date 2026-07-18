import streamlit as st
from src.components.home_header import home_header
from src.components.footer import home_footer 
from src.ui.base_layout import base_layout,style_background_dashboard,style_background_home
import os
def home_screen():

   
    home_header()
    base_layout()
    style_background_home()
    col1,col2 = st.columns(2,gap="large")

    with col1:
        st.header("I'm  Student")
        st.image("src/images/mascot-teacher.png", width=120)
        if st.button("Login as Student",key="btn1",type="primary",icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=150)
        if st.button("Login as Teacher",key="btn2",type="primary",icon=':material/arrow_outward:',icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
        
    home_footer()