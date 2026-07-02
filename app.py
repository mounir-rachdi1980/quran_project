import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام الرابطة - المكناسي", layout="wide")

# 2. التنسيق الأساسي (فقط للاتجاه)
st.markdown("""
    <style>
    div.stButton > button:first-child { background-color: #FF4D4D; color: white; }
    </style>
""", unsafe_allow_html=True)

# 3. محاكاة قاعدة البيانات (إذا لم تكن موجودة)
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(columns=['المعرف', 'الاسم', 'المرحلة', 'الوحدة'])

# تعريف المراحل
stages_structure = {
    "المرحلة الأولى": ["الوحدة 1", "الوحدة 2"],
    "المرحلة الثانية": ["الوحدة 1", "الوحدة 2"]
}

menu = ["تسجيل طالب", "عرض الطلاب"]
choice = st.sidebar.selectbox("القائمة", menu)

if choice == "تسجيل طالب":
    st.title("تسجيل طالب جديد")
    with st.form("add_student"):
        name = st.text_input("اسم الطالب")
        stage = st.selectbox("المرحلة", list(stages_structure.keys()))
        unit = st.selectbox("الوحدة", stages_structure[stage])
        if st.form_submit_button("إضافة"):
            new_id = len(st.session_state.students_db) + 1
            st.session_state.students_db = pd.concat([st.session_state.students_db, 
                pd.DataFrame({'المعرف': [new_id], 'الاسم': [name], 'المرحلة': [stage], 'الوحدة': [unit]})], ignore_index=True)
            st.rerun()

elif choice == "عرض الطلاب":
    # عرض التبويبات
    tabs = st.tabs(list(stages_structure.keys()))
    
    for i, stage in enumerate(stages_structure.keys()):
        with tabs[i]:
            # --- هذا هو الجزء الذي يحل مشكلتك: تنسيق مباشر وقوي ---
            st.markdown(f"""
                <h1 style='color: #FF5733; font-size: 35px; font-weight: bold;'>
                {stage}
                </h1>
            """, unsafe_allow_html=True)
            
            # عرض الوحدات والطلاب مع زر حذف
            for unit in stages_structure[stage]:
                st.subheader(unit)
                df = st.session_state.students_db[(st.session_state.students_db['المرحلة'] == stage) & (st.session_state.students_db['الوحدة'] == unit)]
                
                if not df.empty:
                    st.dataframe(df)
                    # زر الحذف داخل كل وحدة
                    student_to_del = st.selectbox(f"اختر طالباً للحذف في {unit}", df['المعرف'], key=f"del_{stage}_{unit}")
                    if st.button(f"حذف بيانات الطالب {student_to_del}", key=f"btn_{stage}_{unit}"):
                        st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['المعرف'] != student_to_del]
                        st.rerun()
                else:
                    st.write("لا يوجد طلاب هنا.")
