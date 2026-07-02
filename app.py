import streamlit as st
import pandas as pd

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="نظام الفرع المحلي للرابطة الوطنية للقرآن الكريم بالمكناسي", layout="wide", page_icon="🕌")

# 2. إضافة التنسيقات البصرية المطلوبة
st.markdown("""
    <style>
    /* تفعيل اتجاه لغة الضاد وضبط مسافة علوية مريحة للعين */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stSidebar"], .main .block-container, div[data-testid="stForm"], .stDataFrame {
        direction: rtl !important;
        text-align: right !important;
    }
    
    .stMarkdown, p, label {
        text-align: right !important;
    }
    
    /* توسيط الاستمارة والتبويبات */
    div[data-testid="stForm"], div[data-testid="stTab"] {
        direction: rtl !important;
    }
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
    
    /* 🔴 اسم الفرع الرئيسي */
    .main-title { 
        color: #FF4D4D !important; 
        text-align: center !important;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        font-size: 32px !important;
        text-decoration: underline !important;
    } 
    
    /* 🟢 عناوين الاستمارات والقوائم الموحدة */
    .custom-heading { 
        color: #2ECC71 !important; 
        text-align: center !important;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        font-size: 24px !important; 
        text-decoration: underline !important; 
        margin-top: 15px;
        margin-bottom: 15px;
    }
    
    h2, h3, h4 {
        font-size: 24px !important;
        text-align: right !important;
    }
    
    /* 🎨 تنسيقات مخصصة وعريضة لعناوين المراحل التعليمية */
    .stage-title-1 {
        color: #3498DB !important; /* أزرق فخم */
        font-size: 26px !important;
        font-weight: bold !important;
        text-decoration: underline !important;
        margin-top: 10px;
    }
    .stage-title-2 {
        color: #E67E22 !important; /* برتقالي دافئ */
        font-size: 26px !important;
        font-weight: bold !important;
        text-decoration: underline !important;
        margin-top: 10px;
    }
    .stage-title-3 {
        color: #9B5DE5 !important; /* بنفسجي ملكي */
        font-size: 26px !important;
        font-weight: bold !important;
        text-decoration: underline !important;
        margin-top: 10px;
    }
    
    /* تجميل شكل التبويبات لعرض المراحل التعليمية */
    button[data-testid="stMarkdownContainer"] p {
        font-size: 18px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الترويسة والشعار المتناسق
st.markdown("""
    <div style="text-align: center; width: 100%;">
        <img src="https://raw.githubusercontent.com/mounir-rachdi1980/quran_project/main/logo.jpg" 
             style="display: block; width: 100%; max-width: 420px; height: auto; object-fit: contain; margin: 25px auto 15px auto; padding: 0; filter: brightness(1.25);">
        <h1 class="main-title" style="margin-top: 15px; margin-bottom: 20px;">نظام الفرع المحلي للرابطة الوطنية للقرآن الكريم بالمكناسي</h1>
    </div>
""", unsafe_allow_html=True)


# --- محاكاة قاعدة البيانات وجلسة العمل وتحديث الأعمدة للمراحل والوحدات ---
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(columns=[
        'المعرف', 'الاسم الثلاثي', 'اللقب', 'تاريخ الولادة', 'بطاقة التعريف', 'المهنة', 'المرحلة الحالية', 'الوحدة الحالية'
    ])
if 'grades_db' not in st.session_state:
    st.session_state.grades_db = pd.DataFrame(columns=['المعرف', 'الحفظ', 'الرواية', 'الدراية', 'الحضور'])
if 'weights' not in st.session_state:
    st.session_state.weights = {'الحفظ': 3.0, 'الرواية': 2.0, 'الدراية': 2.0, 'الحضور': 1.0}

w = st.session_state.weights

# تعريف الهيكل التعليمي المتكامل للمنظومة
stages_structure = {
    "المرحلة الأولى: رواية الإمام قالون": ["الوحدة الأولى", "الوحدة الثانية", "الوحدة الثالثة", "الوحدة الرابعة"],
    "المرحلة الثانية: قراءة نافع وحفص عن عاصم": ["الوحدة الأولى", "الوحدة الثانية", "الوحدة الثالثة"],
    "المرحلة الثالثة: القراءات": ["الوحدة الأولى (وحدة سما)", "الوحدة الثانية (الأربعة المتممة)", "الوحدة الثالثة (الثلاثة المتممة)", "الوحدة الرابعة (العشر الكبرى)"]
}

menu = ["تسجيل طالب جديد وتوزيعه", "إدارة وحذف الطلاب", "رصد وتعديل الدرجات", "إعدادات الضوارب (المعاملات)", "استخراج بطاقة الأعداد"]
choice = st.sidebar.selectbox("قائمة التحكم والتنقل :", menu)

# --- تسجيل طالب جديد وإدارة التبويبات والمراحل ---
if choice == "تسجيل طالب جديد وتوزيعه":
    st.markdown('<p class="custom-heading">📝 استمارة بطاقة إرشادات وتسجيل طالب جديد</p>', unsafe_allow_html=True)
    
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("الاسم الثلاثي :")
            dob = st.date_input("تاريخ الولادة :")
            job = st.text_input("المهنة / المستوى الدراسي :")
            chosen_stage = st.selectbox("تسكين في المرحلة التعليمية :", list(stages_structure.keys()))
        with col2:
            last_name = st.text_input("اللقب (اسم العائلة) :")
            cin = st.text_input("رقم بطاقة التعريف الوطنية / رقم القيد :")
            st.write("") # موازنة بصريّة
            chosen_unit = st.selectbox("تسكين في الوحدة البدائية :", stages_structure[chosen_stage])
            
        submitted = st.form_submit_button("حفظ بيانات الطالب وتوليد المعرف")
        
        if submitted:
            if name and last_name and cin:
                next_id = 20260001 + len(st.session_state.students_db)
                new_student = pd.DataFrame([{
                    'المعرف': next_id, 'الاسم الثلاثي': name, 'اللقب': last_name, 
                    'تاريخ الولادة': str(dob), 'بطاقة التعريف': cin, 'المهنة': job,
                    'المرحلة الحالية': chosen_stage, 'الوحدة الحالية': chosen_unit
                }])
                st.session_state.students_db = pd.concat([st.session_state.students_db, new_student], ignore_index=True)
                
                new_grade = pd.DataFrame([{'المعرف': next_id, 'الحفظ': 0.0, 'الرواية': 0.0, 'الدراية': 0.0, 'الحضور': 0.0}])
                st.session_state.grades_db = pd.concat([st.session_state.grades_db, new_grade], ignore_index=True)
                
                st.success(f"🎉 تم تسجيل الطالب بنجاح وتسكينه في {chosen_unit}! المعرف الرقمي: {next_id}")
                st.rerun()
            else:
                st.error("⚠️ يرجى ملء الخانات الأساسية المطلوبة.")

    # 🏢 التبويب الجمالي لعرض وتوزيع الطلبة حسب المراحل والوحدات التعليمية
    st.markdown('<p class="custom-heading">🏢 التوزيع الهيكلي للطلاب حسب المراحل والوحدات التعليمية</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(list(stages_structure.keys()))
    
    # محتويات تبويب المرحلة الأولى
    with tab1:
        st.markdown('<p class="stage-title-1">📜 المرحلة الأولى: رواية الإمام قالون</p>', unsafe_allow_html=True)
        st.info("تشمل هذه المرحلة ركيزة الرواية وبها 4 وحدات دراسية للارتقاء.")
        for unit in stages_structure["المرحلة الأولى: رواية الإمام قالون"]:
            filtered_df = st.session_state.students_db[
                (st.session_state.students_db['المرحلة الحالية'] == "المرحلة الأولى: رواية الإمام قالون") & 
                (st.session_state.students_db['الوحدة الحالية'] == unit)
            ]
            st.markdown(f"🔹 **{unit}** (عدد الطلاب الحركيين حالياً: {len(filtered_df)})")
            if not filtered_df.empty:
                st.dataframe(filtered_df[['المعرف', 'الاسم الثلاثي', 'اللقب', 'المهنة', 'بطاقة التعريف']], use_container_width=True)
                # إضافة خيار حذف سريع وتجريبي للطلاب في التبويب مباشرة
                with st.expander(f"🗑️ خيارات حذف سريعة لـ {unit}"):
                    del_id = st.selectbox("اختر معرف الطالب لحذفه فوراً:", filtered_df['المعرف'], key=f"del_{unit}")
                    if st.button("تأكيد الحذف السريع للطالب", key=f"btn_del_{unit}", type="primary"):
                        st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['المعرف'] != del_id].reset_index(drop=True)
                        st.session_state.grades_db = st.session_state.grades_db[st.session_state.grades_db['المعرف'] != del_id].reset_index(drop=True)
                        st.success("🗑️ تم الحذف بنجاح!")
                        st.rerun()
            else:
                st.caption("لا يوجد طلاب مسجلون في هذه الوحدة حالياً.")
                
    # محتويات تبويب المرحلة الثانية
    with tab2:
        st.markdown('<p class="stage-title-2">📖 المرحلة الثانية: قراءة نافع وحفص عن عاصم</p>', unsafe_allow_html=True)
        st.info("تشمل قراءة الإمام نافع برافديه (قالون وورش) إضافةً إلى رواية حفص وبها 3 وحدات.")
        for unit in stages_structure["المرحلة الثانية: قراءة نافع وحفص عن عاصم"]:
            filtered_df = st.session_state.students_db[
                (st.session_state.students_db['المرحلة الحالية'] == "المرحلة الثانية: قراءة نافع وحفص عن عاصم") & 
                (st.session_state.students_db['الوحدة الحالية'] == unit)
            ]
            st.markdown(f"🔹 **{unit}** (عدد الطلاب الحركيين حالياً: {len(filtered_df)})")
            if not filtered_df.empty:
                st.dataframe(filtered_df[['المعرف', 'الاسم الثلاثي', 'اللقب', 'المهنة', 'بطاقة التعريف']], use_container_width=True)
                with st.expander(f"🗑️ خيارات حذف سريعة لـ {unit}"):
                    del_id = st.selectbox("اختر معرف الطالب لحذفه فوراً:", filtered_df['المعرف'], key=f"del_{unit}")
                    if st.button("تأكيد الحذف السريع للطالب", key=f"btn_del_{unit}", type="primary"):
                        st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['المعرف'] != del_id].reset_index(drop=True)
                        st.session_state.grades_db = st.session_state.grades_db[st.session_state.grades_db['المعرف'] != del_id].reset_index(drop=True)
                        st.success("🗑️ تم الحذف بنجاح!")
                        st.rerun()
            else:
                st.caption("لا يوجد طلاب مسجلون في هذه الوحدة حالياً.")

    # محتويات تبويب المرحلة الثالثة
    with tab3:
        st.markdown('<p class="stage-title-3">🕌 المرحلة الثالثة: علم القراءات المتقدمة</p>', unsafe_allow_html=True)
        st.info("مرحلة علم القراءات المتقدمة والأسانيد وبها 4 وحدات كبرى.")
        for unit in stages_structure["المرحلة الثالثة: القراءات"]:
            filtered_df = st.session_state.students_db[
                (st.session_state.students_db['المرحلة الحالية'] == "المرحلة الثالثة: القراءات") & 
                (st.session_state.students_db['الوحدة الحالية'] == unit)
            ]
            st.markdown(f"🔹 **{unit}** (عدد الطلاب الحركيين حالياً: {len(filtered_df)})")
            if not filtered_df.empty:
                st.dataframe(filtered_df[['المعرف', 'الاسم الثلاثي', 'اللقب', 'المهنة', 'بطاقة التعريف']], use_container_width=True)
                with st.expander(f"🗑️ خيارات حذف سريعة لـ {unit}"):
                    del_id = st.selectbox("اختر معرف الطالب لحذفه فوراً:", filtered_df['المعرف'], key=f"del_{unit}")
                    if st.button("تأكيد الحذف السريع للطالب", key=f"btn_del_{unit}", type="primary"):
                        st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['المعرف'] != del_id].reset_index(drop=True)
                        st.session_state.grades_db = st.session_state.grades_db[st.session_state.grades_db['المعرف'] != del_id].reset_index(drop=True)
                        st.success("🗑️ تم الحذف بنجاح!")
                        st.rerun()
            else:
                st.caption("لا يوجد طلاب مسجلون في هذه الوحدة حالياً.")

# --- قسم إدارة وحذف الطلاب الرئيسي ---
elif choice == "إدارة وحذف الطلاب":
    st.markdown('<p class="custom-heading">⚙️ لوحة التحكم في مسار الطلاب وإجراء الحذف</p>', unsafe_allow_html=True)
    if st.session_state.students_db.empty:
        st.warning("⚠️ لا توجد بيانات طلاب مسجلة حالياً لتعديلها أو حذفها.")
    else:
        student_id = st.selectbox("اختر معرف الطالب المراد إدارته:", st.session_state.students_db['المعرف'])
        s_idx = st.session_state.students_db[st.session_state.students_db['المعرف'] == student_id].index[0]
        s_info = st.session_state.students_db.loc[s_idx]
        
        st.write("---")
        st.markdown(f"### 👤 الطالب الحالي: {s_info['الاسم الثلاثي']} {s_info['اللقب']}")
        
        col1, col2 = st.columns(2)
        with col1:
            mod_stage = st.selectbox("تعديل المرحلة الحالية:", list(stages_structure.keys()), index=list(stages_structure.keys()).index(s_info['المرحلة الحالية']))
        with col2:
            available_units = stages_structure[mod_stage]
            default_unit_idx = available_units.index(s_info['الوحدة الحالية']) if s_info['الوحدة الحالية'] in available_units else 0
            mod_unit = st.selectbox("تعديل الوحدة الحالية:", available_units, index=default_unit_idx)
            
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("💾 حفظ التعديلات على المرحلة والوحدة", use_container_width=True):
                st.session_state.students_db.at[s_idx, 'المرحلة الحالية'] = mod_stage
                st.session_state.students_db.at[s_idx, 'الوحدة الحالية'] = mod_unit
                st.success("✅ تم تحديث مسار الطالب بنجاح!")
                st.rerun()
                
        with col_btn2:
            if st.button("❌ حذف هذا الطالب نهائياً من النظام", use_container_width=True, type="primary"):
                st.session_state.students_db = st.session_state.students_db.drop(s_idx).reset_index(drop=True)
                st.session_state.grades_db = st.session_state.grades_db[st.session_state.grades_db['المعرف'] != student_id].reset_index(drop=True)
                st.success("🗑️ تم حذف الطالب وكافة سجلاته بنجاح!")
                st.rerun()

# --- رصد الأعداد والدرجات ---
elif choice == "رصد وتعديل الدرجات":
    st.markdown('<p class="custom-heading">📊 دفتر رصد أعداد وتقييمات الطلاب</p>', unsafe_allow_html=True)
    if st.session_state.students_db.empty:
        st.warning("⚠️ لا يوجد طلاب مسجلون حالياً في النظام لرصد أعدادهم.")
    else:
        merged_df = pd.merge(st.session_state.students_db, st.session_state.grades_db, on='المعرف')
        student_id = st.selectbox("اختر معرف الطالب المراد رصد درجاته :", merged_df['المعرف'])
        
        current_student = merged_df[merged_df['المعرف'] == student_id].iloc[0]
        st.markdown(f"<h4>📝 رصد ودرجات الطالب: {current_student['الاسم الثلاثي']} {current_student['اللقب']} | الحيز: {current_student['المرحلة الحالية']} - {current_student['الوحدة الحالية']}</h4>", unsafe_allow_html=True)
        
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
        
        if final_score >= 10.0:
            result = "ناجح ومرتقى للوحدة الموالية بموجب تفوقه 🎓"
            result_color = "#27AE60"
        else:
            result = "راسب وله فرصة تدارك في نفس الوحدة الحالية 📑"
            result_color = "#8B0000"
            
        st.markdown(f"""
        <div style="border: 3px double #FF4D4D; padding: 25px; border-radius: 10px; background-color: #FAFAFA; direction: rtl; font-family: 'Cairo', sans-serif; text-align: right; margin: 0 auto; max-width: 900px;">
            <div style="text-align: center;">
                <h2 style="margin: 0; color: #FF4D4D; text-decoration: underline;">بطاقة تقييم وكشف أعداد طالب سنوي</h2>
                <h4 style="color: gray; margin-top: 5px; text-decoration: none;">الفرع المحلي للرابطة الوطنية للقرآن الكريم بالمكناسي</h4>
                <hr style="border-top: 2px solid #FF4D4D; margin: 15px 0;">
            </div>
            <table style="width: 100%; font-size: 18px; margin-bottom: 20px; text-align: right; direction: rtl; border: none; color: #333;">
                <tr><td style="padding: 5px; border:none;"><b>المعرف الخاص :</b> {s_info['المعرف']}</td><td style="padding: 5px; border:none;"><b>الاسم الكامل :</b> {s_info['الاسم الثلاثي']} {s_info['اللقب']}</td></tr>
                <tr><td style="padding: 5px; border:none;"><b>المرحلة الدراسية :</b> {s_info['المرحلة الحالية']}</td><td style="padding: 5px; border:none;"><b>الوحدة التقييمية :</b> {s_info['الوحدة الحالية']}</td></tr>
                <tr><td style="padding: 5px; border:none;"><b>بطاقة التعريف الوطنية :</b> {s_info['بطاقة التعريف']}</td><td style="padding: 5px; border:none;"><b>المهنة / الصفة :</b> {s_info['المهنة']}</td></tr>
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
