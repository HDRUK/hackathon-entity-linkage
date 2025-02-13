import requests

# 🔹 Replace with your actual API key
API_KEY = "sk-fc3beab1e18e4190bcf1b4a996733a5a"
WEBUI_URL = "http://localhost:3000/api/chat/completions"

def can_you_find_a_dataset_webui(description, model):

    prompt = (
        "The text below is from a research publication. Can you extract the names of any datasets mentioned? "
        "Return a **comma-separated list** of dataset names. If none are found, return 'none'.\n\n"
        + description
    )


    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(WEBUI_URL, headers=headers, json=payload)
    
    # Try to parse JSON response safely
    try:
        json_response = response.json()
        content = json_response["choices"][0]["message"]["content"].strip()

        # 🔹 Only process if it's a comma-separated list
        if "," in content:
            return [x.strip() for x in content.split(",")]

        return []  # Return empty list if no valid datasets found

    except (requests.exceptions.JSONDecodeError, KeyError, IndexError):
        return []  # Return empty list if response is invalid