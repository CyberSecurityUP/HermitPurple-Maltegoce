from maltego_trx.maltego import MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests

class ReverseImageSearch(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        image_url = request.Value.strip()  
        
        try:
            result = cls.reverse_image_search(image_url)
            if result['success']:
                response.addUIMessage(f"API Response: {result}")
                
                similar_url = result['data'].get('similarUrl', 'No similar URL found')
                result_text = result['data'].get('resultText', 'No result text found')

                if similar_url != 'No similar URL found':
                    url_entity = response.addEntity('maltego.Website', similar_url)
                phrase_entity = response.addEntity('maltego.Phrase', result_text)
            else:
                response.addUIMessage("No results found.", messageType="Inform")
        except Exception as e:
            response.addUIMessage(str(e), messageType="PartialError")

    @staticmethod
    def reverse_image_search(image_url):
        url = "https://google-reverse-image-api.vercel.app/reverse"
        headers = {"Content-Type": "application/json"}
        payload = {"imageUrl": image_url}

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

if __name__ == "__main__":
    from maltego_trx.server import serve_transform_classes
    serve_transform_classes([ReverseImageSearch])
