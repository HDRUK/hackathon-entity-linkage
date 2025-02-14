from fastapi import APIRouter
from utils.open_webui import list_models_webui

router = APIRouter(prefix="/open_webui_list")

@router.get("/models")
def get_models():
    try:
        models = list_models_webui()
        return {"models": models}
    except Exception as e:
        return {"error": str(e)}