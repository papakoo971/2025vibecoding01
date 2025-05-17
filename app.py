import streamlit as st
import pandas as pd

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

# 타이틀
st.title("📚 2022 개정교육과정 성취기준 조회사이트")

filtered_df = df[
    (df["학년군"] == selected_grade) &
    (df["과목명"] == selected_subject) &
    (df["과목의 내용영역"] == selected_area)
].reset_index(drop=True)

st.markdown(f"#### 🔎 조회 결과: {len(filtered_df)}개 성취기준")

# 스타일 및 JavaScript 복사 기능
st.markdown("""
<style>
.custom-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
.custom-table th, .custom-table td {
    border: 1px solid #ddd;
    padding: 6px 10px;
    text-align: left;
    vertical-align: middle;
}
.custom-table th {
    background-color: #f2f2f2;
}
.copy-button {
    padding: 4px 8px;
    font-size: 13px;
    border: 1px solid #aaa;
    border-radius: 5px;
    cursor: pointer;
    background-color: #eee;
}
.toast {
    visibility: hidden;
    min-width: 180px;
    background-color: #323232;
    color: #fff;
    text-align: center;
    border-radius: 4px;
    padding: 6px;
    position: fixed;
    z-index: 9999;
    right: 30px;
    bottom: 30px;
    font-size: 14px;
}
.toast.show {
    visibility: visible;
    animation: fadein 0.4s, fadeout 0.4s 1.4s;
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
        setTimeout(function(){ toast.className = toast.className.replace("show", ""); }, 1800);
    });
}
</script>
""", unsafe_allow_html=True)

# 테이블 출력 (주의: 맨 앞 줄에 공백 없음!)
table_html = "<table class='custom-table'>"
table_html += "<thead><tr><th>학년군</th><th>과목</th><th>내용영역</th><th>성취기준 코드</th><th>성취기준</th><th>복사</th></tr></thead><tbody>"

for _, row in filtered_df.iterrows():
    full_text = f"{row['성취기준 코드']} {row['성취기준']}".replace("'", "\\'")
    table_html += f"<tr><td>{row['학년군']}</td><td>{row['과목명']}</td><td>{row['과목의 내용영역']}</td><td>{row['성취기준 코드']}</td><td>{row['성취기준']}</td><td><button class='copy-button' onclick=\"copyToClipboard('{full_text}')\">📋 복사</button></td></tr>"

table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)

# CSV 다운로드
csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 조회 결과 CSV 다운로드",
    data=csv,
    file_name=f"{selected_subject}_{selected_area}_성취기준.csv",
    mime="text/csv"
)
