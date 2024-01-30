import os
import third
import re
import json
import plant_info
from rdflib import Graph, URIRef, Literal, BNode, Namespace


def read_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_str = json_file.read()
        data = json.loads(json_str)
    return data


def split_and_filter(text):
    # Split the text using both "\n" and "*" as delimiters
    substrings = re.split(r'[\n*]', text)

    # Filter out empty strings from the resulting list
    filtered_substrings = [substring for substring in substrings if substring]

    return filtered_substrings


def remove_text_inside_square_brackets(input_string):
    # Define the regular expression pattern for text inside square brackets
    pattern = re.compile(r'\[[^\]]*\]')

    # Use the sub function to replace matches with an empty string
    result_string = re.sub(pattern, '', input_string)

    return result_string


def plant(zone_name, plant_name):
    plant_dict = {}
    json_path = os.path.join('D:/WAD3/WADe-Project/apache jena/dbpedia', zone_name, f'{plant_name}.json')
    with open(json_path, 'r') as file:
        data_dict = json.load(file)
        data = third.return_predicate(data_dict, "abstract", "ontology")
        abstract_text = data
        data2 = third.return_predicate(data_dict, "subdivision", "property")
        habitat_info = plant_info.get_distribution_and_habitat(plant_name, "Distribution_and_habitat")
        info = remove_text_inside_square_brackets(habitat_info)
        eco_info = plant_info.get_distribution_and_habitat(plant_name, "Ecology")
        ecological = remove_text_inside_square_brackets(eco_info)
        taxo_info = plant_info.get_distribution_and_habitat(plant_name, "Taxonomy")
        taxonomic = remove_text_inside_square_brackets(taxo_info)

        plant_dict["label"] = plant_name

        if abstract_text is not None:
            plant_dict["abstract"] = abstract_text

        if data2 is not None and data2 != "See text" and data2 != "['See text']":
            subspecies_text = split_and_filter(data2)
            plant_dict["subspecies"] = subspecies_text

        if info is not None and info != "No information found on the section.":
            plant_dict["habitat"] = info

        if ecological is not None and info != "No information found on the section.":
            plant_dict["ecology"] = ecological

        if taxonomic is not None and info != "No information found on the section.":
            plant_dict["taxonomy"] = taxonomic

        # plant_dict["comments"] = ""
        # plant_dict["images"] = ""

        plant_dict["zone"] = f'http://127.0.0.1:5000/zone/{zone_name}'.replace(" ", "%20")

        return plant_dict


def create_rdf(subject_url, predicate_object_dict):
    # Create an RDF graph
    g = Graph()

    # Create a Namespace for your custom labels
    custom_ns = Namespace("https://dbpedia.org/property/")

    # Add the subject to the graph
    # subject = URIRef(subject_url)
    subject = URIRef(f"{subject_url.replace(' ', '%20')}")

    # Iterate through the predicate-object dictionary and add triples to the graph
    for predicate, obj in predicate_object_dict.items():
        predicate_uri = custom_ns[predicate]
        g.add((subject, predicate_uri, Literal(obj)))

    return g


def save_rdf_to_json_ld(graph, label, path):
    # Serialize the RDF graph to JSON-LD format
    json_ld_data = graph.serialize(format='json-ld')

    # Save the JSON-LD data to a file
    filename = f"{label}.jsonld"
    with open(f"{path}/{filename}", 'w', encoding='utf-8') as f:
        f.write(json_ld_data)


def save_rdf_data(subject, predicate_object_dict, file_path):
    # Create an RDF graph
    g = Graph()

    # Define a custom namespace for your predicates
    custom_ns = Namespace("https://dbpedia.org/property/")

    # Convert the subject to a URIRef
    subject_uri = URIRef(f"{subject.replace(' ', '%20')}")

    # Add triples to the graph using the subject, predicate, and object
    for predicate, obj in predicate_object_dict.items():
        predicate_uri = custom_ns[predicate]
        g.add((subject_uri, predicate_uri, Literal(obj)))

    # Serialize the RDF graph to RDF/XML and save it to the specified file path
    g.serialize(destination=file_path, format="xml")


def apply_plant_function_to_folder(zone_name):
    folder_path = os.path.join('D:/WAD3/WADe-Project/apache jena/dbpedia', zone_name)

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            plant_name = os.path.splitext(filename)[0]

            result = plant(zone_name, plant_name)

            subject_url = f'http://127.0.0.1:5000/zone/{zone_name}/plant/{result["label"]}'
            # valid_url = quote(subject_url)
            subject_uri = URIRef(f"{subject_url.replace(' ', '%20')}")

            label = result["label"]
            path = f'D:/WAD3/WADe-Project/apache jena/dataset/{zone_name}/{result["label"]}.xml'

            save_rdf_data(subject_uri, result, path)


apply_plant_function_to_folder("Zona 1 - Sectia Sistematica")
apply_plant_function_to_folder("Zona 2 - Sectia Fitogeografica")
apply_plant_function_to_folder("Zona 3 - Complexul de Sere")
apply_plant_function_to_folder("Zona 4 - Sectia Flora si Vegetatia Romaniei")
apply_plant_function_to_folder("Zona 5 - Sectia Silvostepa Moldovei")
apply_plant_function_to_folder("Zona 6 - Sectia Biologica")
apply_plant_function_to_folder("Zona 7 - Sectia Plante Utile")
apply_plant_function_to_folder("Zona 8 - Sectia Dendrarium")
apply_plant_function_to_folder("Zona 9 - Sectia Ornamentala")
apply_plant_function_to_folder("Zona 10 - Sectia Rosarium")


#
# result = plant("Zona 1 - Sectia Sistematica", "Liliaceae")
# for key in result:
#     print(key, result[key])
# # subject_url = f'http://127.0.0.1:5000/plant/{result["zone"]}/{result["label"]}'
# valid_sub = quote(subject_url)
# save_rdf_data(valid_sub, result, f'D:/WAD3/WADe-Project/apache jena/dataset/Zona 1 - Sectia Sistematica/'
#                                  f'{result["label"]}.xml')
