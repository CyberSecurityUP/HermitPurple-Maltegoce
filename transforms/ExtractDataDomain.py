from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests
from bs4 import BeautifulSoup
import re

class ExtractDataDomain(DiscoverableTransform):
    """
    Transform to extract emails and cryptocurrency wallets from a given domain.
    """

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        domain = request.Value.strip()
        url = f'http://{domain}'  # Assume http for simplicity, consider using https if available
        
        try:
            response_api = requests.get(url)
            soup = BeautifulSoup(response_api.text, 'html.parser')
            
            # Regex patterns
            emails_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            wallets_pattern = r'\b(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|(?:4[0-9a-zA-Z]{96})+|t1[a-zA-Z0-9]{33}|bc1[q,r,p,z][a-z0-9]{39,59}|bitcoincash:q[a-z0-9]{40})\b'
            monero_pattern = r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b'
            
            # Finding data using regex
            emails = re.findall(emails_pattern, response_api.text)
            wallets = re.findall(wallets_pattern, response_api.text)
            wallets.extend(re.findall(monero_pattern, response_api.text))
            
            # Adding email entities
            for email in emails:
                email_entity = response.addEntity('maltego.EmailAddress', email)
            
            # Adding wallet entities
            for wallet in wallets:
                wallet_entity = response.addEntity('maltego.Phrase', wallet)
                wallet_entity.addProperty(fieldName="walletType", displayName="Wallet Type", value="Crypto Wallet")
            
        except Exception as e:
            response.addUIMessage(f'Error retrieving data: {str(e)}', messageType='PartialError')

if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([ExtractDataDomain])

