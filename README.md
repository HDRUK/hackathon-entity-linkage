# HDRUK-ELIXIR Hackathon: Gateway Entity Linkages

Welcome to the HDRUK-ELIXIR hackathon project for HDRUK Gateway entity linkages.

## Overview

This project aims to explore different methods for creating **indirect linkages** between various **gateway entities** such as:
- Datasets
- Publications
- Tools
- External data sources

The service can be run using **Google Gemini** or **Open Web UI**, depending on the available environment variables. The backend **automatically detects** the environment and selects the appropriate mode.

## Running the Services

### Frontend

```
cd fe
npx remix vite:build
npx remix-serve build/server/index.js
```

### Backend

The service can be run in **two modes**:
1. **Google Gemini** (default)
2. **Open Web UI** (if configured)

The backend will check for `WEBUI_API_KEY` and `WEBUI_URL` to determine whether Open Web UI is available. If not, it will default to using Google Gemini.

#### **Running with Default Google Gemini Mode**

This is the simplest way to run the service, requiring only the FastAPI application.

```sh
cd app
docker-compose up --build fastapi-app
```

you will need authenication keys for the following additional services:
- **Elasticsearch** (for dataset and tool matching)
- **Google Gemini** (for dataset and tool discovery)

#### Running with Open Web UI Compatibility

If you want to run the service using **Open Web UI**, you will need additional services, including:
- **Open Web UI** (LLM-based text searching)
- **Ollama** (LLM backend for Open Web UI)
- **Elasticsearch** (for dataset and tool matching)
- **Google Gemini** LLM-based text searching) ••• recomended as a fallback
  

#### **Full Stack with Open Web UI**
To run the full stack with Open Web UI compatibility, use the provided **`docker-compose.yml`** configuration:

```sh
cd app
docker-compose up --build
```
N.b. The FastAPI backend will check for `WEBUI_API_KEY` and `WEBUI_URL`, and ping the Open web UI interface before deciding whether to use Open Web UI instead of Google Gemini.
When the stack is installed for the first time, a WEBUI_API_KEY will need to be generated from within the open web UI interface that should be running on. http://0.0.0.0/3000

## Available API Endpoints

The FastAPI backend provides several endpoints for interacting with the dataset linkage system.

### **Dataset Matching**
#### `POST /find/`
Finds datasets related to a given paper DOI.

**Example Request:**
```json
{
    "doi": "10.1038/s41541-024-00898-w",
    "model": "Gemma2:latest"
}
```
**Response:**
```json
{
    "data": [
        {
            "paper": {
                "doi": "https://doi.org/10.1038/s41541-024-00898-w",
                "title": "Sample Paper Title"
            },
            "dataset": {...},
            "score": 0.85
        }
    ]
}
```

#### `POST /find/OpenAire` - Only avalible in open web UI mode
Queries OpenAIRE for dataset matches.

### **Retrieving Linkages**
#### `GET /find/linkages`
Fetches all stored linkages.

#### `DELETE /find/linkages`
Removes all stored linkages.

### **Text-Based Matching**
#### `GET /find/via-abstracts`
Uses TF-IDF similarity matching between paper and dataset abstracts.

### **Model Information** 
#### `GET /find/models` - Only avalible in open web UI mode
Lists available models for Open Web UI.

### **General API Status**
#### `GET /status`
Returns the active API mode.
```json
{"active_mode": "Open-WebUI"}
```
or
```json
{"active_mode": "Gemini"}
```

---
## Additional resources

We have provide a number of Demo jupyter notebook (ipynb) scripts to show how the component services run.  ([HMTL render](https://hdruk.github.io/hackathon-entity-linkage/demo)) 

Example data we started with can be found [here](https://github.com/HDRUK/hackathon-entity-linkage/tree/main/data)


<div style="border: 2px solid black;">
<p align="center">
  <img src="https://github.com/user-attachments/assets/cef39f2a-97f6-49f7-99c5-73f6a81313a4" width="30%" />
  <img src="https://github.com/user-attachments/assets/d6d3f221-8813-4f0f-b86c-01dfc09968f6" width="30%" />
  <img src="https://github.com/user-attachments/assets/0e715d76-62f1-478c-8016-f3289c8a7adf" width="30%" />
</p>
</div>


