from fastapi import APIRouter
from pydantic import BaseModel
from utils.paper_finder import PaperFinder
from utils.open_webui import can_you_find_a_dataset_webui, can_you_find_a_tool_webui
from utils.matcher import find_best_matches


router = APIRouter(prefix="/open_webui_find")

class Request(BaseModel):
    doi: str
    model: str


@router.post("/")
def datasets(data: Request):
    retval = None
    try:
        finder = PaperFinder(data.doi)
        datasets = can_you_find_a_dataset_webui(finder.methods,data.model)
        matches = find_best_matches(datasets)
        # tools = can_you_find_a_tool(finder.title, finder.code)
        retval = {
            "doi": data.doi,
            "datasets": matches,
        }
    # , "tools": tools}
    except ValueError:
        pass

    return {"data": retval}
