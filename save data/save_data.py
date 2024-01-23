import os
import third
import re
import json
import plant_info
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, FOAF
from urllib.parse import quote


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

        if data2 is not None and data2 != "See text" and data2 !="['See text']":
            subspecies_text = split_and_filter(data2)
            plant_dict["subspecies"] = subspecies_text

        if info is not None and info != "No information found on the section.":
            plant_dict["habitat"] = info

        if ecological is not None and info != "No information found on the section.":
            plant_dict["ecology"] = ecological

        if taxonomic is not None and info != "No information found on the section.":
            plant_dict["taxonomy"] = taxonomic

        return plant_dict


def create_rdf(subject_url, predicate_object_dict):
    # Create an RDF graph
    g = Graph()

    # Create a Namespace for your custom labels
    custom_ns = Namespace("https://dbpedia.org/property/")

    # Add the subject to the graph
    subject = URIRef(subject_url)

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


def apply_plant_function_to_folder(zone_name):
    folder_path = os.path.join('D:/WAD3/WADe-Project/apache jena/dbpedia', zone_name)

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Extract plant_name from the filename (assuming filenames are like 'plant_name.json')
            plant_name = os.path.splitext(filename)[0]

            # Call the plant function for each file
            result = plant(zone_name, plant_name)

            # Print or do something with the result (e.g., store it in a list or another data structure)

            # print(f'http://127.0.0.1:5000/plant/{zone_name}/{result["title"]}', result)

            subject_url = f'http://127.0.0.1:5000/plant/{zone_name}/{result["label"]}'
            valid_url = quote(subject_url)

            rdf_graph = create_rdf(valid_url, result)
            label = result["label"]
            path = "D:/WAD3/WADe-Project/apache jena/dataset/Zona 1 - Sectia Sistematica"

            save_rdf_to_json_ld(rdf_graph, label, path)  # Corrected indentation


apply_plant_function_to_folder("Zona 1 - Sectia Sistematica")
