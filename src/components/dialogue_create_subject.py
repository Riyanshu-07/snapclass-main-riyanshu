import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_dialogue_subject(teacher_id):
    st.write("Enter the new Details of subject")
    sub_id = st.text_input('Subject id',placeholder='101')
    sub_code = st.text_input('Subject Code',placeholder='CS101')
    sub_name = st.text_input('Subject Name',placeholder='Introduction to CS')
    sub_section = st.text_input('Section',placeholder='A')

    if st.button('Create Subject Now',type='primary',width='stretch'):
        if sub_code or sub_name or sub_section:
            try:
                create_subject(sub_id,sub_code,sub_name,sub_section,teacher_id)
                st.toast("Subject Created successfully !")
                st.rerun()
            except Exception as e:
                st.error(f" Error :  {str(e)}")
        else:
            st.error("Please fill the fields")