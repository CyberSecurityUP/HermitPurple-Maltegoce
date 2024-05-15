import requests
from bs4 import BeautifulSoup
import re
import socks

def buscar_informacoes(url):
    try:
        # Configuração do proxy para usar com Tor
        proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }
        
        response = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Regex para e-mails e carteiras de criptomoedas, conforme seu script anterior
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', response.text)
        carteiras = re.findall(r'\b(0x[a-fA-F0-9]{40}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|(?:4[0-9a-zA-Z]{96})+|t1[a-zA-Z0-9]{33}|bc1[q,r,p,z][a-z0-9]{39,59}|bitcoincash:q[a-z0-9]{40})\b', 
response.text)
        carteiras_monero = re.findall(r'\b4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}\b', response.text)
        carteiras.extend(carteiras_monero)
        
        for email in emails:
            print('E-mail encontrado:', email)
        
        for carteira in carteiras:
            print('Endereço de carteira encontrado:', carteira)
        
    except Exception as e:
        print('Erro ao buscar informações:', e)

# URLs para testar o script, incluindo URLs .onion
#urls = ['https://unico.io', 'http://lockbit7z3ddvg5vuez2vznt73ljqgwx5tnuqaa2ye7lns742yiv2zyd.onion', 
#'https://www.to.gov.br/igeprev/solicitacoes-por-e-mail/214rd378o6pv', 
#'https://www.saoluis.ma.gov.br/smtt/conteudo/215', 'http://hackersec.com', 'https://shop.wikileaks.org/donate', 
#'https://hrf.org/btc']

urls = ['https://invest4on3fs7i6j3u7oh5plm2xj26xqxre2gj2ddhnpfmyhmj4uokyd.onion/ethereum-core/index18.html']

for url in urls:
    buscar_informacoes(url)

