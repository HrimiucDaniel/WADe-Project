import json
from rdflib import Graph, Namespace, URIRef, Literal
import add_plants


def rdf_to_jsonld(subject, rdf_data, output_path):
    # Create an RDF graph
    g = Graph()
    #print(subject)

    # Define a namespace for your properties
    ns = Namespace("https://dbpedia.org/property/")

    # Add triples to the graph
    subject_uri = URIRef(f"http://127.0.0.1:5000/zone/{subject.replace(' ', '%20')}")
    g.add((subject_uri, ns.label, Literal(rdf_data['label'])))
    g.add((subject_uri, ns.list_of_plants, Literal(rdf_data['list_of_plants'])))
    g.add((subject_uri, ns.positioning, Literal(rdf_data['positioning'])))

    # Serialize RDF graph to JSON-LD format
    jsonld_data = {
        "@context": {
            "label": "https://dbpedia.org/property/label",
            "list_of_plants": "https://dbpedia.org/property/list_of_plants",
            "positioning": "https://dbpedia.org/property/positioning"
        },
        "@id": f"http://127.0.0.1:5000/zone/{subject.replace(' ', '%20')}",
        **rdf_data
    }

    # Save JSON-LD data to a file
    with open(output_path, 'w') as jsonld_file:
        json.dump(jsonld_data, jsonld_file, indent=2)


def save_zones(zone_name, list_of_plants, positioning):
    rdf_data = {'label': zone_name, 'list_of_plants': list_of_plants,
                'positioning': positioning}
    output_path = f'D:/WAD3/WADe-Project/apache jena/dataset/zones/{zone_name}.jsonld'
    rdf_to_jsonld(zone_name, rdf_data, output_path)


save_zones("Zona 1 - Sectia Sistematica", add_plants.create_list_plants("Zona 1 - Sectia Sistematica"), "---")
save_zones("Zona 2 - Sectia Fitogeografica", "---", "---")
save_zones("Zona 3 - Complexul de sere", "---", "---")
save_zones("Zona 4 - Sectia Flora si Vegetatia Romaniei", "---", "---")
save_zones("Zona 5 - Sectia Silvostepa Moldovei", "---", "---")
save_zones("Zona 6 - Sectia Biologica", "---", "---")
save_zones("Zona 7 - Sectia Plante Utile", "---", "---")
save_zones("Zona 8 - Sectia Dendrarium", "---", "---")
save_zones("Zona 9 - Sectia Ornamentala", "---", "---")
save_zones("Zona 10 - Sectia Rosarium", "---", "---")
