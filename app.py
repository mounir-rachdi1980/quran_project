import streamlit as st
import pandas as pd
from datetime import date

# (هنا يجب أن تضع باقي تعريفات الكود الخاصة بك مثل w أو session_state)
# تأكد أن w معرفة مسبقاً في كودك الأصلي قبل الوصول لهذا الجزء

# --- استخراج بطاقة الأعداد ---
elif choice == "استخراج بطاقة الأعداد":
    today_miladi = date.today().strftime("%d / %m / %Y")
    
    st.markdown('<p class="custom-heading">🖨️ استخراج وطباعة كشف الأعداد السنوي</p>', unsafe_allow_html=True)
    
    if st.session_state.students_db.empty:
        st.warning("⚠️ لا توجد بيانات طلاب متوفرة.")
    else:
        student_id = st.selectbox("اختر معرف الطالب:", st.session_state.students_db['المعرف'])
        s_info = st.session_state.students_db[st.session_state.students_db['المعرف'] == student_id].iloc[0]
        g_info = st.session_state.grades_db[st.session_state.grades_db['المعرف'] == student_id].iloc[0]
        
        # حساب المعدل
        final_score = round(((g_info['الحفظ']*w['الحفظ']) + (g_info['الرواية']*w['الرواية']) + (g_info['الدراية']*w['الدراية']) + (g_info['الحضور']*w['الحضور'])) / sum(w.values()), 2)
        
        st.markdown(f"""
        <div style="direction: rtl; text-align: right; margin: 0 auto; max-width: 800px; padding: 20px;">
            <table style="width: 100%; border: none;">
                <tr>
                    <td style="text-align: right; vertical-align: top;">
                        <b>الجمهورية التونسية</b><br>الرابطة الوطنية للقرآن الكريم بالمكناسي
                    </td>
                    <td style="text-align: center;">
                        <img src="https://raw.githubusercontent.com/mounir-rachdi1980/quran_project/main/logo.jpg" style="width: 100px;">
                        <div style="border: 2px solid red; color: red; font-size: 20px; font-weight: bold; padding: 5px; margin-top: 10px; display: inline-block;">بطاقة النتائج السنوية</div>
                    </td>
                    <td style="text-align: left; vertical-align: top;">
                        <b>الحمد لله</b><br>المكناسي في: {today_miladi}<br>التاريخ الهجري: [التاريخ]<br><b>السنة الدراسية: 2025-2026</b>
                    </td>
                </tr>
            </table>
            <hr style="border: 1px solid #ccc; margin: 20px 0;">
            <table style="width: 100%;">
                <tr>
                    <td style="text-align: right; width: 50%;">
                        <p><b>الاسم:</b> {s_info['الاسم الثلاثي']}</p>
                        <p><b>اللقب:</b> {s_info['اللقب']}</p>
                        <p><b>الوحدة:</b> {s_info['الوحدة الحالية']}</p>
                    </td>
                    <td style="text-align: left; width: 50%;">
                        <p><b>رقم الترسيم:</b> {s_info['المعرف']}</p>
                        <p><b>المرحلة:</b> {s_info['المرحلة الحالية']}</p>
                    </td>
                </tr>
            </table>
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px; text-align: center;">
                <tr style="background-color: #f2f2f2;">
                    <th style="border: 1px solid #ddd; padding: 8px;">المادة</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">العدد</th>
                </tr>
                <tr><td style="border: 1px solid #ddd; padding: 8px;">الحفظ</td><td style="border: 1px solid #ddd; padding: 8px;">{g_info['الحفظ']}</td></tr>
                <tr><td style="border: 1px solid #ddd; padding: 8px;">الرواية</td><td style="border: 1px solid #ddd; padding: 8px;">{g_info['الرواية']}</td></tr>
                <tr><td style="border: 1px solid #ddd; padding: 8px;">الدراية</td><td style="border: 1px solid #ddd; padding: 8px;">{g_info['الدراية']}</td></tr>
                <tr><td style="border: 1px solid #ddd; padding: 8px;">الحضور</td><td style="border: 1px solid #ddd; padding: 8px;">{g_info['الحضور']}</td></tr>
            </table>
            <div style="margin-top: 20px; text-align: center; font-size: 20px; font-weight: bold;">المعدل العام: {final_score} / 20</div>
        </div>
        """, unsafe_allow_html=True)
