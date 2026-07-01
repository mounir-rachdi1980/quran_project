import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الواجهة والربط السحابي الثابت
st.set_page_config(page_title="نظام إدارة الجمعية القرآنية", layout="wide", page_icon="🕌")
st.markdown("<style>[data-testid='stSidebar'] {direction: rtl; text-align: right;} .main .block-container {direction: rtl; text-align: right;} div[data-testid='stForm'] {direction: rtl; text-align: right;} th, td {text-align: right !important;}</style>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #1E4620;'>🕌 نظام إدارة الجمعية القرآنية السحابي</h1>", unsafe_allow_html=True)

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    students_df = conn.read(worksheet="Students", ttl=0).dropna(how='all')
    grades_df = conn.read(worksheet="Grades", ttl=0).dropna(how='all')
    settings_df = conn.read(worksheet="Settings", ttl=0).dropna(how='all')
    weights = {'الحفظ': float(settings_df.iloc['الحفظ']), 'الرواية': float(settings_df.iloc['الرواية']), 'الدراية': float(settings_df.iloc['الدراية']), 'الحضور': float(settings_df.iloc['الحضور'])} if not settings_df.empty else {'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}
except:
    st.error("⚠️ فشل الاتصال بقاعدة البيانات السحابية. يرجى التحقق من إعداد الرابط السري في الـ Secrets.")
    st.stop()

menu = ["تسجيل طالب جديد", "رصد وتعديل الدرجات", "إعدادات الضوارب (المعاملات)", "استخراج بطاقة الأعداد"]
choice = st.sidebar.selectbox("قائمة التحكم", menu)

if choice == "إعدادات الضوارب (المعاملات)":
    st.subheader("⚙️ تعديل ضوارب المواد")
    col1, col2, col3, col4 = st.columns(4)
    w_hifz = col1.number_input("ضارب الحفظ", min_value=1.0, value=weights['الحفظ'])
    w_riwaya = col2.number_input("ضارب الرواية", min_value=1.0, value=weights['الرواية'])
    w_diraya = col3.number_input("ضارب الدراية", min_value=1.0, value=weights['الدراية'])
    w_hodoor = col4.number_input("ضارب الحضور", min_value=1.0, value=weights['الحضور'])
    if st.button("حفظ الضوارب الجديدة سحابياً"):
        conn.update(worksheet="Settings", data=pd.DataFrame([{'الحفظ': w_hifz, 'الرواية': w_riwaya, 'الدراية': w_diraya, 'الحضور': w_hodoor}]))
        st.success("✅ تم تحديث الضوارب السحابية بنجاح!")
        st.cache_data.clear()

elif choice == "تسجيل طالب جديد":
    st.subheader("📝 استمارة بطاقة الإرشادات")
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم الثلاثي")
        dob = col1.date_input("تاريخ الولادة")
        job = col1.text_input("المهنة")
        last_name = col2.text_input("الالقب")
        cin = col2.text_input("رقم بطاقة التعريف")
        if st.form_submit_button("حفظ البيانات وتوليد المعرف"):
            if name and last_name and cin:
                next_id = 20260001 + len(students_df)
                conn.update(worksheet="Students", data=pd.concat([students_df, pd.DataFrame([{'المعرف': next_id, 'الاسم الثلاثي': name, 'الالقب': last_name, 'تاريخ الولادة': str(dob), 'بطاقة التعريف': cin, 'المهنة': job}])], ignore_index=True))
                conn.update(worksheet="Grades", data=pd.concat([grades_df, pd.DataFrame([{'المعرف': next_id, 'الحفظ': 0.0, 'الرواية': 0.0, 'الدراية': 0.0, 'الحضور': 0.0}])], ignore_index=True))
                st.success(f"🎉 تم حفظ البيانات سحابياً بنجاح! المعرف: {next_id}")
                st.cache_data.clear()
                st.rerun()
            else: st.error("⚠️ يرجى ملء الخانات الأساسية.")
    st.write("### قائمة الطلاب المسجلين:")
    st.dataframe(students_df, use_container_width=True, hide_index=True)

elif choice == "رصد وتعديل الدرجات":
    st.subheader("📊 دفتر رصد أعداد الطلاب")
    if students_df.empty: st.warning("⚠️ لا يوجد طلاب مسجلين.")
    else:
        students_df['المعرف'], grades_df['المعرف'] = students_df['المعرف'].astype(int), grades_df['المعرف'].astype(int)
        merged = pd.merge(students_df[['المعرف', 'الاسم الثلاثي', 'الالقب']], grades_df, on='المعرف')
        student_id = st.selectbox("اختر الطالب بالمعرف", merged['المعرف'])
        current_student = merged[merged['المعرف'] == student_id].iloc[0]
        st.write(f"📝 رصد درجات الطالب: **{current_student['الاسم الثلاثي']} {current_student['الالقب']}**")
        col1, col2, col3, col4 = st.columns(4)
        hifz = col1.number_input("الحفظ", min_value=0.0, max_value=20.0, value=float(current_student['الحفظ']))
        riwaya = col2.number_input("الرواية", min_value=0.0, max_value=20.0, value=float(current_student['الرواية']))
        diraya = col3.number_input("الدراية", min_value=0.0, max_value=20.0, value=float(current_student['الدراية']))
        hodoor = col4.number_input("الحضور", min_value=0.0, max_value=20.0, value=float(current_student['الحضور']))
        if st.button("تحديث وحفظ الدرجات سحابياً"):
            grades_df.loc[grades_df['المعرف'] == student_id, ['الحفظ', 'الرواية', 'الدراية', 'الحضور']] = [hifz, riwaya, diraya, hodoor]
            conn.update(worksheet="Grades", data=grades_df)
            st.success("✅ تم تحديث أعداد الطالب سحابياً!")
            st.cache_data.clear()
            st.rerun()

elif choice == "استخراج بطاقة الأعداد":
    st.subheader("🖨️ استخراج وطباعة كشف النتائج")
    if students_df.empty: st.warning("⚠️ لا توجد بيانات طلاب.")
    else:
        students_df['المعرف'], grades_df['المعرف'] = students_df['المعرف'].astype(int), grades_df['المعرف'].astype(int)
        student_id = st.selectbox("اختر معرف الطالب", students_df['المعرف'])
        s_info = students_df[students_df['المعرف'] == student_id].iloc[0]
        g_info = grades_df[grades_df['المعرف'] == student_id].iloc[0]
        total_points = (g_info['الحفظ'] * weights['الحفظ']) + (g_info['الرواية'] * weights['الرواية']) + (g_info['الدراية'] * weights['الدراية']) + (g_info['الحضور'] * weights['الحضور'])
        final_score = round(total_points / sum(weights.values()), 2)
        result = "ناجح 🎉" if final_score >= 10.0 else "راسب 📑"
        result_color = "#1E4620" if final_score >= 10.0 else "#8B0000"
        
        # كشف الأعداد المنسق والمحمي سحابياً بالكامل
        st.markdown(f"<div style='border: 3px double #1E4620; padding: 20px; border-radius: 10px; background-color: #FAFAFA; direction: r_t_l; text-align: right;'> <div style='text-align: center;'> <h2>بطاقة تقييم طالب سنوي</h2> <h4 style='color: gray;'>الجمعية القرآنية الموقرة</h4> <hr style='border-top: 2px solid #1E4620;'> </div> <table style='width: 100%; font-size: 18px; margin-bottom: 20px; text-align: right;'> <tr><td><b>المعرف الخاص:</b> {s_info['المعرف']}</td><td><b>الاسم الثلاثي:</b> {s_info['الاسم الثلاثي']}</td></tr> <tr><td><b>اللقب:</b> {s_info['الالقب']}</td><td><b>المهنة:</b> {s_info['المهنة']}</td></tr> <tr><td><b>تاريخ الولادة:</b> {s_info['تاريخ الولادة']}</td><td><b>بطاقة التعريف:</b> {s_info['بطاقة التعريف']}</td></tr> </table> <table style='width: 100%; border-collapse: collapse; text-align: center; font-size: 18px;'> <tr style='background-color: #1E4620; color: white;'> <th style='padding: 10px; text-align: center !important;'>المادة</th> <th style='padding: 10px; text-align: center !important;'>العدد</th> <th style='padding: 10px; text-align: center !important;'>الضارب</th> </tr> <tr><td>الحفظ</td><td>{g_info['الحفظ']}</td><td>{weights['الحفظ']}</td></tr> <tr><td>الرواية</td><td>{g_info['الرواية']}</td><td>{weights['الرواية']}</td></tr> <tr><td>الدراية</td><td>{g_info['الدراية']}</td><td>{weights['الدراية']}</td></tr> <tr><td>الحضور</td><td>{g_info['الحضور']}</td><td>{weights['الحضور']}</td></tr> </table> <br> <div style='font-size: 20px; padding: 10px; background-color: #EAEAEA; border-radius: 5px;'> <b>المعدل العام الإجمالي:</b> <span style='color: blue;'>{final_score} / 20</span> | <b>النتيجة:</b> <span style='color: {result_color};'>{result}</span> </div> </div>", unsafe_allow_html=True)
