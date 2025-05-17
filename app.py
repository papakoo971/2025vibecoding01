import streamlit as st
import pandas as pd

# CSV 불러오기
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/papakoo971/2025vibecoding01/main/korean_curriculum_standards.csv"
    return pd.read_csv(url, encoding='utf-8-sig')

df = load_data()

# 사이드바 필터
st.sidebar.title("🔍 필터 설정")
selected_grade = st.sidebar.selectbox("학년군 선택", sorted(df["학년군"].unique()))
selected_subject = st.sidebar.selectbox("과목 선택", sorted(df["과목명"].unique()))
selected_area = st.sidebar.selectbox("내용영역 선택", sorted(df[df["과목명"] == selected_subject]["과목의 내용영역"].unique()))

# 제목
st.title("📚 2022 개정교육과정 성취기준 조회사이트")

# 필터링된 결과
filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목명"] == selected_subject) &
    (df["과목의 내용영역"] == selected_area)
].reset_index(drop=True)

st.markdown(f"#### 🔎 조회 결과: {len(filtered_df)}개 성취기준")

# 복사 버튼 포함 출력
for i, row in filtered_df.iterrows():
    code = row["성취기준 코드"]
    content = row["성취기준"]
    copy_text = f"{code} {content}"
    st.markdown(f"""
        <div style="border:1px solid #ccc; padding:10px; border-radius:6px; margin-bottom:5px;">
            <strong>{code}</strong>: {content}
            <button onclick="navigator.clipboard.writeText('{copy_text}')" style="float:right; margin-left:10px;">📋 복사</button>
        </div>
    """, unsafe_allow_html=True)

# CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
