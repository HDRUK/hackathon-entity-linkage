import os
import time
import requests
from fastapi import FastAPI
from routes.find import router as find_router
from routes.open_webui_find import router as open_webui_find_router

app = FastAPI()

# Retrieve Open WebUI configuration
WEBUI_API_KEY = os.getenv("WEBUI_API_KEY")
WEBUI_URL = os.getenv("WEBUI_URL")


def is_open_webui_available(max_retries=10, initial_wait=2):
    """Check if Open WebUI is running and accessible, with authentication and retries."""
    if not WEBUI_API_KEY or not WEBUI_URL:
        print("❌ WEBUI_API_KEY or WEBUI_URL is not set.")
        return False  # WebUI is not configured

    url = f"{WEBUI_URL}/api/models"
    headers = {"Authorization": f"Bearer {WEBUI_API_KEY}"}

    wait_time = initial_wait

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                print(f"✅ Open WebUI is available on attempt {attempt}.")
                return True  # WebUI is reachable and responding

            print(f"⚠️ Attempt {attempt}: WebUI responded with {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print(f"⚠️ Attempt {attempt}: Failed to reach Open WebUI: {e}")

        if attempt < max_retries:
            print(f"⏳ Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 5  # Exponential backoff (2, 4, 8, ...)

    print("❌ Open WebUI is unreachable after maximum retries.")
    return False

# Conditionally include the appropriate router
if is_open_webui_available():
    app.include_router(open_webui_find_router)
    print("✅ Using Open WebUI for dataset matching.")
else:
    app.include_router(find_router)
    print("⚡ Using Gemini for dataset matching.")
