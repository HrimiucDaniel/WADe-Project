from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom
from SPARQLWrapper import SPARQLWrapper, JSON
import urllib.parse


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_rdf_xml_file(about, label, abstract, subspecies, habitat, ecology, taxonomy, subClassOf, synonym, rank, same,
                        filename, zone):
    rdf = Element('rdf:RDF', {
        'xmlns:ns1': 'http://www.geneontology.org/formats/oboInOwl#',
        'xmlns:ns2': 'https://dbpedia.org/ontology/',
        'xmlns:ns3': 'https://dbpedia.org/property/',
        'xmlns:ns4': 'http://purl.obolibrary.org/obo/ncbitaxon#',
        'xmlns:ns5': 'https://www.w3.org/2002/07/',
        'xmlns:ns6': 'https://dbpedia.org/page/',
        'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'xmlns:rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
    })

    description = SubElement(rdf, 'rdf:Description', {'rdf:about': about})
    SubElement(description, 'rdfs:label').text = label
    SubElement(description, 'ns2:abstract', {'xml:lang': 'en'}).text = abstract

    subspecies_elem = SubElement(description, 'ns3:subspecies', {'rdf:parseType': 'Resource'})
    for item in subspecies:
        SubElement(subspecies_elem, 'ns3:subspeciesItem').text = item

    SubElement(description, 'ns3:habitat').text = habitat
    SubElement(description, 'ns6:ecology').text = ecology
    SubElement(description, 'ns6:taxonomy').text = taxonomy
    SubElement(description, 'rdf:type', {'rdf:resource': 'http://www.w3.org/2000/01/rdf-schema#Class'})
    SubElement(description, 'rdf:zone').text = zone
    SubElement(description, 'rdfs:subClassOf', {'rdf:resource': subClassOf})
    SubElement(description, 'ns1:hasExactSynonym').text = synonym
    SubElement(description, 'ns4:has_rank', {'rdf:resource': rank})

    same_elem = SubElement(description, 'ns5:owlsameAs', {'rdf:parseType': 'Resource'})
    for item in same:
        SubElement(same_elem, 'ns5:sameAsItem').text = item

    # Write the XML to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(prettify(rdf))


def query_dbpedia_same_as(label):
    # Define the DBpedia SPARQL endpoint
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    # Define the SPARQL query with the input label as a parameter
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?sameAs
    WHERE {
      ?resource rdfs:label ?label .
      FILTER (langMatches(lang(?label), "en")) .
      ?resource owl:sameAs ?sameAs .
      FILTER (isIRI(?sameAs))
      FILTER (?label = "%s"@en)
    }
    """ % label

    # Set the SPARQL query and request JSON results
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the query and process the results
    try:
        results = sparql.query().convert()
        same_as_values = [result['sameAs']['value'] for result in results['results']['bindings']]
        return same_as_values
    except Exception as e:
        print("Error executing SPARQL query:", e)
        return []


# if __name__ == "__main__":
#     label = "Hosta"
#     same_as_values = query_dbpedia_same_as(label)
#     if same_as_values:
#         print("Values from owl:sameAs for label '{}':".format(label))
#         for value in same_as_values:
#             print(value)
#     else:
#         print("No owl:sameAs values found for label '{}'".format(label))
#
#







# Example usage:
# about = 'http://example.com/about'
# label = 'Label'
# abstract = 'Abstract of the entity'
# subspecies = ['Subspecies 1', 'Subspecies 2']
# habitat = 'Habitat of the entity'
# ecology = 'Ecology of the entity'
# taxonomy = 'Taxonomy of the entity'
# subClassOf = 'http://example.com/subClassOf'
# synonym = 'Exact Synonym of the entity'
# rank = 'http://example.com/rank'
# same = ['Same 1', 'Same 2']
# filename = 'entity.rdf'
#
# create_rdf_xml_file(about, label, abstract, subspecies, habitat, ecology, taxonomy, subClassOf, synonym, rank, same,
#                     filename)
