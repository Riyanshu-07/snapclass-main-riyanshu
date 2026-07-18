from src.database.config import supabase
import bcrypt

def check_teacher_exits(username):
    # check for unique username , if username already exists return False
    response = supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0

def hash_pass(pw):
    return bcrypt.hashpw(pw.encode(),bcrypt.gensalt()).decode()



def create_student(studentname,face_embedding=None,voice_embedding=None):
    # create a new student in the database
    data = {"name":studentname , "face_embedding" : face_embedding , "voice_embedding" : voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

def create_teacher(username,password,name):
    # create a new teacher in the database
    data = {"username":username , "password" : hash_pass(password) , "name" : name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def check_pass(pw,hashed_pass):
    return bcrypt.checkpw(pw.encode(),hashed_pass.encode())

def teacher_login(username,password):
    # check if the teacher exists and password is correct
    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password,teacher["password"]):
            return teacher
    else:
        return None

def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data

def create_subject(subject_id,subject_code,name,section,teacher_id):
    # create a new subject in the database
    data = {"subject_code":subject_code, "name" : name ,"subject_id":subject_id , "section" : section,"teacher_id":teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response = supabase.table("subjects").select("*,subject_students(count),attendence_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subjects = response.data
    for sub in subjects:
        sub['total_students'] = sub.get("subject_students",[{}])[0].get('count',0) if sub.get('subject_students') else 0
        attendence = sub.get('attendence_logs',[])
        unique_sessions = len(set(log['timestamp'] for log in attendence))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_students',None)
        sub.pop('attendence_logs',None)

    return subjects


def enroll_student_to_subject(student_id,subject_id):
    data = {'student_id':student_id,"subject_id":subject_id}
    res = supabase.table('subject_students').insert(data).execute()
    return res.data


def unenroll_student_to_subject(student_id,subject_id):
    res = supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return res.data


def get_student_subjects(student_id):
    res = supabase.table('subject_students').select('*,subjects(*)').eq('student_id',student_id).execute()
    return res.data

def get_student_attendence(student_id):
    res = supabase.table('attendence_logs').select('*,subjects(*)').eq('student_id',student_id).execute()
    return res.data

def create_attendance(logs):
    res = supabase.table('attendence_logs').insert(logs).execute()
    return res.data


def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendence_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data