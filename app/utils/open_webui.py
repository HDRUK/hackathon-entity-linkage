import requests 
import re
import os
# 🔹 Replace with your actual API key
WEBUI_API_KEY=os.environ.get("WEBUI_API_KEY")
WEBUI_URL=os.environ.get("WEBUI_URL")

def can_you_find_a_dataset_webui(description, model):

    url = f"{WEBUI_URL}/api/chat/completions"
    contents=f"Can you find a name of any dataset(s) in the following description from a paper abstract, give me a comma separated list of names of possible dataset names, if you dont think there is one, give me no response - not a single word:\n\n {description}"
    headers = {
        "Authorization": f"Bearer {WEBUI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": contents}]
    }

    response = requests.post(url, headers=headers, json=payload, stream=True)

    is_google_genai = "google_genai" in model.lower()
    full_content = []

    try:
        if is_google_genai:
            response_text = ""
            for line in response.iter_lines():
                if not line.strip():
                    continue  # Ignore empty lines
                
                line = line.decode("utf-8")  # Convert from bytes to string
                response_text += line + " "  # Append to full text

            # Extract all content values manually using regex
            matches = re.findall(r'"content":\s?"(.*?)"', response_text)
            full_content = [match.strip() for match in matches if match.strip()]

            # Join extracted content into a single string
            content = "".join(full_content).replace("\\n", "")
            content = [x.lstrip().rstrip() for x in content.split(",")]
        else:
            content = [x.lstrip().rstrip() for x in response.text.split(",")]

        return content if content else []

    except requests.exceptions.RequestException as e:
        return []   
    

# 🔹 List available models to check correct name
def list_models_webui():
    url = f"{WEBUI_URL}/api/models"  # Correct API path for model listing
    headers = {"Authorization": f"Bearer {WEBUI_API_KEY}"}
    response = requests.get(url, headers=headers)
    
    try:
        available_models = response.json()
        #print("Available Models:", models)

        model_names = [model["id"] for model in available_models["data"] if "name" in model]

        return model_names
    except requests.exceptions.RequestException as e:
        return f"Error fetching models: {e}"
