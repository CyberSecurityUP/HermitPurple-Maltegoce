from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

class AhmiaDomainExtractor(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        search_term = request.getProperty('text')
        html_content = cls.search_ahmia(search_term)
        unique_domains = cls.parse_results(html_content)
        
        if unique_domains:
            for domain in unique_domains:
                entity = response.addEntity('maltego.Domain', domain)
        else:
            # Se nenhum domínio foi encontrado, adicione uma entidade de "Empty Result".
            entity = response.addEntity('maltego.Phrase', 'No domains found')
            entity.addProperty(fieldName="description", displayName="Description", value="Search returned no results")

    @staticmethod
    def search_ahmia(search_term):
        base_url = "https://ahmia.fi"
        search_url = f"{base_url}/search/?q={search_term}"
        try:
            response = requests.get(search_url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return None

    @staticmethod
    def parse_results(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        domains = set()
        for result in soup.select('h4 > a'):
            if result.get('href'):
                parsed_href = urlparse(result['href'])
                redirect_params = parse_qs(parsed_href.query)
                redirect_url = redirect_params.get('redirect_url', [None])[0]
                if redirect_url:
                    domain = urlparse(unquote(redirect_url)).netloc
                    domains.add(domain)
        return domains