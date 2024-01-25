from SPARQLWrapper import SPARQLWrapper, JSON


def get_labels_from_sparql():
    endpoint_url = "http://localhost:3030/Zones/sparql"
    # Set up the SPARQLWrapper with the provided endpoint URL
    sparql = SPARQLWrapper(endpoint_url)

    # Set the SPARQL query to retrieve the values for the "label" predicate
    sparql.setQuery("""
        SELECT ?label
        WHERE {
          ?subject <https://dbpedia.org/property/label> ?label
        }
        LIMIT 100
    """)

    # Set the query type (in this case, it's a SELECT query)
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()

    # Extract and return the values for the "label" predicate
    label_values = [result["label"]["value"] for result in results["results"]["bindings"]]
    return label_values


# Example usage:
# endpoint_url = "http://localhost:3030/Zones/sparql"
# labels = get_labels_from_sparql(endpoint_url)
#
# # Print the list of label values
# print(labels)
