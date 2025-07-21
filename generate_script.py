import requests
import os

def generate_script(prompt):
    api_key = os.environ["DEEPSEEK_API_KEY"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Generate a 200-word story for a YouTube short."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)

    result = response.json()
    return result["choices"][0]["message"]["content"]
