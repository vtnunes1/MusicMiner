import requests # Usado para as requisições das APIs
import json # Usado para trabalhar com dados no formato JSON
import base64 # Usado para decodificar dados em Base64

class SpotifyAPI:

    ## Construtor ##
    def __init__(self, client_id, client_secret):
        """
        Inicializa uma instância da classe.

        Args:
            - client_id (str): O "client id" para autenticação na API do Spotify.
            - client_secret (str): A "secret key" para autenticação na API do Spotify
        """
        
        self.base_token_url = "https://accounts.spotify.com"
        self.base_url = "https://api.spotify.com"
        
        self.base64 = self.encode64(client_id, client_secret)
        self.token = self.getToken(self.base64)
        
    ## Métodos ##
    def encode64(self, client_id, client_secret):
        """
        Esta função concatena o `client_id` e o `client_secret` com ":" e codifica a string resultante em base64.
    
        Args:
            - client_id (str): O identificador do cliente.
            - client_secret (str): O segredo do cliente.
    
        Returns:
            - str: A string codificada em base64 contendo o `client_id` e o `client_secret`.
        """
        
        string = client_id + ":" + client_secret
        string_bytes = string.encode("ascii")
        base64_bytes = base64.b64encode(string_bytes)
        return base64_bytes.decode("ascii")

    def getToken(self, base64_string):
        """
        Esta função obtém o token de autenticação.
    
        Args:
            - base64_string (str): A string codificada em base64 para autenticação.
    
        Returns:
            - dict: A resposta da requisição formato JSON.
    
        Raised:
            - requests.exceptions.RequestException: Uma exceção é levantada se ocorrer um erro na requisição.
        """
        
        headers = {"Authorization": f"Basic {base64_string}", "Content-Type": "application/x-www-form-urlencoded"}
        payload = {"grant_type": "client_credentials"}
        url = self.base_token_url + "/api/token"
        
        try:
            response = requests.request("POST", url = url, headers = headers, data = payload)
        
            if response.status_code == 200:
                return response.json()["access_token"]
            else:
                print(f"Erro na requisição. Código de resposta: {response.status_code}")
                return null
        
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro na requisição: {e}")
            return null

    def getTrack(self, id_track):
        """
        Esta função obtém informações de uma música.

        Args:
            - id_track (str): O identificador de uma música no Spotify.

        Returns:
            - dict: A resposta da requisição formato JSON.

        Raised:
            - requests.exceptions.RequestException: Uma exceção é levantada se ocorrer um erro na requisição.
        """

        headers = {"Authorization": f"Bearer {self.token}"}
        url = self.base_url + "/v1/tracks/" + id_track

        try:
            response = requests.request("GET", url = url, headers = headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição. Código de resposta: {response.status_code}")
                return null

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro na requisição: {e}")
            return null

    def getAudioFeatures(self, id_track):
        """
        Esta função obtém as informações de áudio de uma faixa no Spotify.
    
        Args:
            - id_track (str): O identificador único da faixa no Spotify.
            
        Raised:
            - requests.exceptions.RequestException: Uma exceção é levantada se ocorrer um erro na requisição.
        """
        
        headers = {"Authorization": f"Bearer {self.token}"}
        url = self.base_url + "/v1/audio-features/" + id_track
        
        try:
            response = requests.request("GET", url = url, headers = headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição. Código de resposta: {response.status_code}")
                return null

        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro na requisição: {e}")
            return null

    def getPlaylist(self, id_playlist):
        """
        Esta função obtém informações de uma playlist no Spotify.
    
        Args:
            - id_playlist (str): Identificador único da playlist no Spotify.
    
        Returns:
            - dict: Dados em formato JSON contendo informações da playlist.
            
        Raised:
            - requests.exceptions.RequestException: Uma exceção é levantada se ocorrer um erro na requisição.
        """
        
        headers = {"Authorization": f"Bearer {self.token}"}
        url = self.base_url + "/v1/playlists/" + id_playlist

        try:
            response = requests.request("GET", url = url, headers = headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição. Código de resposta: {response.status_code}")
                return null
            
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro na requisição: {e}")
            return null

    def getArtist(self, id_artist):
        """
        Esta função obtém informações de um artista no Spotify.
    
        Args:
            - id_artist (str): Identificador único do artista no Spotify.
    
        Returns:
            - dict: Dados em formato JSON contendo informações do artista.
            
        Raised:
            - requests.exceptions.RequestException: Uma exceção é levantada se ocorrer um erro na requisição.
        """
        
        headers = {"Authorization": f"Bearer {self.token}"}
        url = self.base_url + "/v1/artists/" + id_artist

        try:
            response = requests.request("GET", url = url, headers = headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Erro na requisição. Código de resposta: {response.status_code}")
                return null
            
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro na requisição: {e}")
            return null
        
    
        
        
        