import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GLM_API_KEY")
if not API_KEY:
    st.markdown("<h3 style='color:#f44336;text-align:center'>🔐 API Key Missing</h3>", unsafe_allow_html=True)
    st.stop()

st.set_page_config(page_title="⚡ KAGE", page_icon="⚡", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background: #000; color: #00ff88; }
    .title { font-size: 40px; font-weight: 700; text-align: center; color: #00ff88; margin: 10px 0; text-shadow: 0 0 15px rgba(0, 255, 136, 0.6); letter-spacing: 1px; }
    .subtitle { text-align: center; color: #aaa; font-size: 16px; margin-bottom: 30px; }
    .section { margin: 25px 0; padding: 20px; border-radius: 16px; background: #0a0a0a; box-shadow: 0 4px 20px rgba(0, 255, 136, 0.1); border: 1px solid #00ff8820; }
    .icon { font-size: 50px; text-align: center; margin: 15px 0; filter: drop-shadow(0 0 10px rgba(0, 255, 136, 0.4)); }
    .btn { background: #00ff88 !important; color: #000 !important; font-weight: 600; border-radius: 8px !important; }
    .result-box { background: #001208; border: 1px solid #00ff8830; border-radius: 12px; padding: 16px; color: #00ff88; font-size: 15px; line-height: 1.7; }
    .code-output { background: #001208; border: 1px solid #00ff8830; border-radius: 12px; padding: 16px; color: #00ff88; font-family: 'Courier New', monospace; white-space: pre-wrap; }
    .ask-section { margin-top: 25px; padding-top: 20px; border-top: 1px solid #00ff8820; }
    input, textarea, select { color: #00ff88 !important; }
    .stTextInput > div > div > input { background: #0a0a0a !important; border: 1px solid #00ff8840 !important; }
    .stTextArea > div > div > textarea { background: #0a0a0a !important; border: 1px solid #00ff8840 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>⚡ KAGE</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>暗のAI • Data & Code Intelligence</p>", unsafe_allow_html=True)

def glm(prompt):
    try:
        r = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": "glm-4", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1024}
        )
        return r.json()["choices"][0]["message"]["content"] if r.status_code == 200 else "❌ Failed"
    except Exception:
        return "❌ Connection error"

tab1, tab2 = st.tabs(["📊 ANALYZE", "💻 CODE"])

# ────────────── ANALYZE TAB ──────────────
with tab1:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='icon'>🌀</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["csv", "xlsx"], label_visibility="collapsed")
    
    if uploaded:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        st.dataframe(df.head(10), use_container_width=True)
        
        if st.checkbox("📊 Show Statistics"):
            st.write(df.describe().style.set_properties(**{"background-color": "#0a0a0a", "color": "#00ff88"}))

        num_cols = df.select_dtypes(include="number").columns
        if len(num_cols) > 0:
            x_col = st.selectbox("🟢 X-Axis", num_cols)
            y_col = st.selectbox("🔵 Y-Axis (Optional)", ["(None)"] + list(num_cols))

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.set_facecolor("#000")
            fig.patch.set_facecolor("#000")
            ax.tick_params(colors="#00ff88")
            for spine in ax.spines.values():
                spine.set_color("#00ff8830")

            if y_col != "(None)":
                ax.scatter(df[x_col], df[y_col], color="#00ff88", alpha=0.7)
                ax.set_title(f"{x_col} vs {y_col}", color="#00ff88", fontsize=12)
            else:
                ax.hist(df[x_col], bins=20, color="#00ff88", alpha=0.7)
                ax.set_title(f"Distribution of {x_col}", color="#00ff88", fontsize=12)
            ax.set_xlabel(x_col, color="#aaa")
            ax.set_ylabel(y_col if y_col != "(None)" else "Frequency", color="#aaa")
            st.pyplot(fig)

            if st.button("🔍 AI Insight", key="analyze_btn"):
                with st.spinner("🧠 Processing..."):
                    prompt = f"Analyze the pattern in column '{x_col}'" + (f" vs '{y_col}'" if y_col != "(None)" else "")
                    prompt += ". Explain trends, anomalies, and implications. Be concise and technical."
                    response = glm(prompt)
                    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                    st.markdown(response)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # ────────────── ASK ANYTHING SECTION ──────────────
            st.markdown("<div class='ask-section'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#00ff88;margin-bottom:15px'>❓ Ask Anything</h3>", unsafe_allow_html=True)
            
            question = st.text_input(
                "", 
                placeholder="What's the average sales in Q3?", 
                label_visibility="collapsed"
            )
            
            if st.button("🔍 Get Answer", key="ask_btn"):
                if question.strip():
                    with st.spinner("💡 Thinking..."):
                        data_context = f"Dataset has {len(df)} rows and {len(df.columns)} columns."
                        data_context += f"\nNumeric columns: {', '.join(num_cols)}"
                        if len(num_cols) > 0:
                            data_context += f"\nSample stats: {x_col} mean={df[x_col].mean():.2f}"
                        
                        full_prompt = f"{data_context}\n\nQuestion: {question}\n\nProvide a clear, concise answer with reasoning."
                        answer = glm(full_prompt)
                        
                        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                        st.markdown(f"**Q:** {question}")
                        st.markdown(f"**A:** {answer}")
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='result-box' style='color:#ff5555'>⚠️ Please ask a question</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box'>No numeric columns found.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ────────────── CODER TAB ──────────────
with tab2:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='icon'>🤖</div>", unsafe_allow_html=True)
    task = st.text_area("", placeholder="Write a Python function to detect outliers using Z-score...", height=120)
    lang = st.selectbox("Language", ["Python", "SQL", "JavaScript", "R", "C++", "Shell"])

    if st.button("⚡ Generate", key="code_btn"):
        if task.strip():
            with st.spinner("⚡ Synthesizing code..."):
                prompt = f"Write a clean {lang} code snippet for: {task}. "
                prompt += "Include minimal comments. Return ONLY code and one-line explanation - no extra text."
                result = glm(prompt)
                
                # Clean the response to remove any extra text
                if "```" in result:
                    result = result.split("```")[1].split("\n", 1)[1].rsplit("```", 1)[0]
                
                st.markdown("### 💾 Generated Code", unsafe_allow_html=True)
                st.markdown(f'<div class="code-output">{result}</div>', unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-box' style='color:#ff5555'>⚠️ Enter a coding task.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)