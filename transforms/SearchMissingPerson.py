from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests
from bs4 import BeautifulSoup

class SearchMissingPerson(DiscoverableTransform):
    """
    Transform to search for missing persons from desaparecidosdobrasil.org based on name.
    Includes full name, location of disappearance, and optionally, the police report number.
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        name_to_search = request.Value.strip().lower()  # Ensure case insensitivity and strip extra spaces
        response.addUIMessage(f"Searching for: {name_to_search}")
        max_id = 350
        
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
                    response.addUIMessage(f"Found Name: {full_name}")

                    if name_to_search in full_name:
                        response.addUIMessage("Match found, adding entity...")
                        entity = response.addEntity('maltego.Person', full_name.title())

                        local_desaparecimento = soup.find('input', {'id': 'txtlocaldesaparecimento'})
                        if local_desaparecimento and local_desaparecimento.get('value'):
                            entity.addProperty('disappearanceLocation', 'Local Desaparecimento', 'loose', local_desaparecimento.get('value'))
                        
                        # Collect and add the police report number if available
                        boletim_ocorrencia = soup.find('input', {'id': 'txtboletimocorrencia'})
                        if boletim_ocorrencia and boletim_ocorrencia.get('value'):
                            boletim_number = boletim_ocorrencia.get('value').strip()
                            response.addEntity('maltego.Phrase', boletim_number)
                            response.addUIMessage(f"Police Report Number: {boletim_number}")

if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([SearchMissingPerson])

