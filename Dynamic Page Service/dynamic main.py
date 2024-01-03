from flask import Flask, render_template
from rdflib import ConjunctiveGraph
import os

app = Flask(__name__)


@app.route('/')
def index():
    xml_folder_path = 'D:/WAD3/WADe-Project/apache jena/dataset/Zona 1 - Sectia Sistematica'  # Updated path
    plant_list = [file[:-4] for file in os.listdir(xml_folder_path) if file.endswith('.xml')]
    return render_template('index.html', plant_list=plant_list)


@app.route('/plants/<path:plant_name>')
def plant(plant_name):
    try:
        xml_file_path = f'D:/WAD3/WADe-Project/apache jena/dataset/Zona 1 - Sectia Sistematica/{plant_name}.xml'  # Updated path

        # Parse RDF data from XML file
        graph = ConjunctiveGraph()
        graph.parse(xml_file_path)

        # Get triples from RDF data
        triples = list(graph.triples((None, None, None)))

        # Render the plant template with RDF data
        return render_template('plant.html', plant_name=plant_name, rdf_data=triples)
    except FileNotFoundError:
        return 'Plant data not found.'


if __name__ == '__main__':
    app.run(debug=True)
