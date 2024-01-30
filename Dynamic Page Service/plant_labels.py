from SPARQLWrapper import SPARQLWrapper, JSON


def get_plant_info(zone, name):
    endpoint_url = "http://localhost:3030/Plants/sparql"
    # Create a SPARQLWrapper object and set the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)

    # SPARQL query to get all predicates and objects based on zone and name
    query = """
    PREFIX dbp: <https://dbpedia.org/property/>

    SELECT ?predicate ?object
    WHERE {
        ?subject dbp:label "%s" .
        ?subject dbp:zone "%s" .
        ?subject ?predicate ?object .
    }
    """ % (name, zone)

    # Set the SPARQL query
    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()

    # Process the results and create a dictionary with predicates and objects
    plant_info_dict = {"https://dbpedia.org/property/comments": [], "https://dbpedia.org/property/images": []}

    for result in results["results"]["bindings"]:
        predicate = result["predicate"]["value"]
        object_value = result["object"]["value"]

        if predicate == "https://dbpedia.org/property/comments":
            plant_info_dict["https://dbpedia.org/property/comments"].append(object_value)
        elif predicate == "https://dbpedia.org/property/images":
            plant_info_dict["https://dbpedia.org/property/images"].append(object_value)
        else:
            plant_info_dict[predicate] = object_value

    return plant_info_dict


def get_all_plants(zone):
    endpoint_url = "http://localhost:3030/Plants/sparql"
    # Create a SPARQLWrapper object and set the endpoint URL
    sparql = SPARQLWrapper(endpoint_url)
    zone2 = zone.split("/")[-1]

    # SPARQL query to get predicates and objects based on zone and name
    query = """
    PREFIX dbp: <https://dbpedia.org/property/>

    SELECT ?predicate ?object
    WHERE {
        ?subject dbp:zone "%s" .
        ?subject dbp:label ?object .
    }
    """ % (zone)

    # Set the SPARQL query
    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()

    # Process the results and create a dictionary of predicate-object pairs
    label_list = []
    for result in results["results"]["bindings"]:
        object_value = result["object"]["value"]
        label_list.append(object_value)

    return label_list

# endpoint_url = "http://localhost:3030/Plants/sparql"
# zone = "http://127.0.0.1:5000/zone/Zona%205%20-%20Sectia%20Silvostepa%20Moldovei"
# result_dict = get_all_plants(zone)
# print(result_dict)

# # Example usage:
# endpoint_url = "http://localhost:3030/Plants/sparql"
# zone = "Zona 1 - Sectia Sistematica"
# name = "Celastraceae"
#
# result_dict = sparql_query(endpoint_url, zone, name)
# print(result_dict)
