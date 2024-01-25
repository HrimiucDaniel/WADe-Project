import requests

def add_comments_to_plant(plant_uri, comments):
    # Fuseki server details
    fuseki_endpoint = "http://localhost:3030/Plants/update"

    # Constructing a SPARQL Update query for each comment
    queries = []
    for comment in comments:
        query = f"""
        INSERT DATA {{
            <{plant_uri}> <https://dbpedia.org/property/comments> "{comment}" .
        }}
        """
        queries.append(query)

    # Sending the SPARQL Update queries to the Fuseki server using PATCH method
    headers = {'Content-Type': 'application/sparql-update'}
    for query in queries:
        response = requests.post(fuseki_endpoint, data=query, headers=headers)

        # Checking the response status for each query
        if response.status_code == 200:
            print(f"Comment added successfully for {plant_uri}")
        else:
            print(f"Failed to add comment for {plant_uri}. Status code: {response.status_code}")
            print(response.text)


