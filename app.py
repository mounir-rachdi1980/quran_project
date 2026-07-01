import streamlit as st
import pandas as pd
# إعدادات الواجهة والربط المباشر بدون Secrets لتجنب أخطاء الترجمة
st.set_page_config(page_title="نظام إدارة الجمعية القرآنية", layout="wide", page_icon="🕌")
st.markdown("<style>[data-testid='stSidebar'] {direction: rtl; text-align: right;} .main .block-container {direction: rtl; text-align: right;} div[data-testid='stForm'] {direction: rtl; text-align: right;} th, td {text-align: right !important;}</style>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #1E4620;'>🕌 نظام إدارة الجمعية القرآنية السحابي</h1>", unsafe_allow_html=True)
# الرابط المباشر المكشوف للخادم لضمان القراءة الفورية
sheet_url = "https://docs.google.com/spreadsheets/d/ضع_هنا_رابط_جدولك_الخاص/export?format=csv"
try:
    # قراءة البيانات سحابياً بشكل مباشر عبر الرابط الثابت لكل تبويب
    students_df = pd.read_csv(sheet_url + "&gid=0").dropna(how='all')
    grades_df = pd.read_csv(sheet_url + "&gid=1351113271").dropna(how='all')
    settings_df = pd.read_csv(sheet_url + "&gid=186638064").dropna(how='all')
    weights = {'الحفظ': float(settings_df.iloc[0]['الحفظ']), 'الرواية': float(settings_df.iloc[0]['الرواية']), 'الدراية': float(settings_df.iloc[0]['الدراية']), 'الحضور': float(settings_df.iloc[0]['الحضور'])} if not settings_df.empty else {'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}
except:
    st.error("⚠️ جاري الاتصال بقاعدة البيانات السحابية الحية... يرجى تحديث الصفحة.")
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
    st.info("ℹ️ لحفظ المعاملات الجديدة، يرجى تحديثها مباشرة في جدول الإعدادات السحابي.")
elif choice == "تسجيل طالب جديد":
    st.subheader("📝 استمارة بطاقة الإرشادات")
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("الاسم الثلاثي")
        dob = col1.date_input("تاريخ الولادة")
        job = col1.text_input("المهنة")
        last_name = col2.text_input("اللقب")
        cin = col2.text_input("رقم بطاقة التعريف")
        if st.form_submit_button("عرض المعرف التلقائي الجديد"):
            if name and last_name and cin:
                next_id = 20260001 + len(students_df)
                st.success(f"🎉 المعرف التلقائي المخصص للطالب القادم هو: {next_id} . يرجى تدوين بياناته في جدول جوجل لتعكس سحابياً فوراً.")
            else: st.error("⚠️ يرجى ملء الخانات الأساسية.")
    st.write("### قائمة الطلاب المسجلين حالياً في قاعدة البيانات:")
    st.dataframe(students_df, use_container_width=True, hide_index=True)
elif choice == "رصد وتعديل الدرجات":
    st.subheader("📊 دفتر رصد أعداد الطلاب السحابي")
    if students_df.empty: st.warning("⚠️ لا يوجد طلاب مسجلين حالياً.")
    else:
        students_df['المعرف'], grades_df['المعرف'] = students_df['المعرف'].astype(int), grades_df['المعرف'].astype(int)
        merged = pd.merge(students_df[['المعرف', 'الاسم الثلاثي', 'اللقب']], grades_df, on='المعرف')
        student_id = st.selectbox("اختر الطالب بالمعرف", merged['المعرف'])
        current_student = merged[merged['المعرف'] == student_id].iloc[0]
        st.write(f"📝 الدرجات الحالية للطالب: **{current_student['الاسم الثلاثي']} {current_student['اللقب']}**")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("الحفظ", f"{current_student['الحفظ']} / 20")
        col2.metric("الرواية", f"{current_student['الرواية']} / 20")
        col3.metric("الدراية", f"{current_student['الدراية']} / 20")
        col4.metric("الحضور", f"{current_student['الحضور']} / 20")
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
        st.markdown(f"<div style='border: 3px double #1E4620; padding: 20px; border-radius: 10px; background-color: #FAFAFA; direction: rtl; text-align: right;'> <div style='text-align: center;'> <h2>بطاقة تقييم طالب سنوي</h2> <h4 style='color: gray;'>الجمعية القرآنية الموقرة</h4> <hr style='border-top: 2px solid #1E4620;'> </div> <table style='width: 100%; font-size: 18px; margin-bottom: 20px; text-align: right;'> <tr><td><b>المعرف الخاص:</b> {s_info['المعرف']}</td><td><b>الاسم الثلاثي:</b> {s_info['الاسم الثلاثي']}</td></tr> <tr><td><b>اللقب:</b> {s_info['الالقب']}</td><td><b>المهنة:</b> {s_info['المهنة']}</td></tr> <tr><td><b>تاريخ الولادة:</b> {s_info['تاريخ الولادة']}</td><td><b>بطاقة التعريف:</b> {s_info['بطاقة التعريف']}</td></tr> </table> <table style='width: 100%; border-collapse: collapse; text-align: center; font-size: 18px;'> <tr style='background-color: #1E4620; color: white;'> <th style='padding: 10px; text-align: center !important;'>المادة</th> <th style='padding: 10px; text-align: center !important;'>العدد</th> <th style='padding: 10px; text-align: center !important;'>الضارب</th> </tr> <tr><td>الحفظ</td><td>{g_info['الحفظ']}</td><td>{weights['الحفظ']}</td></tr> <tr><td>الرواية</td><td>{g_info['الرواية']}</td><td>{weights['الرواية']}</td></tr> <tr><td>الدراية</td><td>{g_info['الدراية']}</td><td>{weights['الدراية']}</td></tr> <tr><td>الحضور</td><td>{g_info['الحضور']}</td><td>{weights['الحضور']}</td></tr> </table> <br> <div style='font-size: 20px; padding: 10px; background-color: #EAEAEA; border-radius: 5px;'> <b>المعدل العام الإجمالي:</b> <span style='color: blue;'>{final_score} / 20</span> | <b>النتيجة:</b> <span style='color: {result_color};'>{result}</span> </div> </div>", unsafe_allow_html=True)
