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

The backend will check for `WEBUI_API_KEY` and `WEBUI_URL` to determine whether Open Web UI is available. If these are not set, the service will default to using Google Gemini.

## Running with Default Google Gemini Mode

In this mode, you need to provide authentication keys for the following services:

- **Elasticsearch** (for dataset and tool matching)
- **Google Gemini** (for dataset and tool discovery)

These environment variables can be passed to Docker Compose in several ways:

### **1. Using a `.env` file** (recommended)

Create a `.env` file in the root of the project and define the necessary variables:

```ini
# .env file
ELASTICSEARCH_URL=http://elasticsearch:9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=yourpassword
GEMINI_API_KEY=your-gemini-key
```
This is the simplest way to run the service, requiring only the FastAPI application.

```sh
docker-compose --env-file .env up --build fastapi-app
```

### **2. Passing Environment Variables Directly in the Command**

If you prefer, you can pass the required variables inline when running `docker-compose`:

```sh
ELASTICSEARCH_URL=http://elasticsearch:9200 \
ELASTICSEARCH_USER=elastic \
ELASTICSEARCH_PASSWORD=yourpassword \
GEMINI_API_KEY=your-gemini-key \
docker-compose up --build fastapi-app
```


## Running with Open Web UI Compatibility

To run the service using **Open Web UI**, you need additional services:

- **Open Web UI** (LLM-based text searching)
- **Ollama** (LLM backend for Open Web UI)
- **Elasticsearch** (for dataset and tool matching)
- **Google Gemini** (recommended as a fallback for text searching)

### **Configuring Environment Variables for Open Web UI Mode**

To enable Open Web UI, in addition to teh above, you must also set `WEBUI_API_KEY` and `WEBUI_URL`
For example if running using a .env these vars would be:

```ini
# .env file
WEBUI_API_KEY=your-openwebui-api-key
WEBUI_URL=http://openwebui:3000
ELASTICSEARCH_URL=http://elasticsearch:9200
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=yourpassword
GEMINI_API_KEY=your-gemini-key
```

### **Starting the Services**

Run the following command to start all necessary containers:

```sh
docker-compose --env-file .env up --build
```

This setup ensures that:

- If `WEBUI_API_KEY` and `WEBUI_URL` are set, Open Web UI will be used.
- If these variables are missing, the service will default to Google Gemini.

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


