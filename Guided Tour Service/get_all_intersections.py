from SPARQLWrapper import SPARQLWrapper, JSON


def retrieve_all_triples():
    # Set the endpoint URL
    endpoint = "http://localhost:3030/intersectii/sparql"

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
    subject_list = []

    # Print the results
    for result in results["results"]["bindings"]:
        subject = result["subject"]["value"]
        predicate = result["predicate"]["value"]
        obj = result["object"]["value"]
        if subject not in subject_list:
            subject_list.append(subject)
    return subject_list


def retrieve_object_for_label(label):
    # Set the endpoint URL
    endpoint = "http://localhost:3030/intersectii/sparql"

    # Create a SPARQLWrapper object
    sparql = SPARQLWrapper(endpoint)

    # Set the SPARQL query to retrieve the object based on the label and predicate
    query = f"""
        SELECT ?object
        WHERE {{
          ?subject <http://www.w3.org/2000/01/rdf-schema#label> "{label}" .
          ?subject <http://127.0.0.1:5000/intersectii/inainte> ?object .
        }}
    """

    # Set the SPARQL query and return format
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and convert results to JSON
    results = sparql.query().convert()

    # Extract and return the object
    objects = []
    for result in results["results"]["bindings"]:
        objects.append(result["object"]["value"])

    return objects


def retrieve_triples_for_subject(subject_param):
    # Set the endpoint URL
    endpoint = "http://localhost:3030/intersectii/sparql"

    # Create a SPARQLWrapper object
    sparql = SPARQLWrapper(endpoint)

    # Set the SPARQL query with a filter for the subject parameter
    query = f"""
        SELECT ?predicate ?object
        WHERE {{
          <{subject_param}> ?predicate ?object .
        }}
    """
    sparql.setQuery(query)

    # Set the return format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and convert results to JSON
    results = sparql.query().convert()

    # Store triples matching the subject parameter
    triples_dict = {}

    # Extract and store the results
    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        obj = result["object"]["value"]

        if predicate not in triples_dict:
            triples_dict[predicate] = []

        triples_dict[predicate].append(obj)

    return triples_dict

# print(retrieve_all_triples())
# Example usage:
# subject_param = "http://127.0.0.1:5000/intersectii/intersectia1"  # Change this to your desired subject URI
# triples_dict = retrieve_triples_for_subject(subject_param)

# Print the retrieved triples dictionary
# for predicate, objects in triples_dict.items():
# print(f"Predicate: {predicate}, Objects: {objects}")
