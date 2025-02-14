from fastapi import FastAPI
from routes.find import router as find_router
from routes.open_webui_find import router as open_webapi_find_router
from routes.open_webui_list import router as open_webapi_list_router


app = FastAPI()

app.include_router(find_router)
app.include_router(open_webapi_find_router)
app.include_router(open_webapi_list_router)
