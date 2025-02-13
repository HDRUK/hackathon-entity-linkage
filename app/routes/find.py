from fastapi import APIRouter
from pydantic import BaseModel
from utils.paper_finder import PaperFinder
from utils.gemini import can_you_find_a_dataset, can_you_find_a_tool
from utils.matcher import find_best_matches, find_elastic_matches


router = APIRouter(prefix="/find")


class Request(BaseModel):
    doi: str


@router.post("/")
def datasets(data: Request):
    retval = None
    try:
        finder = PaperFinder(data.doi)
        datasets = can_you_find_a_dataset(finder.methods)
        matches = find_elastic_matches(datasets)
        # tools = can_you_find_a_tool(finder.title, finder.code)
        retval = {
            "doi": data.doi,
            "datasets": matches,
        }
    # , "tools": tools}
    except ValueError:
        pass

    return {"data": retval}
