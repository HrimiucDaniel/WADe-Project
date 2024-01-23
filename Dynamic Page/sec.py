from rdflib import Graph, Namespace, URIRef, Literal
import json


def parse_dbpedia_sparql_results(data):
    g = Graph()

    # Assuming 'data' is the SPARQL results in JSON format
    results = data['results']['bindings']

    for result in results:
        predicate = result.get('predicate', {}).get('value')
        obj = result.get('object', {}).get('value')
        obj_lang = result.get('object', {}).get('xml:lang')

        if predicate and obj:
            predicate_uri = URIRef(predicate)
            subject_uri = URIRef("http://example.org/resource/1")  # Replace with actual subject URI

            # You may need to adjust the datatype or language tag based on your data
            if obj_lang:
                g.add((subject_uri, predicate_uri, Literal(obj, lang=obj_lang)))
            else:
                g.add((subject_uri, predicate_uri, Literal(obj)))

    x = g.serialize(format='turtle')
    return x

# Example usage


def read_and_transform_json_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Assuming the file contains JSON data
            data_dict = json.load(file)

            # Assuming parse_dbpedia_sparql_results is a function that takes a dictionary as input
            parsed_data = parse_dbpedia_sparql_results(data_dict)

            return parsed_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


