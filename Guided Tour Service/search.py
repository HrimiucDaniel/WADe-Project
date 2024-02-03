import get_all_intersections


def extract_last_part(url):
    """
    Extracts the last part of a URL after the last '/' character.
    """
    parts = url.split('/')
    last_part = parts[-1]
    return last_part


def find_shortest_path(input_zones, current_intersection, visited_intersections, visited_zones, path):
    triples = get_all_intersections.retrieve_triples_for_subject(current_intersection)

    visited_intersections.add(current_intersection)
    # print(triples)
    # print("Again")
    # print("")
    # print("")

    for direction, next_node in triples.items():
        # print(extract_last_part(next_node[0]).replace("%20", " "))

        if direction == 'http://www.w3.org/2000/01/rdf-schema#label':
            # print(extract_last_part(next_node[0]).replace("%20", " "))
            continue

        if "zone" in next_node[0] and next_node[0] in input_zones and next_node[0] not in visited_zones:
            # print("Zone --------------------", next_node[0])
            visited_zones.add(next_node[0])
            path.append((direction, next_node[0]))  # Add the zone to the solution
            if len(visited_zones) == len(input_zones):
                return path

    for direction, next_node in triples.items():
        # print(next_node)
        # print("Break")
        if direction == 'http://www.w3.org/2000/01/rdf-schema#label':
            continue

        # If the next node is a zone in the input list and has not been visited

        # If the next node is an intersection and has not been visited
        if "intersectii" in next_node[0] and next_node[0] not in visited_intersections:
            print("Intersectia ", next_node[0])
            new_path = path + [(direction, next_node[0])]
            solution = find_shortest_path(input_zones, next_node[0], visited_intersections, visited_zones, new_path)
            if solution:
                return solution

    return None


# input_zones = [
#     "http://127.0.0.1:5000/zone/Zona%203%20-%20Complexul%20de%20Sere",
#     "http://127.0.0.1:5000/zone/Zona%2010%20-%20Sectia%20Rosarium"
# ]
#
# start_intersection = "http://127.0.0.1:5000/intersectii/start"
# visited_intersections = set()
# visited_zones = set()
# path = []
#
# shortest_path = find_shortest_path(input_zones, start_intersection, visited_intersections, visited_zones, path)
# if shortest_path:
#     print("Shortest Path:")
#     for step in shortest_path:
#         print(step)
# else:
#     print("No path found.")
