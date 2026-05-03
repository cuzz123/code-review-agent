import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Code Review", layout="wide")
st.title("🔍 AI Code Review Agent")

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📝 粘贴代码")
    code = st.text_area("代码", height=400, placeholder="粘贴你的代码...")

    if st.button("开始审查", type="primary"):
        if code.strip():
            with st.spinner("正在审查...（4 个维度：架构/安全/性能/风格）"):
                r = requests.post(f"{API_URL}/review", json={
                    "code": code,
                    "language": "source.py",
                })
                if r.ok:
                    st.session_state.report = r.json()
                    st.success("审查完成！")
                else:
                    st.error(f"审查失败: {r.text}")
        else:
            st.warning("请先粘贴代码")

with col2:
    st.subheader("📊 审查报告")
    report = st.session_state.get("report")
    if report:
        st.metric("评分", f"{report['score']}/100")
        st.metric("发现问题", len(report["issues"]))

        with st.expander("摘要", expanded=True):
            st.write(report["summary"])

        with st.expander("优点"):
            for s in report["strengths"]:
                st.write(f"✅ {s}")

        with st.expander("改进建议"):
            for s in report["suggestions"]:
                st.write(f"💡 {s}")

        if report["issues"]:
            st.subheader("问题详情")
            for issue in report["issues"]:
                sev = {"critical": "🔴", "major": "🟡", "minor": "🔵", "info": "⚪"}
                with st.expander(f"{sev.get(issue['severity'], '⚪')} [{issue['severity'].upper()}] {issue['title']}"):
                    st.write(f"分类： {issue['category']}")
                    st.write(f"描述： {issue['description']}")
                    st.write(f"建议： {issue['suggestion']}")

    else:
        st.info("粘贴代码并点击「开始审查」")