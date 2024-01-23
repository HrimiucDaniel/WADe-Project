import requests
from bs4 import BeautifulSoup


def get_distribution_and_habitat(plant_name, section):
    url = f"https://en.wikipedia.org/wiki/{plant_name}"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        distribution_section = soup.find('span', {'id': section})

        if distribution_section:
            distribution_info = ""
            current_tag = distribution_section.find_next()

            while current_tag and current_tag.name not in ['h2', 'h3', 'h4', 'h5', 'h6']:
                distribution_info += str(current_tag)
                current_tag = current_tag.find_next()

            distribution_info = BeautifulSoup(distribution_info, 'html.parser').get_text('\n', strip=True)

            return distribution_info.strip()
        else:
            return "No information found on the section."

    else:
        return f"Failed to retrieve data. Status code: {response.status_code}"


# Example usage
#plant_name = "Liliaceae"
#distribution_and_habitat_info = get_distribution_and_habitat(plant_name, "Distribution_and_habitat")
#print(distribution_and_habitat_info)
