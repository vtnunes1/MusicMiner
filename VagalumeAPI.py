import requests # Usado para as requisições das APIs
import json # Usado para trabalhar com dados no formato JSON
import urllib.parse # Usado para manipulação de URLs

class VagalumeAPI:

    ## Construtor ##
    def __init__(self, secrete_key):
        """
        Inicializa uma instância da classe.

        Args:
            secrete_key (str): A "secret key" para acessar a API do Vagalume.
        """
        
        self.secrete_key = secrete_key
        
    ## Métodos ##    
    def getLyric(self, artist, title):
        """
        Esta função busca informações de uma música.

        Args:
            - artist (str): Nome do artista.
            - track (str): Nome da música.

        Returns:
            - dict: Um JSON contendo informações da música.

        Raised:
            - requests.exceptions.RequestException: Uma exceção é levantada se ocorrer um erro na requisição.
        """
        
        encoded_track = urllib.parse.quote(title)
        
        artist_name = artist.split(', ')[0]
        main_artist = artist_name.replace(' ','-')
        encoded_artist = urllib.parse.quote(main_artist)
        
        url = f"https://api.vagalume.com.br/search.php?art={encoded_artist}&mus={encoded_track}&apikey={self.secrete_key}"
        
        try:
            response = requests.request("GET", url = url)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição. Código de resposta: {response.status_code}")
                # return null
                
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro na requisição: {e}")
            # return null
    