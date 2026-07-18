import streamlit as st
from src.components.home_header import home_header, header_dashboard
from src.components.footer import home_footer, footer_dashboard
from src.ui.base_layout import base_layout,style_background_dashboard,style_background_home
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendence,get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendence,unenroll_student_to_subject
from src.components.subject_card import subject_card
from src.components.dialog_enroll import enroll_dialoge
from src.ui.base_layout import base_layout

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    col1,col2 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    with col1: 
        header_dashboard()
        
    with col2:
        st.subheader(f""" Welcome , {student_data['name']}!""")
        if st.button("Logout + Backspace",type="secondary",key="loginbackbtn"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()
    

    col1,col2 = st.columns(2,vertical_alignment='center',gap="xxlarge")
    base_layout()
    with col1: 
        st.header("Your enrolled subjects")
        
    with col2:
        if st.button("Enroll in suject",type="tertiary",width='stretch'):
            enroll_dialoge()
    
    
    st.divider()

    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs =  get_student_attendence(student_id)
        stats_map = {}
        for log in logs:
            sid = log['subject_id']
            if sid not in stats_map:
                stats_map[sid] = {"total":0,"attended":0}
            stats_map[sid]['total'] += 1
            
            if log.get("is_present"):
                stats_map[sid]["attended"] += 1

        cols = st.columns(2)

        for i,sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sub_id = sub['subject_id']

            stats = stats_map.get(sub_id,{"total":0,"attended":0})
            def  unenroll_btn():
                if st.button('Unenrolled', key=f"unenroll_{sub_id}",type='tertiary',width='stretch'):
                    unenroll_student_to_subject(student_id,sub_id)
                    st.toast(f'Unenrolled from{sub['name']} , successfully')
            
            with cols[i%2]:
               
                subject_card(
                    name = sub['name'],
                    code = sub['subject_code'],
                    section = sub['section'],
                    stats = [
                        ('📅',' Total',stats['total']),        # emoji , key , value
                        ('✅',' Attended',stats['attended'])
                    ],
                    footer_callback= unenroll_btn,
                )
        footer_dashboard()

def student_screen():
    if 'student_data' in st.session_state:
        student_dashboard()
        return 
    col1,col2 = st.columns(2)
    style_background_dashboard()
    base_layout()

    with col1: 
        header_dashboard()
        
    with col2:
        if st.button("Go back to Home  + Backspace",type="secondary",key="loginbackbtn"):
            st.session_state['login_type'] = None  
            st.rerun()

    st.space()
    st.space()
    st.header("Login With FaceId",text_alignment="center")
    st.space()
    show_registration = False
    image_source = st.camera_input("Capture your face to login",key="student_face_login" ,width='stretch')
    if image_source:
        img = np.array(Image.open(image_source))
        with st.spinner('Ai is Scanning...'):
            detected,all_ids,num_faces = predict_attendence(img)
            if num_faces == 0:
                st.error("No face detected. Please try again.")
            elif num_faces > 1:
                st.error("Multiple faces detected. Please ensure only your face is in the frame.")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id),None)
                    if student:
                        st.session_state.student_data = student
                        st.session_state.user_role = 'student'
                        st.session_state.is_logged_in = True
                        st.toast(f'Welcome back  {student['name']}')
                        import time
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognised , you might be a new student')
                    show_registration = True
        if show_registration:
            with st.container(border=True):
                st.header("Register New Profile")
                new_name = st.text_input('Enter your name',placeholder=' e.g Riyanshu ')
                st.subheader('Optional : Voice Only Enrollment')
                st.info("Enroll for Voice Only Attendence")


                audio_data = None
                try:
                    audio_data = st.audio_input('Record a short Phrase i.e I am Present , My Name is Riyanshu')
                except Exception:
                    st.error('Voice input Failed ! ')
                
                if st.button('Create Account',type='primary'):
                    if new_name:
                        with st.spinner('Creating Profile ... '):
                            img = np.array(Image.open(image_source))
                            encodings = get_face_embeddings(img)
                            if encodings:
                                face_emb = encodings[0].tolist()
                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embeddings(audio_data.read())

                                response_data = create_student(new_name,face_embedding = face_emb,voice_embedding=voice_emb)

                                if response_data:
                                    train_classifier()
                                    st.session_state.student_data = response_data[0]
                                    st.session_state.user_role = 'student'
                                    st.session_state.is_logged_in = True
                                    st.toast(f'Profile created! Hi {new_name} !')
                                    import time
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("Cant capture your facial feature for Registration !")

                    else:
                        st.warning('Please enter your name ..')

        

    footer_dashboard()

