from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class SearchMissingPerson(DiscoverableTransform):
    """
    Transform to search for missing persons from multiple sources based on name.
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        name_to_search = request.Value.strip().lower()
        response.addUIMessage(f"Searching for: {name_to_search}")

        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(cls.search_desaparecidos, name_to_search, response)
            executor.submit(cls.search_fbi, name_to_search, response)
            executor.submit(cls.search_garda, name_to_search, response)

    @staticmethod
    def search_desaparecidos(name_to_search, response):
        max_id = 150
        base_url = "https://desaparecidosdobrasil.org/pesquisa_exibecadastrodesaparecidos.php?edit_id={}"
        for i in range(1, max_id + 1):
            url = base_url.format(i)
            response_api = requests.get(url)
            response.addUIMessage(f"Checking URL: {url} - Status: {response_api.status_code}")

            if response_api.status_code == 200:
                soup = BeautifulSoup(response_api.text, 'html.parser')
                input_name = soup.find('input', {'id': 'txtnome'})
                
                if input_name and input_name.get('value'):
                    full_name = input_name.get('value').strip().lower()
                    if name_to_search in full_name:
                        entity = response.addEntity('maltego.Person', full_name.title())

    @staticmethod
    def search_fbi(name_to_search, response):
        url = "https://www.fbi.gov/wanted/kidnap"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response_api = requests.get(url, headers=headers)
        response.addUIMessage(f"Checking FBI URL: {url} - Status: {response_api.status_code}")

        if response_api.status_code == 200:
            soup = BeautifulSoup(response_api.text, 'html.parser')
            for item in soup.find_all('li', class_="portal-type-person"):
                title = item.find('h3', class_='title')
                if title and name_to_search in title.text.lower():
                    link = title.find('a')['href']
                    entity = response.addEntity('maltego.Website', link)
                    entity.addProperty('URL', 'URL', 'strict', link)

    @staticmethod
    def search_garda(name_to_search, response):
        url = "https://www.garda.ie/en/missing-persons/"
        response_api = requests.get(url)
        response.addUIMessage(f"Checking Garda URL: {url} - Status: {response_api.status_code}")

        if response_api.status_code == 200:
            soup = BeautifulSoup(response_api.text, 'html.parser')
            persons = soup.find_all('li', class_='missing-person')
            
            for person in persons:
                h2_tag = person.find('h2')
                if h2_tag:
                    name = h2_tag.text.strip()
                    if name_to_search in name.lower():
                        person_entity = response.addEntity('maltego.Person', name)

if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([SearchMissingPerson])
