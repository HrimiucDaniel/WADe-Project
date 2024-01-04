from SPARQLWrapper import SPARQLWrapper, JSON
import json  # Add this line to import the json module

# Set the endpoint URL of your Jena Fuseki server
endpoint_url = "http://localhost:3030/Plants/sparql"  # Replace "dataset-name" with your actual dataset name

# Create a SPARQLWrapper instance and set the endpoint
sparql = SPARQLWrapper(endpoint_url)

# Set the SPARQL query
query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object
    }
    LIMIT 10
"""

sparql.setQuery(query)

# Set the query format to JSON
sparql.setReturnFormat(JSON)

# Execute the query and print the results
response = sparql.query().response
content = response.read().decode('utf-8')

results = json.loads(content)

for result in results["results"]["bindings"]:
    subject = result["subject"]["value"]
    predicate = result["predicate"]["value"]
    obj = result["object"]["value"]
    print(f"Subject: {subject}, Predicate: {predicate}, Object: {obj}")
