import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/papakoo971/2025vibecoding01/main/korean_curriculum_standards.csv"
    return pd.read_csv(url, encoding='utf-8-sig')

df = load_data()

# 필터 설정
st.sidebar.title("🔍 필터 설정")
selected_grade = st.sidebar.selectbox("학년군 선택", sorted(df["학년군"].unique()))
selected_subject = st.sidebar.selectbox("과목 선택", sorted(df["과목명"].unique()))
selected_area = st.sidebar.selectbox("내용영역 선택", sorted(df[df["과목명"] == selected_subject]["과목의 내용영역"].unique()))

st.title("📚 2022 개정교육과정 성취기준 조회사이트")

filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목명"] == selected_subject) &
    (df["과목의 내용영역"] == selected_area)
].reset_index(drop=True)

st.markdown(f"#### 🔎 조회 결과: {len(filtered_df)}개 성취기준")

# 성취기준 카드식 출력 + 복사 유도
for i, row in filtered_df.iterrows():
    code = row["성취기준 코드"]
    content = row["성취기준"]
    full_text = f"{code} {content}"
    
    with st.container():
        st.markdown(f"**{code}**: {content}")
        with st.expander("📋 복사하려면 클릭"):
            st.code(full_text, language='text')

# CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
