from SPARQLWrapper import SPARQLWrapper, JSON


def get_plant_info(zone, name):
    endpoint_url = "http://localhost:3030/Plants/sparql"
    # Create a SPARQLWrapper object and set the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)
    uri = f'http://127.0.0.1:5000/zone/{zone}/plant/{name}'
    subject_uri = uri.replace(" ", "%20")
    if subject_uri.endswith("[]"):
        return 0


    # SPARQL query to get all predicates and objects based on zone and name
    query = """
        SELECT DISTINCT ?predicate ?object WHERE {
            <%s> ?predicate ?object .
            FILTER(STRSTARTS(STR(?predicate), "http://127.0.0.1:5000/relations/"))
        }
    """% (subject_uri)

    # Set the SPARQL query
    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()

    # Process the results and create a dictionary with predicates and objects

    relation_dict = {}

    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        object_value = result["object"]["value"]

        # If the predicate already exists in the dictionary
        if predicate in relation_dict:
            # Append the object_value to the existing list
            relation_dict[predicate].append(object_value)
        else:
            # Create a new list for the predicate and add the object_value
            relation_dict[predicate] = [object_value]

    return relation_dict

