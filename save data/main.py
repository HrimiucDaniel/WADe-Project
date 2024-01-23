from flask import Flask, render_template, jsonify
import os
import json
import re

app = Flask(__name__)

# Path to the directory containing botanical garden zones
base_path = r'D:\WAD3\WADe-Project\apache jena\dataset'


def get_value(data, predicate):
    if predicate in data:
        if isinstance(data[predicate], list):
            return data[predicate][0]['@value']
        elif isinstance(data[predicate], str):
            # Convert the string to a list
            return json.loads(data[predicate])[0]
    return None


@app.route('/')
def index():
    # Get the list of botanical garden zones
    zones = [zone for zone in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, zone))]
    return render_template('index.html', zones=zones)


@app.route('/zone/<zone_name>')
def zone(zone_name):
    # Get the list of json ld files in the specified zone
    zone_path = os.path.join(base_path, zone_name)
    plant_files = [file.replace('.jsonld', '') for file in os.listdir(zone_path) if file.endswith('.jsonld')]
    return render_template('zone.html', zone_name=zone_name, plant_files=plant_files)


def split_and_filter(text):
    # Remove square brackets from the text
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r"'", '', text)

    # Split the text using both "\n" and "*" as delimiters
    substrings = re.split(r'[\n*,]', text)

    # Filter out empty strings from the resulting list
    filtered_substrings = [substring.strip() for substring in substrings if substring]

    return filtered_substrings


@app.route('/plant/<zone_name>/<plant_name>')
def plant(zone_name, plant_name):
    # Read and format the rdf data inside the specified json ld file
    zone_path = os.path.join(base_path, zone_name)
    file_path = os.path.join(zone_path, f"{plant_name}.jsonld")

    with open(file_path, 'r') as file:
        rdf_data = json.load(file)

    title = get_value(rdf_data[0], 'https://dbpedia.org/property/label')
    abstract = get_value(rdf_data[0], 'https://dbpedia.org/property/abstract')
    subspecies = get_value(rdf_data[0], 'https://dbpedia.org/property/subspecies')
    ecology = get_value(rdf_data[0], 'https://dbpedia.org/property/ecology')
    taxonomy = get_value(rdf_data[0], 'https://dbpedia.org/property/taxonomy')

    if subspecies is not None:
        subspecies = split_and_filter(subspecies)
        print(subspecies)

    return render_template('plant.html', title=title, abstract=abstract, subspecies=subspecies, ecology=ecology,
                           taxonomy=taxonomy)


if __name__ == '__main__':
    app.run(debug=True)
