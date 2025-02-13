from db.database import database
from rapidfuzz import process


def find_best_matches(candidates, threshold=80):
    titles = [x["metadata"]["summary"]["title"] for x in database.datasets]

    matches = {}
    for cand in candidates:
        match_title, score, index = process.extractOne(cand, titles)

        if score >= threshold:
            data = database.datasets[index]
            matches[cand] = {
                "id": data["id"],
                "title": data["metadata"]["summary"]["title"],
            }
        else:
            matches[cand] = None

    return matches
