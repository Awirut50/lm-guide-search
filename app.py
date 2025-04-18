import streamlit as st
import pandas as pd

st.set_page_config(page_title="LM Guide Search", layout="wide")
st.title("🔍 ค้นหาขนาด LM Guide (THK)")

uploaded_file = st.file_uploader("📤 อัปโหลดไฟล์ Excel ที่มีข้อมูล LM Guide", type=["xlsx", "xls"])

if uploaded_file:
    try:
        # โหลดข้อมูลจากไฟล์ Excel
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # แสดง preview คอลัมน์
        st.subheader("📑 Preview ข้อมูลที่อัปโหลด")
        st.dataframe(df.head(), use_container_width=True)

        # ช่องค้นหาทั้ง 4 ช่อง
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            model_query = st.text_input("Model")
        with col2:
            m_query = st.text_input("M")
        with col3:
            b_query = st.text_input("B")
        with col4:
            c_query = st.text_input("C")

        # กรองข้อมูลตาม input
        filtered_df = df.copy()
        if model_query:
            filtered_df = filtered_df[filtered_df['Model'].astype(str).str.contains(model_query, case=False, na=False)]
        if m_query:
            filtered_df = filtered_df[filtered_df['M'].astype(str).str.contains(m_query, case=False, na=False)]
        if b_query:
            filtered_df = filtered_df[filtered_df['B'].astype(str).str.contains(b_query, case=False, na=False)]
        if c_query:
            filtered_df = filtered_df[filtered_df['C'].astype(str).str.contains(c_query, case=False, na=False)]

        # แสดงผลลัพธ์
        st.markdown(f"### 📋 ผลลัพธ์ ({len(filtered_df)} รายการ)")
        st.dataframe(filtered_df, use_container_width=True)

        # ปุ่มดาวน์โหลด
        if not filtered_df.empty:
            csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("⬇️ ดาวน์โหลดผลลัพธ์เป็น CSV", data=csv, file_name="lm_guide_search_result.csv", mime='text/csv')

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
else:
    st.info("กรุณาอัปโหลดไฟล์ Excel ก่อนเริ่มค้นหา")
