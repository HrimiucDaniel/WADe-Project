import json
import os
import zones

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
            label = file_data["label"]
            plants = file_data["list_of_plants"]
            description = file_data["description"]
            filename = f'D:/WAD3/WADe-Project/apache jena/taxonomy/zones/{file_name}.rdf'

            zones.create_rdf_xml_file(about, label, plants, description, filename)


def parse_jsonld_file(folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    data = {
        "@id": json_data["@id"],
        "label": json_data["label"],
        "list_of_plants": json_data["list_of_plants"],
        "description": json_data["description"],
    }
    return data


# Example usage:
folder_path = 'D:/WAD3/WADe-Project/apache jena/dataset/zones'
parse_all_jsonld_files(folder_path)
