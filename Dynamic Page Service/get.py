from SPARQLWrapper import SPARQLWrapper, JSON


def get_all_plants():
    endpoint_url = "http://localhost:3030/zones/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?object
    WHERE {
        ?subject rdfs:label ?object.
    }
    """

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_list = []
    for result in results["results"]["bindings"]:
        result_list.append(result["object"]["value"])

    return result_list

def get_all_zones():
    endpoint_url = "http://localhost:3030/zones/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?object
    WHERE {
        ?subject rdfs:label ?object.
    }
    """

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_list = []
    for result in results["results"]["bindings"]:
        result_list.append(result["object"]["value"])

    return result_list


def get_plant(plant_name):
    endpoint_url = "http://localhost:3030/zones/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject rdfs:label "%s".
        ?subject ?predicate ?object.

    }
    """%(plant_name)

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_dict = {}
    for result in results["results"]["bindings"]:
        result_dict["subject"] = result["subject"]["value"]
        result_dict["predicate"] = result["predicate"]["value"]
        result_dict["object"] = result["object"]["value"]

    return result_dict
