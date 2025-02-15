from fastapi import APIRouter
from pydantic import BaseModel
from utils.paper_finder import PaperFinder
from utils.gemini import can_you_find_a_dataset, can_you_find_a_tool
from utils.matcher import find_best_matches, find_elastic_matches

from db.database import database
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize


router = APIRouter(prefix="/find")


class Request(BaseModel):
    doi: str


@router.post("/")
def datasets(data: Request):
    retval = []
    try:
        finder = PaperFinder(data.doi)
        datasets = can_you_find_a_dataset(finder.methods)
        all_matches = find_elastic_matches(datasets)
        for key, matches in all_matches.items():
            if not matches:
                continue
            for match in matches:
                if not match:
                    continue
                score = match.pop("score") / 18.0
                value = {
                    "paper": {
                        "doi": f"https://doi.org/{data.doi}",
                        "title": finder.title,
                    },
                    "dataset": match,
                    "score": score,
                }
                retval.append(value)
                database.save_linkages(value)
    except ValueError:
        pass

    return {"data": retval}


@router.get("/linkages")
def get_linkages():
    data = database.get_linkages()
    return {"data": data}


@router.delete("/linkages")
def delete_linkages():
    data = database.delete_linkages()
    return {"data": data}


@router.get("/via-abstracts")
def via_abstracts():
    paper_abstracts = [x["abstract"] for x in database.publications]
    dataset_abstracts = [
        x["metadata"]["summary"]["description"] for x in database.datasets
    ]

    tokenized_paper_abstracts = [
        " ".join(word_tokenize(abstract.lower())) if abstract else " "
        for abstract in paper_abstracts
    ]
    tokenized_dataset_abstracts = [
        " ".join(word_tokenize(abstract.lower())) if abstract else " "
        for abstract in dataset_abstracts
    ]

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

    paper_tfidf = vectorizer.fit_transform(
        tokenized_paper_abstracts
    )  # Paper abstracts TF-IDF
    dataset_tfidf = vectorizer.transform(
        tokenized_dataset_abstracts
    )  # Dataset abstracts TF-IDF (same vocab)

    similarity_matrix = cosine_similarity(paper_tfidf, dataset_tfidf)

    matches = []
    for paper_idx in range(similarity_matrix.shape[0]):
        similarities = similarity_matrix[paper_idx]
        best_match_index = similarities.argmax()
        best_match_score = similarities[best_match_index]
        if best_match_score < 0.6:
            continue

        paper = database.publications[int(paper_idx)]
        dataset = database.datasets[int(best_match_index)]

        matches.append(
            {
                "paper": {
                    "id": paper["id"],
                    "doi": paper["paper_doi"],
                    "title": paper["paper_title"],
                },
                "dataset": {
                    "id": dataset["id"],
                    "title": dataset["metadata"]["summary"]["title"],
                },
                "score": float(best_match_score),
            }
        )

    return {"data": matches}


@router.get("/")
def all():
    def add_label(x, label):
        x["source"] = label
        return x

    data = [add_label(x, "LLM Gemini") for x in database.get_linkages()]
    extra = via_abstracts()["data"]

    [data.append(add_label(x, "TfidVectorise")) for x in extra]

    return {"data": data}
