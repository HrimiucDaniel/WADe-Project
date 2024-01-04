from SPARQLWrapper import SPARQLWrapper, JSON


def run_sparql_query(subject):
    endpoint_url = "http://dbpedia.org/sparql"

    # Construct the SPARQL query
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?abstract ?thumbnail ?subdivision ?comment ?label
    WHERE {
      <%s> dbo:abstract ?abstract .
      <%s> dbo:thumbnail ?thumbnail .
      <%s> dbp:subdivision ?subdivision .
      <%s> rdfs:comment ?comment .
      <%s> rdfs:label ?label .
      FILTER (LANG(?abstract) = 'en')
      FILTER (LANG(?comment) = 'en')
      FILTER (LANG(?label) = 'en')
    }
    """ % (subject, subject, subject, subject, subject)

    # Set up the SPARQL endpoint
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and get the results
    results = sparql.query().convert()

    return results


# Example usage:
subject_uri = "https://dbpedia.org/page/Celastrales"  # Replace with your subject URI
results = run_sparql_query(subject_uri)

# Access the results
bindings = results["results"]["bindings"]

# Print the values of the attributes
for result in bindings:
    abstract = result["abstract"]["value"]
    thumbnail = result["thumbnail"]["value"]
    subdivision = result["subdivision"]["value"]
    comment = result["comment"]["value"]
    label = result["label"]["value"]

    print(f"Abstract: {abstract}")
    print(f"Thumbnail: {thumbnail}")
    print(f"Subdivision: {subdivision}")
    print(f"Comment: {comment}")
    print(f"Label: {label}")
