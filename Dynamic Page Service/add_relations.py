import requests


def add_relation_to_plant(plant_uri, predicate, value, zone_name):
    # Fuseki server details
    fuseki_endpoint = "http://localhost:3030/Plants/update"
    predicate = f'http://127.0.0.1:5000/relations/{predicate}'
    if "Zona" in value:
        value = f'http://127.0.0.1:5000/zone/{value}'
    else:
        value = f'http://127.0.0.1:5000/zone/{zone_name}/plant/{value}'
    value = value.replace(" ", "%20")
    query = f"""
    INSERT DATA {{
        <{plant_uri}> <{predicate}> <{value}>.
    }}
    """

    print(query)

    headers = {'Content-Type': 'application/sparql-update'}
    response = requests.post(fuseki_endpoint, data=query, headers=headers)

    if response.status_code == 200:
        print(f"Relation added successfully for {plant_uri}")
    else:
        print(f"Failed to add relation for {plant_uri}. Status code: {response.status_code}")
        print(response.text)
