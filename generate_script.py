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
            {"role": "system", "content": "Generate a reddit story about, 1. childhood neglect 2. Child favoritism 3. Infidelity 4. Narcissist people 5. Narcissist partners. 6. Narcissist parents (Choose randomly) In 450 words exactly You can't use complicated language. You are forbidden from using the 6 literary devices. You also can't use any poetic lines.Only give me title and story. And don't say "title" before writing the title. Just give plain text. Add as much personal details as possible like name, sex, age ect. Write as if you are recalling from memory leave some details as you "don't remember. Don't be generic and avoid all common tropes."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data)

    result = response.json()
    return result["choices"][0]["message"]["content"]
