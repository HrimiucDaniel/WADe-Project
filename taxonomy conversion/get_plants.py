import xml.etree.ElementTree as ET
import os
import plants
from googletrans import Translator


def translate_to_romanian(text):
    translator = Translator()
    translated = translator.translate(text, src='en', dest='ro')
    return translated.text


def process_xml_files_in_directory(directory_path):
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    # Get a list of XML files in the directory
    xml_files = [f for f in os.listdir(directory_path) if f.endswith('.xml')]

    # Process each XML file
    for xml_file in xml_files:
        file_path = os.path.join(directory_path, xml_file)
        rdf_data = read_rdf_xml_file(file_path)
        about = rdf_data["about"] if rdf_data["about"] is not None else []
        label = rdf_data["label"] if rdf_data["label"] is not None else []
        abstract = rdf_data["abstract"] if rdf_data["abstract"] is not None else ""
        if abstract != "" and abstract is not None:
            abstract = abstract.replace("\n", " ")
            abstract = abstract.replace("  ", " ")
            abstract = abstract.replace(" .", ".")
            abstract = abstract.replace(" ,", ",")
            abstract = abstract.replace(".", ". ")
            abstract = abstract.replace(",", ", ")
            abstract = translate_to_romanian(str(abstract))
        subspecies = rdf_data["subspecies"] if rdf_data["subspecies"] is not None else []
        if subspecies is not None:
            subspecies_url = [f"https://dbpedia.org/page/{sub.lstrip()}" for sub in subspecies]
        else:
            subspecies_url = None
        habitat = rdf_data["habitat"] if rdf_data["habitat"] is not None else ""
        if habitat != "" and habitat is not None:
            #print("Hab", habitat.replace("\n", ""))
            habitat = habitat.replace("\n", " ")
            habitat = habitat.replace("  ", " ")
            habitat = habitat.replace(" .", ".")
            habitat = habitat.replace(" ,", ",")
            habitat = habitat.replace(".", ". ")
            habitat = habitat.replace(",", ", ")
            habitat = translate_to_romanian(str(habitat.replace("\n", " ")))

        ecology = rdf_data["ecology"] if rdf_data["ecology"] is not None else ""
        if ecology != "" and ecology is not None:
            ecology = ecology.replace("\n", " ")
            ecology = ecology.replace("  ", " ")
            ecology = ecology.replace(" .", ".")
            ecology = ecology.replace(" ,", ",")
            ecology = ecology.replace(".", ". ")
            ecology = ecology.replace(",", ", ")
            ecology = translate_to_romanian(str(ecology.replace("\n", " ")))

        taxonomy = rdf_data["taxonomy"] if rdf_data["taxonomy"] is not None else ""
        if taxonomy != "" and taxonomy is not None:
            print(label)
            taxonomy = taxonomy.replace("\n", " ")
            taxonomy = taxonomy.replace("  ", " ")
            taxonomy = taxonomy.replace(" .", ".")
            taxonomy = taxonomy.replace(" ,", ",")
            taxonomy = taxonomy.replace(".", ". ")
            taxonomy = taxonomy.replace(",", ", ")
            print(taxonomy)
            taxonomy = translate_to_romanian(str(taxonomy))
        subClassOf = rdf_data["subClassOf"] if rdf_data["subClassOf"] is not None else []
        synonym = rdf_data["synonym"] if rdf_data["synonym"] is not None else []
        rank = rdf_data["rank"] if rdf_data["rank"] is not None else []
        same = rdf_data["same"] if rdf_data["same"] is not None else []
        zone = rdf_data["zone"] if rdf_data["zone"] is not None else []
        filename = f'D:/WAD3/WADe-Project/apache jena/taxonomy/Zona 10 - Sectia Rosarium/{label}.rdf'

        plants.create_rdf_xml_file(about, label, abstract, subspecies_url, habitat, ecology, taxonomy, subClassOf,
                                   synonym, rank,
                                   same,
                                   filename, zone)


def read_rdf_xml_file(file_path):
    data_dict = {}

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Namespace mappings
    namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'ns1': 'http://www.geneontology.org/formats/oboInOwl#',
        'ns2': 'https://dbpedia.org/property/',
        'ns3': 'https://www.w3.org/2002/07/',
        'ns4': 'http://purl.obolibrary.org/obo/ncbitaxon#',
        'ns5': 'https://dbpedia.org/ontology/'
    }

    # Find the rdf:Description element
    description_elem = root.find('.//rdf:Description', namespaces)

    # Extract data from elements
    data_dict['about'] = description_elem.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')

    label_elem = description_elem.find('rdfs:label', namespaces)
    data_dict['label'] = label_elem.text.strip() if label_elem is not None else ''

    abstract_elem = description_elem.find('ns5:abstract', namespaces)
    data_dict['abstract'] = abstract_elem.text.strip() if abstract_elem is not None else ''

    subspecies_elem = description_elem.find('ns2:subspecies', namespaces)
    data_dict['subspecies'] = eval(subspecies_elem.text.strip()) if subspecies_elem is not None else []

    habitat_elem = description_elem.find('ns2:habitat', namespaces)
    data_dict['habitat'] = habitat_elem.text.strip() if habitat_elem is not None else ''

    ecology_elem = description_elem.find('ns2:ecology', namespaces)
    data_dict['ecology'] = ecology_elem.text.strip() if ecology_elem is not None else ''

    taxonomy_elem = description_elem.find('ns2:taxonomy', namespaces)
    data_dict['taxonomy'] = taxonomy_elem.text.strip() if taxonomy_elem is not None else ''

    zone_elem = description_elem.find('rdf:zone', namespaces)
    data_dict['zone'] = zone_elem.text.strip() if zone_elem is not None else ''

    type_elem = description_elem.find('rdf:type', namespaces)
    data_dict['type'] = type_elem.text.strip() if type_elem is not None else ''

    subclassof_elem = description_elem.find('rdfs:subClassOf', namespaces)
    data_dict['subClassOf'] = subclassof_elem.text.strip() if subclassof_elem is not None else ''

    synonym_elem = description_elem.find('ns1:hasExactSynonym', namespaces)
    data_dict['synonym'] = synonym_elem.text.strip() if synonym_elem is not None else ''

    rank_elem = description_elem.find('ns4:has_rank', namespaces)
    data_dict['rank'] = rank_elem.text.strip() if rank_elem is not None else ''

    same_elem = description_elem.find('ns3:owlsameAs', namespaces)
    data_dict['same'] = eval(same_elem.text.strip()) if same_elem is not None else []

    # same_elem = description_elem.find('rdf:zone', namespaces)
    #  data_dict['zone'] = eval(same_elem.text.strip()) if same_elem is not None else []

    return data_dict


# Example usage:
directory_path = 'D:/WAD3/WADe-Project/apache jena/ontology/Zona 10 - Sectia Rosarium'
process_xml_files_in_directory(directory_path)
