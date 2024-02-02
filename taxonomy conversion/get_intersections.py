import json
import os
import intersectii


def parse_all_jsonld_files(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)

    # Iterate through each file
    for file_name in files:
        # Check if the file has a .jsonld extension
        if file_name.endswith('.jsonld'):
            # Parse the JSON-LD file
            file_data = parse_jsonld_file(folder_path, file_name)
            # Print the parsed data
            about = file_data["@id"]
            stanga = file_data["stanga"]
            dreapta = file_data["dreapta"]
            inainte = file_data["inainte"]
            label = file_data["label"]
            filename = f'D:/WAD3/WADe-Project/apache jena/taxonomy/intersectii/{file_name}.rdf'

            intersectii.create_rdf_xml_file(about, stanga, dreapta, inainte, label, filename)

def parse_jsonld_file(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    data = {
        "@id": json_data["@id"],
        "stanga": json_data["stanga"],
        "dreapta": json_data["dreapta"],
        "inainte": json_data["inainte"],
        "label": json_data["label"]
    }
    return data


# Example usage:
folder_path = 'D:/WAD3/WADe-Project/apache jena/dataset/intersectii'
parsed_data = parse_all_jsonld_files(folder_path)
