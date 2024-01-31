import xml.etree.ElementTree as ET
import get_ontology_data


def parse_sparql_response(xml_response):
    # Parse the XML response
    root = ET.fromstring(xml_response)

    # Initialize an empty dictionary to store predicates and their first objects
    predicate_object_dict = {}

    # Iterate through the result elements
    for result in root.findall(
            '{http://www.w3.org/2005/sparql-results#}results/{http://www.w3.org/2005/sparql-results#}result'):
        predicate_uri = None
        object_value = None

        # Extract predicate and object from each result
        for binding in result.findall('{http://www.w3.org/2005/sparql-results#}binding'):
            name = binding.get('name')
            if name == 'predicate':
                predicate_uri = binding.find('{http://www.w3.org/2005/sparql-results#}uri').text
            elif name == 'object':
                object_element = binding.find('{http://www.w3.org/2005/sparql-results#}uri')
                if object_element is None:
                    object_element = binding.find('{http://www.w3.org/2005/sparql-results#}literal')
                object_value = object_element.text

        # Add predicate and its object to the dictionary if it's not already added
        if predicate_uri and object_value and predicate_uri not in predicate_object_dict:
            predicate_object_dict[predicate_uri] = object_value

    return predicate_object_dict


# Example usage:
# parameter_value = 'Mentha'
# result = get_ontology_data.send_sparql_query(parameter_value)
# xml_response = result
#
# parsed_data = parse_sparql_response(xml_response)
# for predicate, obj in parsed_data.items():
#     print(f"Predicate: {predicate}, Object: {obj}")
