import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")

# CSV 파일 로드
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/papakoo971/2025vibecoding01/main/2022_curri_elementray.csv"
    df = pd.read_csv(url, encoding='utf-8-sig')
    df.columns = df.columns.str.replace(r"\s+", "", regex=True)  # 열 이름 정리
    return df

df = load_data()

# 🔍 사이드바 필터 설정
selected_grade = st.sidebar.selectbox("학년군 선택", sorted(df["학년군"].dropna().unique()))

# 학년군에 종속된 과목 필터링
available_subjects = df[df["학년군"] == selected_grade]["과목"].dropna().unique()
selected_subject = st.sidebar.selectbox("과목 선택", sorted(available_subjects))

# 과목에 종속된 내용영역 필터링
available_areas = df[
    (df["학년군"] == selected_grade) &
    (df["과목"] == selected_subject)
]["내용영역(단원)"].dropna().unique()
selected_area = st.sidebar.selectbox("내용영역(단원) 선택", sorted(available_areas))

# 🔎 최종 필터링된 DataFrame
filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목"] == selected_subject) &
    (df["내용영역(단원)"] == selected_area)
].reset_index(drop=True)

# 📚 제목
st.title("📚 2022 개정교육과정 성취기준 조회")

# 💬 필터 정보 요약
st.markdown(
    f"""
    <div style='padding: 10px 0; font-size:16px;'>
    🎓 <b>학년군: {selected_grade}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    📘 <b>과목: {selected_subject}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    📂 <b>내용영역(단원): {selected_area}</b> &nbsp;&nbsp; | &nbsp;&nbsp;
    🔍 <b>{len(filtered_df)}개 성취기준</b>
    </div>
    """,
    unsafe_allow_html=True)

# 🧾 성취기준 코드 + 내용 출력
for _, row in filtered_df.iterrows():
    full_text = f"{row['성취기준코드']} {row['성취기준']}"
    st.code(full_text, language='text')


# 📥 CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
