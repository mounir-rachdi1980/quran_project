import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات واجهة التطبيق
st.set_page_config(page_title="نظام إدارة الجمعية القرآنية", layout="wide", page_icon="🕌")
st.markdown("<h1 style='text-align: center; color: #1E4620;'>🕌 نظام إدارة الجمعية القرآنية السحابي</h1>", unsafe_allow_html=True)

# الاتصال بقاعدة بيانات Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# قراءة البيانات ديناميكياً من جوجل
try:
    students_db = conn.read(worksheet="Students", ttl=0)
    grades_db = conn.read(worksheet="Grades", ttl=0)
    settings_db = conn.read(worksheet="Settings", ttl=0)
except:
    students_db = pd.DataFrame(columns=['المعرف', 'الاسم الثلاثي', 'اللقب', 'تاريخ الولادة', 'بطاقة التعريف', 'المهنة'])
    grades_db = pd.DataFrame(columns=['المعرف', 'الحفظ', 'الرواية', 'الدراية', 'الحضور'])
    settings_db = pd.DataFrame([{'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}])

# استخراج الضوارب الحالية
try:
    w = {
        'الحفظ': float(settings_db.iloc[0]['الحفظ']),
        'الرواية': float(settings_db.iloc[0]['الرواية']),
        'الدراية': float(settings_db.iloc[0]['الدراية']),
        'الحضور': float(settings_db.iloc[0]['الحضور'])
    }
except:
    w = {'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}

menu = ["تسجيل طالب جديد", "رصد وتعديل الدرجات", "إعدادات الضوارب (المعاملات)", "استخراج بطاقة الأعداد"]
choice = st.sidebar.selectbox("قائمة التحكم", menu)

# --- إعدادات الضوارب ---
if choice == "إعدادات الضوارب (المعاملات)":
    st.subheader("⚙️ تعديل ضوارب المواد")
    col1, col2, col3, col4 = st.columns(4)
    with col1: w_hifz = st.number_input("ضارب الحفظ", min_value=1.0, value=w['الحفظ'])
    with col2: w_riwaya = st.number_input("ضارب الرواية", min_value=1.0, value=w['الرواية'])
    with col3: w_diraya = st.number_input("ضارب الدراية", min_value=1.0, value=w['الدراية'])
    with col4: w_hodoor = st.number_input("ضارب الحضور", min_value=1.0, value=w['الحضور'])
    
    if st.button("حفظ الضوارب الجديدة"):
        new_settings = pd.DataFrame([{'الحفظ': w_hifz, 'الرواية': w_riwaya, 'الدراية': w_diraya, 'الحضور': w_hodoor}])
        conn.update(worksheet="Settings", data=new_settings)
        st.success("✅ تم تحديث الضوارب في ملف Google Sheets!")

# --- تسجيل طالب جديد ---
elif choice == "تسجيل طالب جديد":
    st.subheader("📝 استمارة بطاقة الإرشادات")
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("الاسم الثلاثي")
            dob = st.date_input("تاريخ الولادة")
            job = st.text_input("المهنة")
        with col2:
            last_name = st.text_input("اللقب")
            cin = st.text_input("رقم بطاقة التعريف")
            
        submitted = st.form_submit_button("حفظ البيانات وتوليد المعرف")
        
        if submitted:
            if name and last_name and cin:
                next_id = 20260001 + len(students_db)
                
                new_student = pd.DataFrame([{
                    'المعرف': next_id, 'الاسم الثلاثي': name, 'اللقب': last_name, 
                    'تاريخ الولادة': str(dob), 'بطاقة التعريف': cin, 'المهنة': job
                }])
                updated_students = pd.concat([students_db, new_student], ignore_index=True)
                conn.update(worksheet="Students", data=updated_students)
                
                new_grade = pd.DataFrame([{'المعرف': next_id, 'الحفظ': 0.0, 'الرواية': 0.0, 'الدراية': 0.0, 'الحضور': 0.0}])
                updated_grades = pd.concat([grades_db, new_grade], ignore_index=True)
                conn.update(worksheet="Grades", data=updated_grades)
                
                st.success(f"🎉 تم التسجيل بنجاح! المعرف: {next_id}")
                st.rerun()
            else:
                st.error("⚠️ يرجى ملء الخانات الأساسية.")

    st.write("### قائمة الطلاب المسجلين:")
    st.dataframe(students_db, use_container_width=True)

# --- رصد الأعداد ---
elif choice == "رصد وتعديل الدرجات":
    st.subheader("📊 دفتر رصد أعداد الطلاب")
    if students_db.empty:
        st.warning("⚠️ لا يوجد طلاب مسجلين حالياً.")
    else:
        merged_df = pd.merge(students_db[['المعرف', 'الاسم الثلاثي', 'اللقب']], grades_db, on='المعرف')
        student_id = st.selectbox("اختر الطالب بالمعرف", merged_df['المعرف'])
        
        current_student = merged_df[merged_df['المعرف'] == student_id].iloc[0]
        st.write(f"📝 رصد درجات: **{current_student['الاسم الثلاثي']} {current_student['اللقب']}**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: hifz = st.number_input("الحفظ", min_value=0.0, max_value=20.0, value=float(current_student['الحفظ']))
        with col2: riwaya = st.number_input("الرواية", min_value=0.0, max_value=20.0, value=float(current_student['الرواية']))
        with col3: diraya = st.number_input("الدراية", min_value=0.0, max_value=20.0, value=float(current_student['الدراية']))
        with col4: hodoor = st.number_input("الحضور", min_value=0.0, max_value=20.0, value=float(current_student['الحضور']))
        
        if st.button("تحديث الدرجات سحابياً"):
            grades_db.loc[grades_db['المعرف'] == student_id, ['الحفظ', 'الرواية', 'الدراية', 'الحضور']] = [hifz, riwaya, diraya, hodoor]
            conn.update(worksheet="Grades", data=grades_db)
            st.success("✅ تم تحديث أعداد الطالب في جوجل شيت!")
            st.rerun()

# --- استخراج بطاقة الأعداد ---
elif choice == "استخراج بطاقة الأعداد":
    st.subheader("🖨️ استخراج وطباعة كشف الأعداد والنتائج")
    if students_db.empty:
        st.warning("⚠️ لا توجد بيانات لاستخراجها.")
    else:
        student_id = st.selectbox("اختر معرف الطالب", students_db['المعرف'])
        s_info = students_db[students_db['المعرف'] == student_id].iloc[0]
        g_info = grades_db[grades_db['المعرف'] == student_id].iloc[0]
        
        total_points = (g_info['الحفظ'] * w['الحفظ']) + (g_info['الرواية'] * w['الرواية']) + (g_info['الدراية'] * w['الدراية']) + (g_info['الحضور'] * w['الحضور'])
        sum_weights = sum(w.values())
        final_score = round(total_points / sum_weights, 2)
        
        result = "ناجح 🎉" if final_score >= 10.0 else "راسب 📑"
        result_color = "#1E4620" if final_score >= 10.0 else "#8B0000"
        
        st.markdown(f"""
        <div style="border: 3px double #1E4620; padding: 25px; border-radius: 10px; background-color: #FAFAFA; direction: rtl; font-family: 'Cairo', sans-serif; text-align: right;">
            <div style="text-align: center;">
                <h2>بطاقة أعداد وتقييم طالب</h2>
                <h4 style="color: gray;">الجمعية القرآنية</h4>
                <hr style="border-top: 2px solid #1E4620;">
            </div>
            <table style="width: 100%; font-size: 18px; margin-bottom: 20px; text-align: right;">
                <tr><td><b>المعرف الخاص:</b> {s_info['المعرف']}</td><td><b>الاسم الثلاثي:</b> {s_info['الاسم الثلاثي']}</td></tr>
                <tr><td><b>اللقب:</b> {s_info['اللقب']}</td><td><b>المهنة:</b> {s_info['المهنة']}</td></tr>
                <tr><td><b>تاريخ الولادة:</b> {s_info['تاريخ الولادة']}</td><td><b>بطاقة التعريف:</b> {s_info['بطاقة التعريف']}</td></tr>
            </table>
            <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 18px;">
                <tr style="background-color: #1E4620; color: white;">
                    <th style="padding: 10px; border: 1px solid black;">المادة</th>
                    <th style="padding: 10px; border: 1px solid black;">العدد (من 20)</th>
                    <th style="padding: 10px; border: 1px solid black;">الضارب</th>
                </tr>
                <tr><td style="padding: 10px; border: 1px solid black;">الحفظ</td><td style="border: 1px solid black;">{g_info['الحفظ']}</td><td style="border: 1px solid black;">{w['الحفظ']}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid black;">الرواية</td><td style="border: 1px solid black;">{g_info['الرواية']}</td><td style="border: 1px solid black;">{w['الرواية']}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid black;">الدراية</td><td style="border: 1px solid black;">{g_info['الدراية']}</td><td style="border: 1px solid black;">{w['الدراية']}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid black;">الحضور</td><td style="border: 1px solid black;">{g_info['الحضور']}</td><td style="border: 1px solid black;">{w['الحضور']}</td></tr>
            </table>
            <br>
            <div style="display: flex; justify-content: space-between; font-size: 20px; padding: 10px; background-color: #EAEAEA; border-radius: 5px; direction: rtl;">
                <div><b>المعدل العام الإجمالي:</b> <span style="color: blue; font-weight: bold;">{final_score} / 20</span></div>
                <div><b>النتيجة النهائية:</b> <span style="color: {result_color}; font-weight: bold;">{result}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)