import os
from flask import Flask, render_template, jsonify
import third
import re
import json
import plant_info

app = Flask(__name__)


@app.route('/')
def index():
    # 1. Print all zones
    zones = get_zones()
    return render_template('index.html', zones=zones)


@app.route('/zone/<zone_name>')
def zone(zone_name):
    # 2. Print all plants in the selected zone
    plants = get_plants(zone_name)
    return render_template('zone.html', zone_name=zone_name, plants=plants)


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


@app.route('/plant/<zone_name>/<plant_name>')
def plant(zone_name, plant_name):
    # Get data from the selected plant JSON file
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
        if data2 is not None:
            subspecies_text = split_and_filter(data2)
            return render_template('plant.html', title=plant_name, abstract=abstract_text, subspecies=subspecies_text,
                                   habitat=info, ecology=ecological, taxonomy=taxonomic)
        else:
            return render_template('plant.html', title=plant_name, abstract=abstract_text, habitat=info,
                                   ecology=ecological, taxonomy=taxonomic)


def get_zones():
    root_path = 'D:/WAD3/WADe-Project/apache jena/dbpedia'
    return [zone for zone in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, zone))]


def get_plants(zone_name):
    zone_path = os.path.join('D:/WAD3/WADe-Project/apache jena/dbpedia', zone_name)
    return [plant.replace('.json', '') for plant in os.listdir(zone_path) if plant.endswith('.json')]


if __name__ == '__main__':
    app.run(debug=True)
