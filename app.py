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

# 복사 기능 + 알림 메시지용 JS & CSS
st.markdown("""
<style>
.copy-box {
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 10px;
    position: relative;
}
.copy-button {
    position: absolute;
    right: 10px;
    top: 10px;
    background-color: #f0f0f0;
    border: 1px solid #aaa;
    padding: 3px 8px;
    border-radius: 4px;
    cursor: pointer;
}
.toast {
    visibility: hidden;
    min-width: 200px;
    background-color: #323232;
    color: #fff;
    text-align: center;
    border-radius: 5px;
    padding: 8px;
    position: fixed;
    z-index: 1;
    right: 30px;
    bottom: 30px;
    font-size: 16px;
}
.toast.show {
    visibility: visible;
    animation: fadein 0.5s, fadeout 0.5s 1.5s;
}
@keyframes fadein {
    from {bottom: 10px; opacity: 0;}
    to {bottom: 30px; opacity: 1;}
}
@keyframes fadeout {
    from {bottom: 30px; opacity: 1;}
    to {bottom: 10px; opacity: 0;}
}
</style>

<div id="toast" class="toast">✅ 성취기준이 복사되었습니다.</div>

<script>
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        var toast = document.getElementById("toast");
        toast.className = "toast show";
        setTimeout(function(){ toast.className = toast.className.replace("show", ""); }, 2000);
    });
}
</script>
""", unsafe_allow_html=True)

# 항목 출력
for i, row in filtered_df.iterrows():
    code = row["성취기준 코드"]
    content = row["성취기준"]
    full_text = f"{code} {content}".replace("'", "\\'")
    
    st.markdown(f"""
        <div class="copy-box">
            <strong>{code}</strong>: {content}
            <button class="copy-button" onclick="copyToClipboard('{full_text}')">📋 복사</button>
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
