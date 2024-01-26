import os
from urllib.parse import quote
from rdflib import Graph, Namespace, URIRef, Literal


def transform_in_url(zone_name, name):
    url = f'https://127.0.0.1:5000/zone/{zone_name}/plant/{name}'
    subject_uri = URIRef(f"{url.replace(' ', '%20')}")
    return subject_uri


def get_file_names_without_extension(folder_path):
    files = os.listdir(folder_path)

    file_names_without_extension = []

    for file in files:
        if os.path.isfile(os.path.join(folder_path, file)):
            file_name, _ = os.path.splitext(file)
            file_names_without_extension.append(file_name)

    return file_names_without_extension


def create_list_plants(zone_name):
    folder_path = f'D:/WAD3/WADe-Project/apache jena/dbpedia/{zone_name}'
    file_names = get_file_names_without_extension(folder_path)
    url_names = [transform_in_url(zone_name, file) for file in file_names]
    return url_names

