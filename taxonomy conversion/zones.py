from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_rdf_xml_file(about, label, plants, description, filename):
    rdf = Element('rdf:RDF', {
        'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'xmlns:rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'xmlns:ex': 'http://127.0.0.1:5000/',
        'xml:base': 'http://127.0.0.1:5000/'
    })

    rdfs_Class = SubElement(rdf, 'rdfs:Class', {'rdf:about': 'http://127.0.0.1:5000/plant'})

    description1 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/zone'})
    SubElement(description1, 'rdf:type', {'rdf:resource': 'http://www.w3.org/2000/01/rdf-schema#Class'})

    description2 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/list_of_plants'})
    SubElement(description2, 'rdf:type', {'rdf:resource': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'})
    SubElement(description2, 'rdfs:domain', {'rdf:resource': 'http://127.0.0.1:5000/zone'})
    SubElement(description2, 'rdfs:range').text = 'List'

    description3 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/description'})
    SubElement(description3, 'rdf:type', {'rdf:resource': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'})
    SubElement(description3, 'rdfs:domain', {'rdf:resource': 'http://127.0.0.1:5000/zone'})
    SubElement(description3, 'rdfs:range').text = 'http://www.w3.org/2001/XMLSchema#string'

    zone = SubElement(rdf, 'ex:Zone', {'rdf:about': about})
    SubElement(zone, 'rdfs:label').text = label

    list_of_plants = SubElement(zone, 'ex:list_of_plants', {'rdf:parseType': 'Resource'})
    for plant in plants:
        SubElement(list_of_plants, 'ex:plant', {'rdf:resource': plant})

    SubElement(zone, 'ex:description').text = description

    # Write the XML to file
    with open(filename, 'w') as f:
        f.write(prettify(rdf))

# Example usage:
# about = 'http://127.0.0.1:5000/zone1'
# label = 'Zone 1'
# plants = ['http://127.0.0.1:5000/plant1', 'http://127.0.0.1:5000/plant2']
# description = 'This is a description of Zone 1'
# filename = 'zone.rdf'
#
# create_rdf_xml_file(about, label, plants, description, filename)
