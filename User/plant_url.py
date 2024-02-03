from SPARQLWrapper import SPARQLWrapper, JSON


def get_plant_name(plant_name):
    endpoint_url = "http://localhost:3030/plants/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subject
    WHERE {
        ?subject rdfs:label "%s" .
        ?subject ?predicate ?object .
    }
    """ % (plant_name)

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_list = []
    for result in results["results"]["bindings"]:
        result_list.append(result["subject"]["value"])

    return result_list[0] if result_list is not None else []


