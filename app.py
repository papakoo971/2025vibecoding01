import streamlit as st
import pandas as pd

# CSV 파일 로드
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/papakoo971/2025vibecoding01/main/2022_curri_elementray.csv"
    return pd.read_csv(url, encoding='utf-8-sig')

df = load_data()
df.columns = df.columns.str.strip().str.replace(r"\s+", "", regex=True)  # 열 정리

# 🔍 필터 설정
selected_grade = st.sidebar.selectbox("학년군 선택", sorted(df["학년군"].dropna().unique()))

available_subjects = df[df["학년군"] == selected_grade]["과목"].dropna().unique()
selected_subject = st.sidebar.selectbox("과목 선택", sorted(available_subjects))

available_areas = df[
    (df["학년군"] == selected_grade) &
    (df["과목"] == selected_subject)
]["내용영역단원"].dropna().unique()  # 공백 제거된 열 이름 기준
selected_area = st.sidebar.selectbox("내용영역(단원) 선택", sorted(available_areas))

# ✅ 최종 필터링된 성취기준 목록
filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목"] == selected_subject) &
    (df["내용영역단원"] == selected_area)
].reset_index(drop=True)

# 📚 제목
st.title("📚 2022 개정교육과정 성취기준 조회")

# 💬 선택된 필터 정보 출력
st.markdown(
    f"""
    <div style='padding: 10px 0; font-size:16px;'>
    🎓 <b>{selected_grade}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    📘 <b>{selected_subject}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    📂 <b>{selected_area}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    🔍 <b>{len(filtered_df)}개 성취기준</b> 조회됨
    </div>
    """,
    unsafe_allow_html=True
)

# ✅ 성취기준 코드 + 내용 출력
for _, row in filtered_df.iterrows():
    full_text = f"{row['성취기준코드']} {row['성취기준']}"
    st.code(full_text, language='text')

# ✅ CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
