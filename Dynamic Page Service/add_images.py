import requests


def add_images_to_plant(plant_uri, image_urls):
    # Fuseki server details
    fuseki_endpoint = "http://localhost:3030/plants/update"

    # Define a namespace prefix for your property URI
    prefix = """
    PREFIX prop: <https://dbpedia.org/property/>
    """

    # Constructing a SPARQL Update query for each image
    queries = []
    for image_url in image_urls:
        query = f"""
        {prefix}
        INSERT DATA {{
            <{plant_uri}> prop:images <{image_url}> .
        }}
        """
        print(f"Constructed Query: {query}")
        queries.append(query)

    # Sending the SPARQL Update queries to the Fuseki server using PATCH method
    headers = {'Content-Type': 'application/sparql-update'}
    for query in queries:
        response = requests.post(fuseki_endpoint, data=query, headers=headers)

        # Checking the response status for each query
        if response.status_code == 200:
            print(f"Image added successfully for {plant_uri}")
        else:
            print(f"Failed to add image for {plant_uri}. Status code: {response.status_code}")
            print(response.text)