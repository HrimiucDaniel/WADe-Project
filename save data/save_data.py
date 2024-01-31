import os
import third
import re
import json
import plant_info
from rdflib import Graph, URIRef, Literal, BNode, Namespace
import parse_ontology_data
import get_ontology_data


def read_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        json_str = json_file.read()
        data = json.loads(json_str)
    return data


def split_and_filter(text):
    substrings = re.split(r'[\n*]', text)
    filtered_substrings = [substring for substring in substrings if substring]
    return filtered_substrings


def remove_text_inside_square_brackets(input_string):
    pattern = re.compile(r'\[[^\]]*\]')
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

        if ecological is not None and ecological != "No information found on the section.":
            plant_dict["ecology"] = ecological

        if taxonomic is not None and taxonomic != "No information found on the section.":
            plant_dict["taxonomy"] = taxonomic

        plant_dict["zone"] = f'http://127.0.0.1:5000/zone/{zone_name}'.replace(" ", "%20")

        parameter_value = plant_name
        result = get_ontology_data.send_sparql_query(parameter_value)
        xml_response = result

        parsed_data = parse_ontology_data.parse_sparql_response(xml_response)
        new_data = {}
        for key, item in parsed_data.items():
            key2 = key.split("#")[-1]
            new_data[key2] = item
        plant_dict.update(new_data)
        print(plant_name)
        subject = get_ontology_data.get_subject_by_label(plant_name)

        plant_dict["sameAs"] = [subject, f'https://dbpedia.org/page/{plant_name}']

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
        print(predicate)
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
    custom_label = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    custom_abstract = Namespace("https://dbpedia.org/ontology/")
    custom_local = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    custom_type = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    custom_sub = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    custom_synonim = Namespace("http://www.geneontology.org/formats/oboInOwl#")
    custom_rank = Namespace("http://purl.obolibrary.org/obo/ncbitaxon#")
    custom_owl = Namespace("https://www.w3.org/2002/07/owl")

    # Convert the subject to a URIRef
    subject_uri = URIRef(f"{subject.replace(' ', '%20')}")

    # Add triples to the graph using the subject, predicate, and object
    for predicate, obj in predicate_object_dict.items():
        if predicate == "zone":
            predicate_uri = custom_local[predicate]
        elif predicate == "subspecies":
            predicate_uri = custom_ns[predicate]
        elif predicate == "label":
            predicate_uri = custom_label[predicate]
        elif predicate == "abstract":
            predicate_uri = custom_abstract[predicate]
        elif "type" in predicate:
            predicate_uri = custom_type[predicate]
        elif "rank" in predicate:
            predicate_uri = custom_rank[predicate]
        elif "Class" in predicate:
            predicate_uri= custom_sub[predicate]
        elif "Exact" in predicate:
            predicate_uri = custom_synonim[predicate]
        elif predicate == "sameAs":
            predicate_uri = custom_owl[predicate]
        else:
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
            path = f'D:/WAD3/WADe-Project/apache jena/ontology/{zone_name}/{result["label"]}.xml'

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
