import requests

def test_key(key):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {"Authorization": f"Bearer {key}"}
    data = {
        "model": "glm-4",
        "messages": [{"role": "user", "content": "Hello"}]
    }
    
    try:
        print("Testing API key...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print("Success! Key is working.")
            return True
        else:
            print(f"Error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    key = input("Enter your API key: ")
    test_key(key)