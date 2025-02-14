import os
import time
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.find import router as find_router
from routes.open_webui_find import router as open_webui_find_router

# Determine the API mode before FastAPI initialization
WEBUI_API_KEY = os.getenv("WEBUI_API_KEY")
WEBUI_URL = os.getenv("WEBUI_URL")
API_MODE = "Gemini"  # Default to Gemini, will change if Open WebUI is available


def is_open_webui_available(max_retries=10, initial_wait=2):
    """Check if Open WebUI is running and accessible, with authentication and retries."""
    if not WEBUI_API_KEY or not WEBUI_URL:
        print("WEBUI_API_KEY or WEBUI_URL is not set.")
        return False  # WebUI is not configured

    url = f"{WEBUI_URL}/api/models"
    headers = {"Authorization": f"Bearer {WEBUI_API_KEY}"}

    wait_time = initial_wait

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                print(f"Open WebUI is available on attempt {attempt}.")
                return True  # WebUI is reachable and responding

            print(f"Attempt {attempt}: WebUI responded with {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print(f"Attempt {attempt}: Failed to reach Open WebUI: {e}")

        if attempt < max_retries:
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 5  # Exponential backoff (2, 10, 50, ...)

    print("Open WebUI is unreachable after maximum retries.")
    return False


# Set API mode and assign tags dynamically
if is_open_webui_available():
    API_MODE = "Open-WebUI"
    tags_metadata = [{"name": "Open WebUI Mode", "description": "API is running using Open WebUI for dataset matching"}]
    print("Using Open WebUI for dataset matching.")
else:
    API_MODE = "Gemini"
    tags_metadata = [{"name": "Google Gemini Mode", "description": "API is running using Google Gemini for dataset matching"}]
    print("Using Gemini for dataset matching.")

# Initialize FastAPI with dynamic tags
app = FastAPI(
    title="Dataset Finder API",
    description="An API for finding datasets based on research papers.",
    version="1.0",
    openapi_tags=tags_metadata
)

# Middleware to add the X-API-Version header globally
@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-API-Version"] = API_MODE
    return response

# Conditionally include the appropriate router
if API_MODE == "Open-WebUI":
    app.include_router(open_webui_find_router, tags=["Open WebUI Mode"])
else:
    app.include_router(find_router, tags=["Google Gemini Mode"])
