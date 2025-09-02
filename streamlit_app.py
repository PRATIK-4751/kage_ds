import streamlit as st
import os
from app import main

# For Streamlit Cloud deployment
if __name__ == "__main__":
    # Set offline mode for Streamlit Cloud if no API key
    if "GLM_API_KEY" not in os.environ:
        os.environ["GLM_API_KEY"] = ""  # Empty string triggers offline mode
    
    # Run the main app
    main()