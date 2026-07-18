import streamlit as st
from src.ui.base_layout import base_layout,style_background_dashboard,style_background_home
from src.components.footer import footer_dashboard
from src.components.home_header import header_dashboard
from src.database.db import check_teacher_exits,create_teacher,teacher_login,get_teacher_subject
from src.components.dialogue_create_subject import create_dialogue_subject
from src.components.subject_card import subject_card
from src.components.dialogue_share_subject import share_subject
from src.components.dialog_photo_add import add_photo_dialog
from src.pipelines.face_pipeline import predict_attendence
from src.database.config import supabase
import numpy as np
import pandas as pd
from datetime import datetime
from src.components.dialog_attendence_result import attendence_result_dialog
from src.components.dialog_voice_attendence import voice_attendence_dialog
def teacher_screen():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    base_layout()
    if 'teacher_data' in st.session_state:
        teacher_dashboard()
    
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    col1,col2 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    with col1: 
        header_dashboard()
        
    with col2:
        st.subheader(f""" Welcome , {teacher_data['name']}!""")
        if st.button("Logout",type="secondary",key="loginbackbtn"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()
    
    st.space()

    tab1,tab2,tab3 = st.columns(3,vertical_alignment='bottom')
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendence'
      
        
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendence' else "tertiary"
        if st.button('Take Attendence',type=type1,width='stretch',icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendence'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"

        if st.button('Manage Subjects',type=type2,width='stretch',icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()
     
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendence_records' else "tertiary"
        if st.button('Attendence Records',type=type3,width='stretch',icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendence_records'
            st.rerun()

    if st.session_state.current_teacher_tab == 'take_attendence':
        teacher_tab_take_attendence()
        
    if st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == 'attendence_records':
        teacher_tab_attendence_records()

    footer_dashboard()

def teacher_tab_take_attendence():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('take ai attendence')
    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []
    subjects = get_teacher_subject(teacher_id)
    if not subjects:
        st.warning('You havent created any subjects ! So First Create them ..')
        return
    subject_option = {f"{s['name']} - {s['subject_code']}" : s['subject_id'] for s in subjects}
    col1,col2 = st.columns([3,1])
    with col1:
        selected_subjects = st.selectbox('Select Subject',options=list(subject_option.keys()))
    with col2:
        if st.button('Add photos',type='secondary',icon=':material/photo_prints:',width='stretch'):
            add_photo_dialog()
        
    selected_subject_id = subject_option[selected_subjects]

    st.divider()

    if st.session_state.attendence_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx,img in enumerate(st.session_state.attendence_images):
            with gallery_cols[idx % 4]:
                st.image(img,width='stretch',caption=f'Photos {idx+1}')

    has_photos = bool(st.session_state.attendence_images)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button('Clear all photos',width='stretch',type='secondary',icon=':material/delete:',disabled=not has_photos):
            st.session_state.attendence_images = []
            st.rerun()
    with c2:
        has_photos = bool(st.session_state.attendence_images)
        if st.button('Run face anlaysis',width='stretch',type='secondary',icon=':material/analytics:',disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx,img in enumerate(st.session_state.attendence_images):
                    img_np = np.array(img.convert('RGB'))
                    detected,_,_ = predict_attendence(img_np) 
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id,[]).append(f"Photo{idx+1}")

                enrolled_res = supabase.table('subject_students').select('* , students(*)').eq('subject_id',selected_subject_id).execute()
                enrolled_students = enrolled_res.data
                if not enrolled_students:
                    st.warning('No student is enrolled in this course')
                else:
                    result,attendence_to_log = [],[]
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']),[])
                        is_present = len(sources) > 0
                        result.append({
                            "Name":student['name'],
                            "ID":student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status":'✅ Present' if is_present else '❌ Absent',
                        })

                        attendence_to_log.append({
                            "student_id":student['student_id'],
                            "subject_id": selected_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present),
                        })

                attendence_result_dialog(pd.DataFrame(result),attendence_to_log)


    with c3:
        if st.button('Use Voice attendence',width='stretch',type='secondary',icon=':material/mic:'):
            voice_attendence_dialog(selected_subject_id)


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1,col2 = st.columns(2)

    with col1:
        st.header('manage subjects ',width='stretch')
    with col2:
        if st.button('Create New Subject',width='content'):
            create_dialogue_subject(teacher_id)
    # list all subjects
    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("☁️"," Students", sub.get("total_students", 0)),
                ("✅"," Classes", sub.get("total_classes", 0)),
            ]

        def share_button():
            if st.button(f'Share Code:{sub['name']}',key=f"share_{sub['subject_code']}",icon=':material/share:'):
                share_subject(sub['name'],sub['subject_code'])
            st.space()

        subject_card(
            name = sub['name'],
            code = sub['subject_code'],
            section = sub['section'],
            stats = stats,
            footer_callback = share_button
        )
    else:
        st.info('No Subject Found . Create One Above')


def teacher_tab_attendence_records():
    st.header('attendence_records')

def register_teacher(teacher_username,teacher_name,teacher_password,teacher_confirm_password):
    # 1 condition to check if all fields are filled or not
    if not teacher_username or not teacher_name or not teacher_password or not teacher_confirm_password:
        st.error("Please fill in all fields.")
        return False, "Please fill in all fields."
    
    if check_teacher_exits(teacher_username):
        st.error("Username already exists. Please choose a different username.")
        return False, "Username already exists. Please choose a different username."
    
    if teacher_password != teacher_confirm_password:
        st.error("Passwords do not match. Please try again.")
        return False, "Passwords do not match. Please try again."
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True, "Teacher profile created successfully."
    except Exception as e:
        return False, "Unexpected error occurred while creating teacher profile. Please try again later."



def teacher_screen_register():
    col3,col4 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    with col3: 
        header_dashboard()
        
    with col4:
        if st.button("Go back to Home  + Backspace",type="secondary",key="loginbackbtn"):
            st.session_state['login_type'] = None  
    
    st.markdown(
        f"""
            <h2>Register Your Teacher Profile</h2>
        """,unsafe_allow_html=True
    )
   
    teacher_username = st.text_input("Enter your username")
   
    teacher_name = st.text_input("Enter your name")

    teacher_password = st.text_input("Enter your password")
    teacher_confirm_password = st.text_input("confirm your password")
    st.divider()

    col1, col2 = st.columns(2,gap="large")
    with col1:
        if st.button("Register Now  + Enter",type="primary",width='stretch',icon=':material/passkey:',shortcut='control+enter'):
            success, message = register_teacher(teacher_username,teacher_name,teacher_password,teacher_confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = 'login'
                st.rerun()
            else:
                st.error(message)
    with col2:
        if st.button("Login instead",icon=':material/passkey:',type="secondary",width='stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()

def login_teacher(username,password):
    if not username or not password:
        st.error("Please fill in all fields.")
        return None
    teacher = teacher_login(username,password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False

def teacher_screen_login():
    col3,col4 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    with col3: 
        header_dashboard()
        
    with col4:
        if st.button("Go back to Home  + Backspace",type="secondary",key="loginbackbtn"):
            st.session_state['login_type'] = None  
            st.rerun()
    st.space()
    st.space()
    st.header("Login Using Password")
    st.space()

    teacher_username=st.text_input("Enter your username",placeholder='@username')
    teacher_password=st.text_input("Enter your password",type='password',placeholder='********')
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("login Now  + Enter",type="primary",icon=':material/passkey:',shortcut='control+enter',width='stretch'):
            if login_teacher(teacher_username,teacher_password):
                st.toast(" Welcome back , " + teacher_username,icon="☃️")
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("INVALID CREDENTIALS , Please try again or register a new account.")

    with col2:
        if st.button("Register Now",type="secondary",width='stretch',icon=':material/passkey:'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()
            

    footer_dashboard()
    