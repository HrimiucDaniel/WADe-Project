import requests
import xml.etree.ElementTree as ET


def send_sparql_query(param):
    # SPARQL query with a placeholder for the parameter
    sparql_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?predicate ?object
    WHERE {
      ?subject rdfs:label "%s".
      ?subject ?predicate ?object.
      FILTER (?predicate IN (
        <http://www.w3.org/2000/01/rdf-schema#subClassOf>,
        <http://www.geneontology.org/formats/oboInOwl#hasExactSynonym>,
        <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>,
        <http://purl.obolibrary.org/obo/ncbitaxon#has_rank>
      ))
    }
    """ % param

    # Endpoint URL
    endpoint_url = "https://sparql.hegroup.org/sparql"

    # HTTP POST request with the SPARQL query
    response = requests.post(endpoint_url, data={'query': sparql_query},
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        return response.text
    else:
        return "Error: Unable to fetch data from the SPARQL endpoint."


def get_subject_by_label(label):
    # SPARQL query to retrieve the subject for a given label
    sparql_query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subject
    WHERE {
      ?subject rdfs:label "%s".
    }
    """ % label

    # Endpoint URL
    endpoint_url = "https://sparql.hegroup.org/sparql"

    # HTTP POST request with the SPARQL query
    response = requests.post(endpoint_url, data={'query': sparql_query},
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        try:
            # Parse XML response
            root = ET.fromstring(response.text)

            # Find the subject URI in the XML response
            subject_uri = None
            for result in root.findall(
                    '{http://www.w3.org/2005/sparql-results#}results/{http://www.w3.org/2005/sparql-results#}result'):
                binding = result.find('{http://www.w3.org/2005/sparql-results#}binding[@name="subject"]')
                subject_uri = binding.find('{http://www.w3.org/2005/sparql-results#}uri').text
                break  # Exit loop after finding the first subject URI

            return subject_uri
        except Exception as e:
            print("Error parsing XML response:", e)
            return None
    else:
        print("Error: Unable to fetch data from the SPARQL endpoint.")
        return None


# if __name__ == "__main__":
#     # Example usage: Replace 'Your_Label' with the label you want to search for
#     label = 'Your_Label'
#     subject = get_subject_by_label(label)
#     print("Subject for label '%s': %s" % (label, subject))