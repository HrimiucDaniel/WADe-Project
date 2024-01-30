from SPARQLWrapper import SPARQLWrapper, JSON


def retrieve_all_triples():
    # Set the endpoint URL
    endpoint = "http://localhost:3030/Intersectii/sparql"

    # Create a SPARQLWrapper object
    sparql = SPARQLWrapper(endpoint)

    # Set the SPARQL query
    sparql.setQuery("""
        SELECT ?subject ?predicate ?object
        WHERE {
          ?subject ?predicate ?object
        }
    """)

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and convert results to JSON
    results = sparql.query().convert()
    triples = []

    # Print the results
    for result in results["results"]["bindings"]:
        subject = result["subject"]["value"]
        predicate = result["predicate"]["value"]
        obj = result["object"]["value"]

        # Create a dictionary for each triple and append it to the list
        triple = {"subject": subject, "predicate": predicate, "object": obj}
        triples.append(triple)

    return triples

# Call the function to retrieve all triples
# retrieve_all_triples()
