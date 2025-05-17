import streamlit as st
import pandas as pd

# CSV 파일 로드
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/papakoo971/2025vibecoding01/main/korean_curriculum_standards.csv"
    return pd.read_csv(url, encoding='utf-8-sig')

df = load_data()

# 🔍 사이드바 필터 설정
st.sidebar.title("🔍 필터 설정")
selected_grade = st.sidebar.selectbox("학년군 선택", sorted(df["학년군"].unique()))
selected_subject = st.sidebar.selectbox("과목 선택", sorted(df["과목"].unique()))
selected_area = st.sidebar.selectbox(
    "내용영역 선택",
    sorted(df[df["과목"] == selected_subject]["내용영역(단원)"].unique())
)

# 🔎 필터링된 데이터프레임
filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목"] == selected_subject) &
    (df["내용영역(단원)"] == selected_area)
].reset_index(drop=True)

# 📚 제목
st.title("📚 2022 개정교육과정 성취기준 조회")

# 🧾 선택된 필터 정보 상단에 한 줄로 표시
st.markdown(
    f"""
    <div style='padding: 10px 0; font-size:16px;'>
    🎓 <b>{selected_grade}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    📘 <b>{selected_subject}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    📂 <b>{selected_area}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    🔍 <b>{len(filtered_df)}개 성취기준</b> 조회됨
    </div>
    """, unsafe_allow_html=True
)

# 🧾 성취기준 코드 + 내용 출력 (코드 컨테이너로 복사 가능)
for _, row in filtered_df.iterrows():
    full_text = f"{row['성취기준 코드']} {row['성취기준']}"
    st.code(full_text, language='text')

# 📥 CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
