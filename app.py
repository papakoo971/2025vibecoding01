import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/papakoo971/2025vibecoding01/main/korean_curriculum_standards.csv"
    return pd.read_csv(url, encoding='utf-8-sig')

df = load_data()

# 필터
st.sidebar.title("🔍 필터 설정")
selected_grade = st.sidebar.selectbox("학년군 선택", sorted(df["학년군"].unique()))
selected_subject = st.sidebar.selectbox("과목 선택", sorted(df["과목명"].unique()))
selected_area = st.sidebar.selectbox("내용영역 선택", sorted(df[df["과목명"] == selected_subject]["과목의 내용영역"].unique()))

# 제목
st.title("📚 2022 개정교육과정 성취기준 조회사이트")

# 필터링
filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목명"] == selected_subject) &
    (df["과목의 내용영역"] == selected_area)
].reset_index(drop=True)

st.markdown(f"#### 🔎 조회 결과: {len(filtered_df)}개 성취기준")

# 표 출력
for idx, row in filtered_df.iterrows():
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1.2, 3, 1])
    
    with col1:
        st.markdown(row["학년군"])
    with col2:
        st.markdown(row["과목명"])
    with col3:
        st.markdown(row["과목의 내용영역"])
    with col4:
        st.code(row["성취기준 코드"], language='text')
    with col5:
        st.code(row["성취기준"], language='text')
    with col6:
        copy_text = f"{row['성취기준 코드']} {row['성취기준']}"
        if st.button(f"📋 복사", key=f"copy_{idx}"):
            st.session_state["copied_text"] = copy_text
            st.success("✅ 복사되었습니다!", icon="📌")

# CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
