from SPARQLWrapper import SPARQLWrapper, JSON
from flask import jsonify

from database import DatabaseHandler, app as base_app

app = base_app


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = DatabaseHandler.get_all_users()
        users_list = []

        for user in users:
            user_info = {
                'username': user.username,
                'password': user.password,
                'email': user.email
            }
            users_list.append(user_info)

        return jsonify({'users': users_list})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/users/<username>', methods=['GET'])
def get_user_by_name(username):
    try:
        user = DatabaseHandler.get_user_by_name(username)
        if user is None:
            return jsonify({'error': 'User not found'}), 404

        user_info = {
            'username': user.username,
            'password': user.password,
            'email': user.email
        }
        return jsonify({'user': user_info})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/exhibitions', methods=['GET'])
def get_all_exhibitions():
    try:
        exhibitions = DatabaseHandler.get_all_exhibitions()
        exhibitions_list = []

        for exhibition in exhibitions:
            exhibition_info = {
                'name': exhibition.name,
                'plant_name': exhibition.plant_name,
                'start_date': exhibition.start_date,
                'end_date': exhibition.end_date,
                'current_seats': exhibition.current_seats,
                'total_seats': exhibition.total_seats
            }
            exhibitions_list.append(exhibition_info)

        return jsonify({'exhibitions': exhibitions_list})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/exhibitions/<name>', methods=['GET'])
def get_exhibition_by_name(name):
    try:
        exhibition = DatabaseHandler.get_exhibition_by_name(name)
        if exhibition is None:
            return jsonify({'error': 'Exhibition not found'}), 404

        exhibition_info = {
            'name': exhibition.name,
            'plant_name': exhibition.plant_name,
            'start_date': exhibition.start_date,
            'end_date': exhibition.end_date,
            'current_seats': exhibition.current_seats,
            'total_seats': exhibition.total_seats
        }
        return jsonify({'exhibition': exhibition_info})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/plants', methods=['GET'])
def get_all_plants():
    endpoint_url = "http://localhost:3030/plants/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?object
    WHERE {
        ?subject rdfs:label ?object.
    }
    """

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_list = []
    for result in results["results"]["bindings"]:
        result_list.append(result["object"]["value"])

    return jsonify({'plants': result_list})


@app.route('/plants/{plant_name}', methods=['GET'])
def get_plant(plant_name):
    endpoint_url = "http://localhost:3030/plants/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject rdfs:label "%s".
        ?subject ?predicate ?object.

    }
    """ % (plant_name)

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_dict = {}
    for result in results["results"]["bindings"]:
        result_dict["subject"] = result["subject"]["value"]
        result_dict["predicate"] = result["predicate"]["value"]
        result_dict["object"] = result["object"]["value"]

    return jsonify(result_dict, 'plant')


@app.route('/zones', methods=['GET'])
def get_all_zones():
    endpoint_url = "http://localhost:3030/zones/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?object
    WHERE {
        ?subject rdfs:label ?object.
    }
    """

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_list = []
    for result in results["results"]["bindings"]:
        result_list.append(result["object"]["value"])

    return jsonify(result_list, 'zones')


@app.route('/zones/<zone_name>', methods=['GET'])
def get_zone(zone_name):
    endpoint_url = "http://localhost:3030/zones/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject rdfs:label "%s".
        ?subject ?predicate ?object.

    }
    """ % (zone_name)

    sparql.setQuery(query)

    # Set the query result format to JSON
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()
    result_dict = {}
    for result in results["results"]["bindings"]:
        result_dict["subject"] = result["subject"]["value"]
        result_dict["predicate"] = result["predicate"]["value"]
        result_dict["object"] = result["object"]["value"]

    return jsonify(result_dict, 'zone')


if __name__ == '__main__':
    app.run(port=5003, debug=True)
