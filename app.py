import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام الرابطة - المكناسي", layout="wide")

# 2. التنسيق القوي (CSS) - لا تتغير
st.markdown("""
    <style>
    .big-font { font-size: 30px !important; font-weight: bold !important; color: #FF5733 !important; }
    .unit-box { border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. تهيئة البيانات (Session State)
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(columns=['المعرف', 'الاسم', 'المرحلة', 'الوحدة', 'الحفظ', 'الرواية', 'الدراية', 'الحضور'])
if 'weights' not in st.session_state:
    st.session_state.weights = {'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}

# تعريف الهيكل
stages_structure = {
    "المرحلة الأولى: رواية قالون": ["الوحدة 1", "الوحدة 2", "الوحدة 3"],
    "المرحلة الثانية: نافع وحفص": ["الوحدة 1", "الوحدة 2"],
    "المرحلة الثالثة: القراءات": ["الوحدة 1", "الوحدة 2"]
}

# القائمة الجانبية
menu = ["تسجيل طالب", "عرض وإدارة", "رصد الدرجات", "إعدادات الضوارب", "بطاقة الأعداد"]
choice = st.sidebar.selectbox("القائمة", menu)

# --- 1. التسجيل ---
if choice == "تسجيل طالب":
    st.markdown("<p class='big-font'>تسجيل طالب جديد</p>", unsafe_allow_html=True)
    with st.form("add_student"):
        name = st.text_input("اسم الطالب")
        stage = st.selectbox("المرحلة", list(stages_structure.keys()))
        unit = st.selectbox("الوحدة", stages_structure[stage])
        if st.form_submit_button("حفظ"):
            new_id = 20260001 + len(st.session_state.students_db)
            new_row = pd.DataFrame({'المعرف': [new_id], 'الاسم': [name], 'المرحلة': [stage], 'الوحدة': [unit], 'الحفظ': [0.0], 'الرواية': [0.0], 'الدراية': [0.0], 'الحضور': [0.0]})
            st.session_state.students_db = pd.concat([st.session_state.students_db, new_row], ignore_index=True)
            st.success(f"تم تسجيل الطالب بنجاح! المعرف: {new_id}")

# --- 2. العرض والإدارة ---
elif choice == "عرض وإدارة":
    tabs = st.tabs(list(stages_structure.keys()))
    for i, stage in enumerate(stages_structure.keys()):
        with tabs[i]:
            for unit in stages_structure[stage]:
                st.markdown(f"<div class='unit-box'><strong>{unit}</strong></div>", unsafe_allow_html=True)
                df = st.session_state.students_db[(st.session_state.students_db['المرحلة'] == stage) & (st.session_state.students_db['الوحدة'] == unit)]
                if not df.empty:
                    st.dataframe(df[['المعرف', 'الاسم']])
                else:
                    st.write("لا يوجد طلاب.")

# --- 3. رصد الدرجات ---
elif choice == "رصد الدرجات":
    if not st.session_state.students_db.empty:
        s_id = st.selectbox("اختر معرف الطالب", st.session_state.students_db['المعرف'])
        idx = st.session_state.students_db[st.session_state.students_db['المعرف'] == s_id].index[0]
        
        c1, c2, c3, c4 = st.columns(4)
        hifz = c1.number_input("الحفظ", value=float(st.session_state.students_db.at[idx, 'الحفظ']))
        riwaya = c2.number_input("الرواية", value=float(st.session_state.students_db.at[idx, 'الرواية']))
        diraya = c3.number_input("الدراية", value=float(st.session_state.students_db.at[idx, 'الدراية']))
        hodoor = c4.number_input("الحضور", value=float(st.session_state.students_db.at[idx, 'الحضور']))
        
        if st.button("تحديث الدرجات"):
            st.session_state.students_db.at[idx, ['الحفظ', 'الرواية', 'الدراية', 'الحضور']] = [hifz, riwaya, diraya, hodoor]
            st.success("تم التحديث!")

# --- 4. الضوارب والبطاقة (أضف المنطق الخاص بك هنا بنفس الطريقة) ---
