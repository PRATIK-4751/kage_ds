import requests
import time
import streamlit as st

def call_glm_api(prompt, api_key, retry=0, max_retries=3, timeout=60):
    if not api_key:
        return "API Key is missing. Please check your .env file."
    
    if retry > max_retries:
        return "Maximum retries exceeded. Please try again later."
    
    try:
        r = requests.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": "glm-4", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1024},
            timeout=timeout
        )
        
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        elif r.status_code == 401:
            return "Invalid API Key. Please check your API key in the .env file."
        elif r.status_code == 429:  # Rate limit
            wait_time = min(2 ** retry, 60)  # Exponential backoff with max 60 seconds
            time.sleep(wait_time)
            return call_glm_api(prompt, api_key, retry + 1, max_retries, timeout)
        elif r.status_code == 504 or r.status_code == 502:  # Gateway timeout
            if retry < max_retries:
                time.sleep(2)
                return call_glm_api(prompt, api_key, retry + 1, max_retries, timeout)
            else:
                return f"API Gateway Error: {r.status_code}. Please try again later."
        else:
            return f"API Error: Status code {r.status_code}. Response: {r.text[:200]}"
    except requests.exceptions.Timeout:
        if retry < max_retries:
            # Increase timeout for next retry
            new_timeout = timeout * 1.5
            time.sleep(1)
            return call_glm_api(prompt, api_key, retry + 1, max_retries, new_timeout)
        return "Request timed out. The server might be busy. Please try again later."
    except requests.exceptions.ConnectionError:
        if retry < max_retries:
            time.sleep(2)
            return call_glm_api(prompt, api_key, retry + 1, max_retries, timeout)
        return "Connection error. Please check your internet connection."
    except Exception as e:
        return f"Error: {str(e)}"

def get_mock_response(prompt):
    """Provide a mock response when API is unavailable"""
    if "analyze" in prompt.lower():
        return "This is a mock analysis. The actual API is currently unavailable."
    elif "code" in prompt.lower():
        return "```python\ndef example_function():\n    print('This is mock code. The API is unavailable.')\n```"
    else:
        return "The API is currently unavailable. This is a mock response."

@st.cache_data(ttl=600)
def cached_glm_call(prompt, api_key):
    # Check if we're in offline mode
    if 'offline_mode' in st.session_state and st.session_state.offline_mode:
        return get_mock_response(prompt)
    
    try:
        response = call_glm_api(prompt, api_key)
        if (response.startswith("API Error") or 
            response.startswith("Invalid API Key") or 
            response.startswith("Error:") or 
            response.startswith("Request timed out") or
            response.startswith("Connection error")):
            
            # Set offline mode if we detect persistent API issues
            st.session_state.offline_mode = True
            st.warning("⚠️ API connection issues detected. Switched to offline mode.")
            return get_mock_response(prompt)
        return response
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.session_state.offline_mode = True
        return get_mock_response(prompt)