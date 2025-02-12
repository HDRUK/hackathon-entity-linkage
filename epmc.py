import requests
import json

def epmc_by_doi(doi):
    '''
    doi: string - doi of a paper to serach in format '10.xxx...'
    '''
    pmc_base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest"
    
    # Insert doi validation here

    doi_query = "query=(DOI:%s)" % (doi)
    epmc_url = "%s/search?%s&resultType=lite&format=json" % (pmc_base_url, doi_query)
    response = requests.get(epmc_url)
    return response.json()


# If match - call EPMC articles api for most of the paper?