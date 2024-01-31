from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import json
import re


def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_wikipedia_description(concept):
    # Construct the Wikipedia API URL
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&titles={concept}"

    try:
        # Send a GET request to the Wikipedia API
        response = requests.get(api_url)
        data = response.json()

        # Extract the page content
        pages = data['query']['pages']
        for page_id in pages:
            page = pages[page_id]
            if 'extract' in page:
                # Remove HTML tags from the description
                description = remove_html_tags(page['extract'])
                return description

        return "Description not found."
    except Exception as e:
        print("Error:", e)
        return None



def get_label_for_subject(subject_uri):
    endpoint_url = "https://sparql.hegroup.org/sparql"
    # Set up SPARQL wrapper
    sparql = SPARQLWrapper(endpoint_url)

    # SPARQL query
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label
    WHERE {{
      <{subject_uri}> rdfs:label ?label .
    }}
    """

    # Set the query and format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and parse results
    try:
        results = sparql.query().convert()
        if results and 'results' in results and 'bindings' in results['results']:
            if results['results']['bindings']:
                label = results['results']['bindings'][0]['label']['value']
                return label
            else:
                return "Label not found for the subject."
        else:
            return "No results found for the query."
    except Exception as e:
        print("Error:", e)
        return None

# Example usage:
# if __name__ == "__main__":
#
#     subject_uri = "http://purl.obolibrary.org/obo/NCBITaxon_91835"
#     label = get_label_for_subject(subject_uri)
#     if label:
#         print(f"Label for subject {subject_uri}: {label}")
#     else:
#         print("Query failed or returned no results.")
