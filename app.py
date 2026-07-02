import streamlit as st
import pandas as pd

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="نظام الفرع المحلي للرابطة الوطنية للقرآن الكريم بالمكناسي", layout="wide", page_icon="🕌")

# 2. إضافة التنسيقات البصرية المطلوبة (الألوان، التسطير، الأحجام، وتفتيح الشعار)
st.markdown("""
    <style>
    /* تفعيل اتجاه لغة الضاد */
    [data-testid="stSidebar"], .main .block-container, div[data-testid="stForm"], .stDataFrame {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stMarkdown, p, label {
        text-align: right !important;
    }
    
    /* توسيط الاستمارة */
    div[data-testid="stForm"] {
        margin: 0 auto !important;
        max-width: 900px !important; 
    }
    
    /* ضبط حقول الإدخال */
    input, select, textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    div[data-testid="stHorizontalBlock"] {
        direction: rtl !important;
    }
    
    /* 🔴 اسم الفرع الرئيسي: أحمر فاتح ومسطر */
    .main-title { 
        color: #FF4D4D !important; 
        text-align: center !important;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        font-size: 32px !important;
        text-decoration: underline !important; /* إضافة تسطير تحت الاسم */
    } 
    
    /* 🟢 عناوين الاستمارات والقوائم الموحدة: نفس الحجم (24px)، لون أخضر فاتح، ومسطرة */
    .custom-heading { 
        color: #2ECC71 !important; /* لون أخضر فاتح زاهي */
        text-align: center !important;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        font-size: 24px !important; /* توحيد الحجم */
        text-decoration: underline !important; /* إضافة تسطير */
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* عناوين القوائم الجانبية أو الصغرى المسطرة أيضاً بلون أخضر فاتح وبنفس الحجم للاتساق */
    h2, h3, h4 {
        color: #2ECC71 !important;
        font-size: 24px !important;
        text-decoration: underline !important;
        text-align: right !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الترويسة: الشعار في الأعلى (مع زيادة السطوع والتفتيح برمجياً) وتحته اسم الفرع مسطراً
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/mounir-rachdi1980/quran_project/main/logo.jpg" width="150" style="display: block; margin: 0 auto; filter: brightness(1.25); /* تفتيح لون الشعار */">
        <h1 class="main-title" style="margin-top: 20px; margin-bottom: 25px;">نظام الفرع المحلي للرابطة الوطنية للقرآن الكريم بالمكناسي</h1>
    </div>
""", unsafe_allow_html=True)


# --- محاكاة قاعدة البيانات وجلسة العمل ---
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(columns=['المعرف', 'الاسم الثلاثي', 'اللقب', 'تاريخ الولادة', 'بطاقة التعريف', 'المهنة'])
if 'grades_db' not in st.session_state:
    st.session_state.grades_db = pd.DataFrame(columns=['المعرف', 'الحفظ', 'الرواية', 'الدراية', 'الحضور'])
