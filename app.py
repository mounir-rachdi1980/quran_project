import streamlit as st
import pandas as pd

# باقي الكود الخاص بك يليهما...
st.set_page_config(page_title="نظام إدارة الجمعية القرآنية", layout="wide")import streamlit as str
from streamlit_gsheets import GSheetsConnection

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    st.success("تم الاتصال بنجاح!")
except Exception as e:
    st.error("فشل الاتصال بقاعدة البيانات.")
    st.exception(e) # هذا سيظهر لك تفاصيل الخطأ الدقيقة لتجده في الـ Logs
