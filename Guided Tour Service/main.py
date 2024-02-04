from flask import Flask, render_template, send_from_directory
from flask import request, redirect, url_for
import zone_labels
import search
import get_all_intersections
import re

app = Flask(__name__)

Username = ""


@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Define your upload folder
app.config['UPLOAD_FOLDER'] = 'static/uploads'


def extract_last_part(url):
    """
    Extracts the last part of a URL after the last '/' character.
    """
    # Split the URL by '/'
    parts = url.split('/')
    # Get the last part of the URL
    last_part = parts[-1]
    return last_part


def remove_last_two_slashes(string):
    # Find the index of the last two occurrences of "/"
    last_slash_index = string.rfind("/")
    second_last_slash_index = string.rfind("/", 0, last_slash_index)

    # If both slashes are found, remove the substring from the second last slash to the end
    if last_slash_index != -1 and second_last_slash_index != -1:
        result_string = string[:second_last_slash_index]

        return result_string
    else:
        # Return the original string if there are less than two slashes
        return string


def get_image_from_element(element, help=0):
    if "Zona" in element:
        match = re.search(r'\d+', element)
        nr = int(match.group())
        title = f'http://127.0.0.1:5001/uploads/zona{nr}.png'
    else:
        if help == 0:
            match = re.search(r'\d+', element)
            nr = int(match.group())
            title = f'http://127.0.0.1:5001/uploads/intersectia{nr}.png'
        else:
            match = re.search(r'\d+', element)
            nr = int(match.group())
            title = f'http://127.0.0.1:5001/uploads/intersectia{nr}-{help}.png'
    return title


@app.route('/tour', methods=['GET', 'POST'])
def tour():
    if request.method == 'GET':
        options = zone_labels.get_labels_from_sparql()
        return render_template('tour.html', options=options, username=Username)
    elif request.method == 'POST':
        selected_options = request.form.getlist('options[]')
        return redirect(url_for('tour_option', options=selected_options, username=Username))


@app.route('/receive-username', methods=['POST'])
def receive_username():
    global Username
    username = request.form.get('username')
    # Do something with the received username
    print(f"Received username on port 5000: {username}")
    Username = username


@app.route('/tour/<options>')
def tour_option(options):
    zone_urls = []
    place_images = []
    # print(options)  # Debugging print
    options = options.replace("'", "")
    options = options.replace("[", "")
    options = options.replace("]", "")
    options_list = options.split(',')  # Split the string into a list based on the assumed separator
    for option in options_list:
        zone_urls.append(f'http://127.0.0.1:5000/zone/{option.strip()}'.replace(" ", "%20"))
    # print(zone_urls)  # Debugging print to check the generated URLs
    start_intersection = "http://127.0.0.1:5000/intersectii/start"
    visited_intersections = set()
    visited_zones = set()
    path = []
    tour_list = search.find_shortest_path(zone_urls, start_intersection, visited_intersections, visited_zones, path)
    # print(tour_list)
    # print(tour_list)

    path_list = []
    for tour in tour_list:
        path_tuples = []
        # print(tour)
        direction = tour[0]
        next_node = tour[1]
        path_tuples.append((extract_last_part(direction), extract_last_part(next_node).replace("%20", " ")))
        path_list.append(path_tuples)

    index = 1
    new_list = []

    for path in path_list:
        pair = path[0]
        if "Zona" in pair[1]:
            if index == 1:
                if pair[0] == "inainte":
                    destination = f'Mergeti inainte pentru a gasi: prima destinatie {pair[1]}'
                    place_images.append(get_image_from_element(pair[1]))
                else:
                    destination = f'Mergeti la {pair[0]} pentru a gasi: prima destinatie {pair[1]}'
                    place_images.append(get_image_from_element(pair[1]))
                index += 1
            else:
                if pair[0] == "inainte":
                    destination = f'Mergeti inainte pentru a gasi: a {index}-a destinatie {pair[1]}'
                    place_images.append(get_image_from_element(pair[1]))
                else:
                    destination = f'Mergeti la {pair[0]} pentru a gasi: a {index}-a destinatie {pair[1]}'
                    place_images.append(get_image_from_element(pair[1]))
                index += 1
        else:
            if pair[0] == "inainte":
                destination = "Mergeti inainte pana la urmatoare intersectie"
                if "8" in pair[1]:
                    if "5" in path_list[len(new_list) - 1][0][1]:
                        place_images.append(get_image_from_element(pair[1], 5))
                    else:
                        place_images.append(get_image_from_element(pair[1], 9))
                elif "9" in pair[1]:
                    if "8" in path_list[len(new_list) - 1][0][1]:
                        place_images.append(get_image_from_element(pair[1], 8))
                    else:
                        place_images.append(get_image_from_element(pair[1], 10))
                elif "10" in pair[1]:
                    if "7" in path_list[len(new_list) - 1][0][1]:
                        place_images.append(get_image_from_element(pair[1], 7))
                    else:
                        place_images.append(get_image_from_element(pair[1], 11))
                else:
                    place_images.append(get_image_from_element(pair[1]))
            else:
                destination = f'Mergeti la {pair[0]} la urmatoare intersectie'
                if "8" in pair[1]:
                    if "5" in path_list[len(new_list) - 1][0][1]:
                        place_images.append(get_image_from_element(pair[1], 5))
                    else:
                        place_images.append(get_image_from_element(pair[1], 9))
                elif "9" in pair[1]:
                    if "8" in path_list[len(new_list) - 1][0][1]:
                        place_images.append(get_image_from_element(pair[1], 8))
                    else:
                        place_images.append(get_image_from_element(pair[1], 10))
                elif "10" in pair[1]:
                    if "7" in path_list[len(new_list) - 1][0][1]:
                        place_images.append(get_image_from_element(pair[1], 7))
                    else:
                        place_images.append(get_image_from_element(pair[1], 11))
                else:
                    place_images.append(get_image_from_element(pair[1]))
        new_list.append(destination)
    # print(place_images)

    return render_template('tour_option.html', places=new_list, images=place_images, username=Username)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
