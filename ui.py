import streamlit as st

def apply_styling():
    st.markdown(
        """
        <style>
        .stApp { background: #111827; color: #F9FAFB; }
        .title { font-size: 40px; font-weight: 700; text-align: center; color: #3B82F6; margin: 10px 0; text-shadow: 0 0 15px rgba(59, 130, 246, 0.6); letter-spacing: 1px; }
        .subtitle { text-align: center; color: #aaa; font-size: 16px; margin-bottom: 30px; }
        .section { margin: 25px 0; padding: 20px; border-radius: 16px; background: #1F2937; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); border: 1px solid #374151; }
        .icon { font-size: 50px; text-align: center; margin: 15px 0; filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.4)); }
        .btn { background: #3B82F6 !important; color: #fff !important; font-weight: 600; border-radius: 8px !important; }
        .result-box { background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 16px; color: #F9FAFB; font-size: 15px; line-height: 1.7; }
        .code-output { background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 16px; color: #F9FAFB; font-family: 'Roboto Mono', monospace; white-space: pre-wrap; }
        .ask-section { margin-top: 25px; padding-top: 20px; border-top: 1px solid #374151; }
        input, textarea, select { color: #F9FAFB !important; }
        .stTextInput > div > div > input { background: #1F2937 !important; border: 1px solid #374151 !important; }
        .stTextArea > div > div > textarea { background: #1F2937 !important; border: 1px solid #374151 !important; }
        .stSpinner > div > div { border-top-color: #3B82F6 !important; }
        .stButton > button { background-color: #3B82F6 !important; color: #fff !important; font-weight: 500; border-radius: 6px !important; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); }
        .stButton > button:hover { background-color: #2563EB !important; transform: translateY(-1px); box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23); }
        .stDataFrame { border-radius: 10px; overflow: hidden; }
        .stProgress > div > div > div { background-color: #3B82F6 !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 8px; }
        .stTabs [data-baseweb="tab"] { background-color: #1F2937; border-radius: 8px 8px 0 0; border: 1px solid #374151; border-bottom: none; padding: 10px 16px; }
        .stTabs [aria-selected="true"] { background-color: #111827 !important; border-color: #3B82F6 !important; }
        /* Modern scrollbar */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #1F2937; }
        ::-webkit-scrollbar-thumb { background: #4B5563; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #60A5FA; }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_header():
    st.markdown("<h1 class='title'>⚡ KAGE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>暗のAI • Data & Code Intelligence</p>", unsafe_allow_html=True)

def display_result(title, content):
    if title:
        st.markdown(f"**{title}**")
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("</div>", unsafe_allow_html=True)

def display_code(code):
    st.markdown("### 💾 Generated Code", unsafe_allow_html=True)
    st.markdown(f'<div class="code-output">{code}</div>', unsafe_allow_html=True)

def display_error(message):
    st.markdown(f"<div class='result-box' style='color:#ff5555'>⚠️ {message}</div>", unsafe_allow_html=True)

def section_start():
    st.markdown("<div class='section'>", unsafe_allow_html=True)

def section_end():
    st.markdown("</div>", unsafe_allow_html=True)

def display_icon(icon):
    st.markdown(f"<div class='icon'>{icon}</div>", unsafe_allow_html=True)

def ask_section_start():
    st.markdown("<div class='ask-section'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#00ff88;margin-bottom:15px'>❓ Ask Anything</h3>", unsafe_allow_html=True)