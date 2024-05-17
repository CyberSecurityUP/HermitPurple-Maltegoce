from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

class SearchMissingPerson(DiscoverableTransform):
    """
    Transform to search for missing persons from desaparecidosdobrasil.org and the FBI based on name.
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        name_to_search = request.Value.strip().lower()
        response.addUIMessage(f"Searching for: {name_to_search}")

        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit search tasks to the executor
            future_desaparecidos = executor.submit(cls.search_desaparecidos, name_to_search, response)
            future_fbi = executor.submit(cls.search_fbi, name_to_search, response)
            
            # Wait for both tasks to complete
            future_desaparecidos.result()
            future_fbi.result()

    @staticmethod
    def search_desaparecidos(name_to_search, response):
        max_id = 300
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

if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([SearchMissingPerson])
                                                     
