import streamlit as st
import os
from app import main

# For Streamlit Cloud deployment
if __name__ == "__main__":
    # Set default API key for demo purposes if not provided
    if "GLM_API_KEY" not in os.environ:
        st.session_state.offline_mode = True
    
    # Run the main app
    main()