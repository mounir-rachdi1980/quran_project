import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# إعدادات الواجهة
st.set_page_config(page_title="نظام إدارة الجمعية القرآنية", layout="wide")

# محاولة الاتصال بقاعدة البيانات
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    st.success("تم الاتصال بنجاح!")
except Exception as e:
    st.error("فشل الاتصال بقاعدة البيانات.")
    st.exception(e)
