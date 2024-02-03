import wikipediaapi

def get_plant_taxonomy(plant_name):
    # Specify a proper user-agent string
    user_agent = 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'

    # Create a custom header with the user-agent string
    headers = {'User-Agent': user_agent}

    # Make the Wikipedia API request with the custom headers
    wiki_wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI, headers=headers)

    page = wiki_wiki.page(plant_name)

    if page.exists():
        section_title = "Taxonomy"
        if section_title in page.sections:
            section = page.section_by_title(section_title)
            taxonomy = section.text if section else "Taxonomy information not found."
            return taxonomy
        else:
            return "Taxonomy section not found on the Wikipedia page."
    else:
        return "Wikipedia page not found for the given plant name."

if __name__ == "__main__":
    plant_name = "Euphorbiaceae"
    taxonomy = get_plant_taxonomy(plant_name)
    print("Taxonomy of", plant_name, ":\n", taxonomy)
