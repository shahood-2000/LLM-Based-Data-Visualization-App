# main.py
import streamlit as st
import pandas as pd
from mistral_engine import query_llm
from chart_generator import generate_chart
from utils import load_file

st.set_page_config(page_title="Conversational Data Visualization", layout="wide", page_icon="📊")

# --- Custom Theme Styling ---
custom_css = """
    <style>
    .main {
        background-color: #f0f8ff;
    }
    header, footer, .css-18e3th9 {
        background-color: #002b36;
        color: white;
    }
    .stButton button {
        background-color: #ff7f50;
        color: white;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.5em 2em;
    }
    .stTextArea textarea {
        background-color: #fefbd8;
    }
    .stMarkdown h2, .stMarkdown h3 {
        color: #007acc;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("🧠 Conversational Data Visualization")
st.markdown("""
Welcome to your **LLM-powered, no-code dashboard**! 🎯

- Upload your own dataset (CSV or Excel)
- Ask a question in plain English
- Instantly visualize your data with beautiful interactive charts powered by AI
""")

# Sidebar: Upload Data
st.sidebar.header("📂 Upload Your Dataset")
st.sidebar.markdown("Supports `.csv` and `.xlsx` files")
file = st.sidebar.file_uploader("Choose a file", type=["csv", "xlsx"])

# Load Data
if file is not None:
    df = load_file(file)
    st.success("✅ File uploaded successfully!")
    st.markdown("### 🔍 Data Preview")
    st.dataframe(df.head(), use_container_width=True)
else:
    df = None

# Prompt Input
st.markdown("---")
st.subheader("💬 Enter a Prompt to Visualize Your Data")
prompt = st.text_area("Try something like: 'Show a pie chart of sales by region'", height=120)

if st.button("🚀 Generate Visualization") and prompt and df is not None:
    with st.spinner("🤖 Mistral 7B is thinking..."):
        chart_instructions, chart_summary = query_llm(prompt, df)

    # Always call generate_chart with a fallback-safe check
    fig = generate_chart(df, chart_instructions)
    st.markdown("### 📈 Visualization")
    st.plotly_chart(fig, use_container_width=True)

    if chart_summary:
        st.markdown("### 🧠 Insight from AI")
        st.success(chart_summary)

elif prompt and df is None:
    st.warning("⚠️ Please upload a dataset first.")
elif not prompt and file is not None:
    st.info("ℹ️ Please enter a prompt to generate a chart.")
