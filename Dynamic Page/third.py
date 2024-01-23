from rdflib import Graph, Namespace, URIRef, Literal
import sec
import json


def filter_and_get_objects(graph, predicates):
    objects = set()
    for subj, pred, obj in graph:
        if pred == predicates:
            objects.add(obj)
    return objects


def return_predicate(sparql_results_data, predicate, namespace):
    turtle_data = sec.parse_dbpedia_sparql_results(sparql_results_data)
    g = Graph()
    g.parse(data=turtle_data, format='turtle')

    # Use the correct namespace for 'abstract'
    dbpedia_ns = Namespace(f"http://dbpedia.org/{namespace}/")
    predicates_of_interest = dbpedia_ns[predicate]

    objects = filter_and_get_objects(g, predicates_of_interest)
    for obj in objects:
        return obj
