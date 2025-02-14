import requests

def query_openaire(datasets, result_limit=10):
    url = "https://api.openaire.eu/graph/researchProducts"
    headers = {"accept": "application/json"}
    results = {}
    
    for dataset in datasets:
        params = {
            "search": dataset,
            "type": "publication",
            "page": 1,
            "pageSize": result_limit,
            "sortBy": "relevance DESC"
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            formatted_results = []
            
            for item in data.get("results", []):
                formatted_results.append({
                    "Title": item.get("mainTitle", "N/A"),
                    #"Publication Date": item.get("publicationDate", "N/A"),
                    #"Authors": ", ".join([author.get("fullName", "N/A") for author in item.get("author", [])]),
                    #"Subjects": ", ".join([subj.get("subject", {}).get("value", "N/A") for subj in item.get("subjects", [])]),
                    #"Publisher": item.get("publisher", "N/A"),
                    #"Access Right": item.get("bestAccessRight", {}).get("label", "N/A"),
                    #"URL": ", ".join([inst.get("url", ["N/A"])[0] for inst in item.get("instance", [])]),
                    "DOI": ", ".join([pid.get("value", "N/A") for pid in item.get("pid", [])])
                })
            
            results[dataset] = formatted_results
        else:
            results[dataset] = {"error": f"Failed to retrieve data: {response.status_code}"}
    
    return results
