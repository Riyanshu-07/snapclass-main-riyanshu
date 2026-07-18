import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialog_attendence_result import show_attendence_results



@st.dialog('Voice attendence ')
def voice_attendence_dialog(selected_subject_id):
    st.write('Record audio of students  saying I am present . Then AI will recognize the students')
    audio_data = None
    audio_data = st.audio_input('Record classroom audio')

    if st.button('Analyze audio',width='stretch',type='primary'):
        with st.spinner('Processing Audio data ...'):
            enrolled_res = supabase.table('subject_students').select('* , students(*)').eq('subject_id',selected_subject_id).execute()
            enrolled_students = enrolled_res.data
            if not enrolled_students:
                st.warning('No student is enrolled in this course')
                return

            candidate_dict = {
                s['students']['student_id']: s['students']['voice_embedding'] for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not candidate_dict:
                st.warning('No student is enrolled with Voice profile registered .. ')
                return
            
            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(audio_bytes,candidate_dict,threshold=0.65)
            result,attendence_to_log = [],[]
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(int(student['student_id']),0)
                is_present = bool(score > 0)
                result.append({
                    "Name":student['name'],
                    "ID":student['student_id'],
                    "Score": score if is_present else "-",
                    "Status":'✅ Present' if is_present else '❌ Absent',
                })

                attendence_to_log.append({
                    "student_id":student['student_id'],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present),
                })

            st.session_state.voice_attendence_results = (pd.DataFrame(result),attendence_to_log)

    if st.session_state.get('voice_attendence_results'):
        st.divider()
        df_results,logs = st.session_state.voice_attendence_results
        show_attendence_results(df_results,logs)