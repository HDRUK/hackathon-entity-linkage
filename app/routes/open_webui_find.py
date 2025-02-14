from fastapi import APIRouter
from pydantic import BaseModel
from utils.paper_finder import PaperFinder
from utils.open_webui import can_you_find_a_dataset_webui
from utils.matcher import find_best_matches
from utils.openaire_matcher import query_openaire

router = APIRouter(prefix="/open_webui_find")

class Request(BaseModel):
    doi: str = "10.1038/s41541-024-00898-w"  # Default DOI
    model: str = "Gemma2:latest"  # Default Model


@router.post("/")
def datasets(data: Request):
    retval = None
    try:
        finder = PaperFinder(data.doi)
        datasets = can_you_find_a_dataset_webui(finder.methods,data.model)
        gateway_matches = find_best_matches(datasets)
        openaire_matches = query_openaire(datasets)
        # tools = can_you_find_a_tool(finder.title, finder.code)
        retval = {
            "doi": data.doi,
            "gateway_datasets": gateway_matches,
            "openaire_datasets": openaire_matches,
        }
    # , "tools": tools}
    except ValueError:
        pass

    return {"Results": retval}
