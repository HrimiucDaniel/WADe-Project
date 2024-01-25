from flask import Flask, render_template, request, redirect, url_for
import zone_labels
import plant_labels
import re
import add_comments

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


@app.route('/zone/<zone_name>/plant/<plant_name>')
def plant(zone_name, plant_name):
    # url = f'http://127.0.0.1:5000/zone/{zone_name}/plant/{plant_name}'
    # val = url.replace(" ", "%20")
    plant_info = plant_labels.get_plant_info(zone_name, plant_name)
    #print(plant_info)
    # print(plant_info.keys())
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

    zone_info = plant_info["https://dbpedia.org/property/zone"]

    return render_template('plant.html', title=plant_name, abstract=abstract, subspecies=subspecies, ecology=ecology,
                           taxonomy=taxonomy, zone=zone_info, comments=comments)


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


if __name__ == '__main__':
    app.run(debug=True)