if 'weights' not in st.session_state:
    st.session_state.weights = {'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}

w = st.session_state.weights

menu = ["تسجيل طالب جديد", "رصد وتعديل الدرجات", "إعدادات الضوارب (المعاملات)", "استخراج بطاقة الأعداد"]
choice = st.sidebar.selectbox("قائمة التحكم والتنقل :", menu)

# --- تسجيل طالب جديد ---
if choice == "تسجيل طالب جديد":
    st.markdown('<p class="custom-heading">📝 استمارة بطاقة إرشادات طالب جديد</p>', unsafe_allow_html=True)
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("الاسم الثلاثي :")
            dob = st.date_input("تاريخ الولادة :")
            job = st.text_input("المهنة / المستوى الدراسي :")
        with col2:
            last_name = st.text_input("اللقب (اسم العائلة) :")
            cin = st.text_input("رقم بطاقة التعريف الوطنية / رقم القيد :")
            
        submitted = st.form_submit_button("حفظ بيانات الطالب وتوليد المعرف")
        
        if submitted:
            if name and last_name and cin:
                next_id = 20260001 + len(st.session_state.students_db)
                new_student = pd.DataFrame([{'المعرف': next_id, 'الاسم الثلاثي': name, 'اللقب': last_name, 'تاريخ الولادة': str(dob), 'بطاقة التعريف': cin, 'المهنة': job}])
                st.session_state.students_db = pd.concat([st.session_state.students_db, new_student], ignore_index=True)
                
                new_grade = pd.DataFrame([{'المعرف': next_id, 'الحفظ': 0.0, 'الرواية': 0.0, 'الدراية': 0.0, 'الحضور': 0.0}])
                st.session_state.grades_db = pd.concat([st.session_state.grades_db, new_grade], ignore_index=True)
                
                st.success(f"🎉 تم تسجيل الطالب بنجاح! المعرف الرقمي الخاص به هو : {next_id}")
                st.rerun()
            else:
                st.error("⚠️ يرجى ملء الخانات الأساسية المطلوبة.")

    st.markdown('<p class="custom-heading" style="text-align: right !important;">👥 قائمة الطلاب المسجلين حالياً :</p>', unsafe_allow_html=True)
    st.dataframe(st.session_state.students_db, use_container_width=True)

# --- رصد الأعداد والدرجات ---
elif choice == "رصد وتعديل الدرجات":
    st.markdown('<p class="custom-heading">📊 دفتر رصد أعداد وتقييمات الطلاب</p>', unsafe_allow_html=True)
    if st.session_state.students_db.empty:
        st.warning("⚠️ لا يوجد طلاب مسجلون حالياً في النظام لرصد أعدادهم.")
    else:
        merged_df = pd.merge(st.session_state.students_db[['المعرف', 'الاسم الثلاثي', 'اللقب']], st.session_state.grades_db, on='المعرف')
        student_id = st.selectbox("اختر معرف الطالب المراد رصد درجاته :", merged_df['المعرف'])
        
        current_student = merged_df[merged_df['المعرف'] == student_id].iloc[0]
        st.markdown(f"<h4>📝 رصد ودرجات الطالب الحالي : {current_student['الاسم الثلاثي']} {current_student['اللقب']}</h4>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1: hifz = st.number_input("مادة الحفظ (من 20) :", min_value=0.0, max_value=20.0, value=float(current_student['الحفظ']))
        with col2: riwaya = st.number_input("مادة الرواية (من 20) :", min_value=0.0, max_value=20.0, value=float(current_student['الرواية']))
        with col3: diraya = st.number_input("مادة الدراية (من 20) :", min_value=0.0, max_value=20.0, value=float(current_student['الدراية']))
        with col4: hodoor = st.number_input("مادة الحضور المواظبة (من 20) :", min_value=0.0, max_value=20.0, value=float(current_student['الحضور']))
        
        if st.button("تحديث وحفظ درجات الطالب"):
            st.session_state.grades_db.loc[st.session_state.grades_db['المعرف'] == student_id, ['الحفظ', 'الرواية', 'الدراية', 'الحضور']] = [hifz, riwaya, diraya, hodoor]
            st.success("✅ تم تحديث وحفظ أعداد الطالب بنجاح في النظام!")

# --- إعدادات الضوارب ---
elif choice == "إعدادات الضوارب (المعاملات)":
    st.markdown('<p class="custom-heading">⚙️ تعديل ضوارب المواد (المعاملات)</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: w_hifz = st.number_input("ضارب مادة الحفظ :", min_value=1.0, value=w['الحفظ'])
    with col2: w_riwaya = st.number_input("ضارب مادة الرواية :", min_value=1.0, value=w['الرواية'])
    with col3: w_diraya = st.number_input("ضارب مادة الدراية :", min_value=1.0, value=w['الدراية'])
    with col4: w_hodoor = st.number_input("ضارب مادة الحضور :", min_value=1.0, value=w['الحضور'])
    
    if st.button("حفظ الضوارب الجديدة"):
        st.session_state.weights = {'الحفظ': w_hifz, 'الرواية': w_riwaya, 'الدراية': w_diraya, 'الحضور': w_hodoor}
        st.success("✅ تم تحديث ضوارب المواد بنجاح!")

# --- استخراج بطاقة الأعداد ---
elif choice == "استخراج بطاقة الأعداد":
    st.markdown('<p class="custom-heading">🖨️ استخراج وطباعة كشف الأعداد السنوي</p>', unsafe_allow_html=True)
    if st.session_state.students_db.empty:
        st.warning("⚠️ لا توجد بيانات طلاب متوفرة لاستخراج الكشوفات.")
    else:
        student_id = st.selectbox("اختر معرف الطالب لإنتاج كشفه :", st.session_state.students_db['المعرف'])
        s_info = st.session_state.students_db[st.session_state.students_db['المعرف'] == student_id].iloc[0]
        g_info = st.session_state.grades_db[st.session_state.grades_db['المعرف'] == student_id].iloc[0]
        
        total_points = (g_info['الحفظ'] * w['الحفظ']) + (g_info['الرواية'] * w['الرواية']) + (g_info['الدراية'] * w['الدراية']) + (g_info['الحضور'] * w['الحضور'])
        sum_weights = sum(w.values())
        final_score = round(total_points / sum_weights, 2)
        
        result = "ناجح ومبارك له 🎉" if final_score >= 10.0 else "راسب وله فرصة تدارك 📑"
        result_color = "#27AE60" if final_score >= 10.0 else "#8B0000"
        
        st.markdown(f"""
        <div style="border: 3px double #FF4D4D; padding: 25px; border-radius: 10px; background-color: #FAFAFA; direction: rtl; font-family: 'Cairo', sans-serif; text-align: right; margin: 0 auto; max-width: 900px;">
            <div style="text-align: center;">
                <h2 style="margin: 0; color: #FF4D4D; text-decoration: underline;">بطاقة تقييم وكشف أعداد طالب سنوي</h2>
                <h4 style="color: gray; margin-top: 5px; text-decoration: none;">الفرع المحلي للرابطة الوطنية للقرآن الكريم بالمكناسي</h4>
                <hr style="border-top: 2px solid #FF4D4D; margin: 15px 0;">
            </div>
            <table style="width: 100%; font-size: 18px; margin-bottom: 20px; text-align: right; direction: rtl; border: none; color: #333;">
                <tr><td style="padding: 5px; border:none;"><b>المعرف الخاص :</b> {s_info['المعرف']}</td><td style="padding: 5px; border:none;"><b>الاسم الكامل :</b> {s_info['الاسم الثلاثي']} {s_info['اللقب']}</td></tr>
                <tr><td style="padding: 5px; border:none;"><b>المهنة / الصفة :</b> {s_info['المهنة']}</td><td style="padding: 5px; border:none;"><b>تاريخ الولادة :</b> {s_info['تاريخ الولادة']}</td></tr>
                <tr><td style="padding: 5px; border:none;"><b>بطاقة التعريف الوطنية :</b> {s_info['بطاقة التعريف']}</td><td style="padding: 5px; border:none;"></td></tr>
            </table>
            <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 18px; direction: rtl;">
                <tr style="background-color: #FF4D4D; color: white;">
                    <th style="padding: 10px; border: 1px solid black; text-align: center !important;">المادة التقييمية</th>
                    <th style="padding: 10px; border: 1px solid black; text-align: center !important;">العدد المرصود (من 20)</th>
                    <th style="padding: 10px; border: 1px solid black; text-align: center !important;">ضارب المادة</th>
                </tr>
                <tr><td style="padding: 10px; border: 1px solid black; text-align: right;">مادة الحفظ والأداء</td><td style="border: 1px solid black; padding: 10px;">{g_info['الحفظ']}</td><td style="border: 1px solid black; padding: 10px;">{w['الحفظ']}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid black; text-align: right;">مادة الرواية والقواعد</td><td style="border: 1px solid black; padding: 10px;">{g_info['الرواية']}</td><td style="border: 1px solid black; padding: 10px;">{w['الرواية']}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid black; text-align: right;">مادة الدراية والتفسير</td><td style="border: 1px solid black; padding: 10px;">{g_info['الدراية']}</td><td style="border: 1px solid black; padding: 10px;">{w['الدراية']}</td></tr>
                <tr><td style="padding: 10px; border: 1px solid black; text-align: right;">مادة الحضور والمواظبة</td><td style="border: 1px solid black; padding: 10px;">{g_info['الحضور']}</td><td style="border: 1px solid black; padding: 10px;">{w['الحضور']}</td></tr>
            </table>
            <div style="margin-top: 20px; font-size: 20px; font-weight: bold; color: #FF4D4D;">
                <p>المعدل العام الإجمالي الحاصل عليه : {final_score} / 20</p>
                <p>النتيجة والقرار النهائي للجنة الإدارية : <span style="color: {result_color}; text-decoration: none;">{result}</span></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
