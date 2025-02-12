import requests
import json
import xmltodict

pmc_base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest"

def epmc_by_doi(doi):
    '''
    doi: string - doi of a paper to serach in format '10.xxx...'
    '''
    # Insert doi validation here
    doi_query = "query=(DOI:%s)" % (doi)
    epmc_url = "%s/search?%s&resultType=lite&format=json" % (pmc_base_url, doi_query)
    response = requests.get(epmc_url)
    return response.json()

def epmc_id_search(pmcid):
    '''
    uses pmcid to retrieve full text from EPMC in xml format and parses that to json
    '''
    epmc_url = "%s/%s/fullTextXML" % (pmc_base_url, pmcid)
    response = requests.get(epmc_url)
    data_dict = xmltodict.parse(response.content)
    return data_dict

def get_full_text_from_doi(doi):
    doi_match = epmc_by_doi(doi)
    pmc_id = doi_match["resultList"]["result"][0]["pmcid"]
    json_res = epmc_id_search(pmc_id)
    return json_res
