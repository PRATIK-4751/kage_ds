import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from utils import load_data, create_visualization, get_data_context
from api import cached_glm_call
from ui import (
    apply_styling, display_header, display_result, 
    display_code, display_error, section_start, 
    section_end, display_icon, ask_section_start
)

def main():
    load_dotenv()
    API_KEY = os.getenv("GLM_API_KEY")
    
    # Set a flag for offline mode
    if 'offline_mode' not in st.session_state:
        st.session_state.offline_mode = False
    
    # Check for API key but don't stop execution
    if not API_KEY:
        st.warning("⚠️ API Key Missing - Running in offline mode with mock responses")
        st.session_state.offline_mode = True
    
    st.set_page_config(
        page_title="Data Insights AI",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Main app logic
    apply_styling()
    display_header()
    
    if 'api_calls' not in st.session_state:
        st.session_state.api_calls = 0
    if 'last_code_task' not in st.session_state:
        st.session_state.last_code_task = None
    if 'last_code_result' not in st.session_state:
        st.session_state.last_code_result = None
    
    tab1, tab2 = st.tabs(["ANALYZE", "CODE"])
    
    with tab1:
        section_start()
        display_icon("🌀")
        uploaded = st.file_uploader("", type=["csv", "xlsx"], label_visibility="collapsed")
        
        if uploaded:
            df = load_data(uploaded)
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.checkbox("Show Statistics"):
                st.write(df.describe().style.set_properties(**{"background-color": "#1F2937", "color": "#F9FAFB"}))

            num_cols = df.select_dtypes(include="number").columns
            if len(num_cols) > 0:
                x_col = st.selectbox("X-Axis", num_cols)
                y_col = st.selectbox("Y-Axis (Optional)", ["(None)"] + list(num_cols))

                fig = create_visualization(df, x_col, y_col)
                st.pyplot(fig)

                if st.button("AI Insight", key="analyze_btn"):
                    with st.spinner("Processing..."):
                        prompt = f"Analyze the pattern in column '{x_col}'" + (f" vs '{y_col}'" if y_col != "(None)" else "")
                        prompt += ". Explain trends, anomalies, and implications. Be concise and technical."
                        response = cached_glm_call(prompt, API_KEY)
                        display_result(None, response)

                ask_section_start()
                
                question = st.text_input(
                    "Enter your question", 
                    placeholder="What's the average sales in Q3?", 
                    label_visibility="collapsed",
                    key="question_input"
                )
                
                if st.button("Get Answer", key="ask_btn"):
                    if question.strip():
                        with st.spinner("Thinking..."):
                            data_context = get_data_context(df, num_cols, x_col)
                            full_prompt = f"{data_context}\n\nQuestion: {question}\n\nProvide a clear, concise answer with reasoning."
                            answer = cached_glm_call(full_prompt, API_KEY)
                            display_result(f"**Q:** {question}", f"**A:** {answer}")
                    else:
                        display_error("Please ask a question")
            else:
                display_error("No numeric columns found.")
        section_end()

    with tab2:
        section_start()
        display_icon("🤖")
        
        example_tasks = {
            "Python": "Write a function to detect outliers using Z-score method",
            "SQL": "Create a query to find top 5 customers by purchase amount",
            "JavaScript": "Write a function to debounce API calls",
            "R": "Create a function to perform ANOVA and visualize results",
            "C++": "Implement a simple thread-safe queue",
            "Shell": "Write a script to find and delete files older than 30 days"
        }
        
        lang = st.selectbox("Language", list(example_tasks.keys()))
        task = st.text_area("", placeholder=example_tasks[lang], height=120)

        if st.button("Generate", key="code_btn"):
            if task.strip():
                with st.spinner("Synthesizing code..."):
                    prompt = f"Write a clean {lang} code snippet for: {task}. "
                    prompt += "Include minimal comments. Return ONLY code and one-line explanation - no extra text."
                    
                    if st.session_state.last_code_task != task:
                        result = cached_glm_call(prompt, API_KEY)
                        st.session_state.last_code_task = task
                        st.session_state.last_code_result = result
                    else:
                        result = st.session_state.last_code_result
                    
                    if "```" in result:
                        result = result.split("```")[1].split("\n", 1)[1].rsplit("```", 1)[0]
                    
                    display_code(result)
            else:
                display_error("Enter a coding task.")
        section_end()

if __name__ == "__main__":
    main()
    