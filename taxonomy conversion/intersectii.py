from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_rdf_xml_file(about, stanga, dreapta, inainte, label, filename):
    rdf = Element('rdf:RDF', {
        'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'xmlns:rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'xmlns:ex': 'http://127.0.0.1:5000/intersectii/',
        'xml:base': 'http://127.0.0.1:5000/intersectii/'
    })

    rdfs_Class = SubElement(rdf, 'rdfs:Class', {'rdf:about': 'http://127.0.0.1:5000/zone'})

    description1 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/intersectii'})
    SubElement(description1, 'rdf:type', {'rdf:resource': 'http://www.w3.org/2000/01/rdf-schema#Class'})
    SubElement(description1, 'rdfs:subClassOf', {'rdf:resource': 'http://127.0.0.1:5000/zone'})

    description2 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/intersectii/stanga'})
    SubElement(description2, 'rdf:type', {'rdf:resource': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'})
    SubElement(description2, 'rdfs:domain', {'rdf:resource': 'http://127.0.0.1:5000/intersectii/'})
    SubElement(description2, 'rdfs:range', {'rdf:resource': 'http://127.0.0.1:5000/zone'})

    description3 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/intersectii/dreapta'})
    SubElement(description3, 'rdf:type', {'rdf:resource': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'})
    SubElement(description3, 'rdfs:domain', {'rdf:resource': 'http://127.0.0.1:5000/intersectii/'})
    SubElement(description3, 'rdfs:range', {'rdf:resource': 'http://127.0.0.1:5000/zone'})

    description4 = SubElement(rdf, 'rdf:Description', {'rdf:about': 'http://127.0.0.1:5000/intersectii/inainte'})
    SubElement(description4, 'rdf:type', {'rdf:resource': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'})
    SubElement(description4, 'rdfs:domain', {'rdf:resource': 'http://127.0.0.1:5000/intersectii/'})
    SubElement(description4, 'rdfs:range', {'rdf:resource': 'http://127.0.0.1:5000/zone'})

    intersection = SubElement(rdf, 'ex:Intersection', {'rdf:about': about})
    SubElement(intersection, 'ex:stanga', {'rdf:resource': stanga})
    SubElement(intersection, 'ex:dreapta', {'rdf:resource': dreapta})
    SubElement(intersection, 'ex:inainte', {'rdf:resource': inainte})
    SubElement(intersection, 'rdfs:label').text = label

    # Write the XML to file
    with open(filename, 'w') as f:
        f.write(prettify(rdf))


# Example usage:
# about = 'http://127.0.0.1:5000/intersectii/intersection1'
# stanga = 'http://127.0.0.1:5000/intersectii/stanga1'
# dreapta = 'http://127.0.0.1:5000/intersectii/dreapta1'
# inainte = 'http://127.0.0.1:5000/intersectii/inainte1'
# label = 'Intersection 1'
# filename = 'intersection.rdf'
#
# create_rdf_xml_file(about, stanga, dreapta, inainte, label, filename)
