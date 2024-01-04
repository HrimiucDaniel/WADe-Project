from flask import Flask, render_template
from rdflib import Graph
from rdflib.namespace import RDF, RDFS
from xml.etree import ElementTree as ET
import os
from rdflib import Namespace


res = Namespace("http://www.w3.org/2005/sparql-results#")

app = Flask(__name__)

# Define the path to your 'dbpedia' folder
dbpedia_folder = 'D:/WAD3/WADe-Project/apache jena/dbpedia'


@app.route('/')
def index():
    zones = get_zones()
    return render_template('index.html', zones=zones)


@app.route('/zone/<zone_name>')
def show_plants(zone_name):
    zone_path = os.path.join(dbpedia_folder, zone_name)
    plants = get_plants(zone_path)
    return render_template('plants.html', zone_name=zone_name, plants=plants)


@app.route('/zone/<zone_name>/plant/<plant_name>')
def show_rdf_data(zone_name, plant_name):
    zone_path = os.path.join(dbpedia_folder, zone_name)
    plant_path = os.path.join(zone_path, plant_name)
    rdf_data = get_rdf_data(plant_path)

    formatted_rdf_data = format_rdf_data(rdf_data)

    return render_template('rdf_data.html', zone_name=zone_name, plant_name=plant_name, rdf_data=formatted_rdf_data)

def format_rdf_data(rdf_data):
    # Parse RDF data using rdflib
    g = Graph()
    g.parse(data=rdf_data, format='xml')

    # Format RDF triples for specific nodes
    formatted_data = []

    for s, p, o in g.triples((None, RDFS.label, None)):
        formatted_data.append(f"Label: {o}")

    for s, p, o in g.triples((None, RDFS.comment, None)):
        formatted_data.append(f"Comment: {o}")

    for s, p, o in g.triples((None, res['abstract'], None)):
        formatted_data.append(f"Abstract: {o}")

    return '\n'.join(formatted_data)


def get_zones():
    return os.listdir(dbpedia_folder)


def get_plants(zone_path):
    return os.listdir(zone_path)


def get_rdf_data(plant_path):
    with open(plant_path, 'r') as file:
        rdf_data = file.read()
    return rdf_data


if __name__ == '__main__':
    app.run(debug=True)
