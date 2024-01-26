from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import zone_labels
import plant_labels
import re
import add_comments
from werkzeug.utils import secure_filename
import os
import add_images
import add_relations
import get_relations

app = Flask(__name__)


def split_and_filter(text):
    # Remove square brackets from the text
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r"'", '', text)

    # Split the text using both "\n" and "*" as delimiters
    substrings = re.split(r'[\n*,]', text)

    # Filter out empty strings from the resulting list
    filtered_substrings = [substring.strip() for substring in substrings if substring]

    return filtered_substrings


# Function to create URLs for dynamic routes
def generate_url(*args):
    return '/'.join(map(str, args))


@app.route('/zones')
def zones():
    labels = zone_labels.get_labels_from_sparql()
    return render_template('zones.html', labels=labels, generate_url=generate_url)


@app.route('/zone/<zone_name>')
def zone(zone_name):
    plants = plant_labels.get_all_plants(zone_name)

    return render_template('zone.html', zone_name=zone_name, plants=plants, generate_url=generate_url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/zone/<zone_name>/plant/<plant_name>', methods=['GET', 'POST'])
def plant(zone_name, plant_name):
    uploaded_images = []  # Initialize the variable here

    if request.method == 'POST':
        plant_uri, uploaded_images = process_image_upload(request, app.config['UPLOAD_FOLDER'], zone_name, plant_name)
        add_images.add_images_to_plant(plant_uri, uploaded_images)
    plant_info = plant_labels.get_plant_info(zone_name, plant_name)
    abstract_key = "https://dbpedia.org/property/abstract"
    if abstract_key in plant_info:
        abstract = plant_info[abstract_key]
    else:
        abstract = None

    subspecies_key = "https://dbpedia.org/property/subspecies"
    if subspecies_key in plant_info:
        subspecies = plant_info[subspecies_key]
        subspecies = split_and_filter(subspecies)
    else:
        subspecies = None

    ecology_key = "https://dbpedia.org/property/ecology"
    if ecology_key in plant_info:
        ecology = plant_info[ecology_key]
    else:
        ecology = None

    taxonomy_key = "https://dbpedia.org/property/taxonomy"
    if taxonomy_key in plant_info:
        taxonomy = plant_info[taxonomy_key]
    else:
        taxonomy = None

    comment_key = "https://dbpedia.org/property/comments"
    if comment_key in plant_info:
        comments = plant_info[comment_key]
    else:
        comments = None

    image_key = "https://dbpedia.org/property/images"
    if image_key in plant_info:
        image = plant_info[image_key]
    else:
        image = None

    plants = plant_labels.get_all_plants(zone_name)

    near_by_list = plants
    near_by_list.append(zone_name)

    relation_dict = get_relations.get_plant_info(zone_name, plant_name)

    # print(f"Uploaded Images: {image}")

    return render_template('plant.html', title=plant_name, abstract=abstract, subspecies=subspecies, ecology=ecology,
                           taxonomy=taxonomy, zone=zone_name, comments=comments, images=image,
                           near_by_list=near_by_list, relations=relation_dict)


@app.route('/zone/<zone_name>/plant/<plant_name>/add_comment', methods=['POST'])
def add_comment(zone_name, plant_name):
    comment = request.form.get('comment')
    good_comment = [comment]
    uri = f'http://127.0.0.1:5000/zone/{zone_name}/plant/{plant_name}'
    plant_uri = uri.replace(" ", "%20")
    # Add the comment to the triple store using your existing function
    add_comments.add_comments_to_plant(plant_uri, good_comment)
    # Redirect back to the plant page after adding the comment
    return redirect(url_for('plant', zone_name=zone_name, plant_name=plant_name))


@app.route('/zone/<zone_name>/plant/<plant_name>/add_relation', methods=['POST'])
def add_relation(zone_name, plant_name):
    relation = request.form.get('relation')
    near_by_option = request.form.get('near_by_option')
    uri = f'http://127.0.0.1:5000/zone/{zone_name}/plant/{plant_name}'
    plant_uri = uri.replace(" ", "%20")
    add_relations.add_relation_to_plant(plant_uri, relation, near_by_option, zone_name)
    return redirect(url_for('plant', zone_name=zone_name, plant_name=plant_name))


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def process_image_upload(request, upload_folder, zone_name, plant_name):
    uploaded_images = []
    uri = f'http://127.0.0.1:5000/zone/{zone_name}/plant/{plant_name}'
    plant_uri = uri.replace(" ", "%20")

    if 'images' in request.files:
        images = request.files.getlist('images')
        for image in images:
            # Save the image to the specified folder
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(upload_folder, image_filename)
            image.save(image_path)

            # Construct the URL based on your setup
            image_url = f'http://127.0.0.1:5000/uploads/{image_filename}'
            uploaded_images.append(image_url)

    return plant_uri, uploaded_images


@app.route('/zone/<zone_name>/plant/<plant_name>/upload_image', methods=['POST'])
def upload_image(zone_name, plant_name):
    plant_uri, uploaded_images = process_image_upload(request, app.config['UPLOAD_FOLDER'], zone_name, plant_name)
    add_images.add_images_to_plant(plant_uri, uploaded_images)
    return redirect(url_for('plant', zone_name=zone_name, plant_name=plant_name))


if __name__ == '__main__':
    app.run(debug=True)
