from flask import Flask, render_template, redirect, url_for
from rdflib import ConjunctiveGraph
import os

app = Flask(__name__)



@app.route('/')
def index():
    dataset_path = 'D:/WAD3/WADe-Project/apache jena/dataset/'
    folders = [folder for folder in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, folder))]
    return render_template('index.html', folders=folders)


@app.route('/zone/<zone_name>')
def zone(zone_name):
    zone_path = f'D:/WAD3/WADe-Project/apache jena/dataset/{zone_name}'
    xml_files = [file[:-4] for file in os.listdir(zone_path) if file.endswith('.xml')]

    return render_template('zone.html', zone_name=zone_name, xml_files=xml_files)


def find_subject_with_most_predicates_and_objects(graph):
    subject_counts = {}

    for subject, predicate, obj in graph:
        subject_str = str(subject)

        if subject_str in subject_counts:
            subject_counts[subject_str]["count"] += 1
        else:
            subject_counts[subject_str] = {"count": 1, "triples": []}

        subject_counts[subject_str]["triples"].append((predicate, obj))

    if subject_counts:
        max_subject = max(subject_counts, key=lambda x: subject_counts[x]["count"])
        return [(max_subject, subject_counts[max_subject]["triples"])]
    else:
        return None



@app.route('/plants/<path:zone_name>/<path:plant_name>')
def plant(zone_name, plant_name):
    try:
        xml_file_path = f'D:/WAD3/WADe-Project/apache jena/dataset/{zone_name}/{plant_name}.xml'

        # Parse RDF data from XML file
        graph = ConjunctiveGraph()
        graph.parse(xml_file_path)

        # Find the subject with the most predicates and objects
        rdf_data = find_subject_with_most_predicates_and_objects(graph)

        if rdf_data:
            # Render the plant template with filtered RDF data
            return render_template('plant.html', plant_name=plant_name, rdf_data=rdf_data, zone_name=zone_name)
        else:
            return 'No RDF data found for the plant.'
    except FileNotFoundError:
        return 'Plant data not found.'


if __name__ == '__main__':
    app.run(debug=True)
