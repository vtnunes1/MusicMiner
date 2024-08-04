import json # Usado para trabalhar com dados no formato JSON
import time # Usado para trabalhar com tempo de execução
import re # Usado para trabalhar com manipulação de strings
import io # Usado para leitura e escrita de arquivos
import csv # Usado para leitura e escrita de arquivos CSV

from Track import Track  # Importa classe Track

class Playlist:
    
    ## Construtor ##
    def __init__(self, spotify, vagalume):
        """
        Inicializa uma instância da classe.

        Args:
            - spotify: O objeto da classe Spotify para obter informações de áudio.
            - vagalume: O objeto da classe Vagalume para obter letras de músicas.
        """
        # API
        self.spotify = spotify
        self.vagalume = vagalume
        # Query
        self.query_artist = ''
        self.query_album = ''
        self.query_track = ''
        self.csv_query_artist = ''
        self.csv_query_album = ''
        self.csv_query_track = ''
        # Playlist
        self.id_playlist = ''
        self.playlist = []

    ## Métodos ##  
    def searchSpotifyPlaylist(self, url):
        """
        Esta função extrai o ID da playlist a partir da URL do Spotify e busca as informações correspondentes.
    
        Args:
            - url (str): A URL da faixa no formato 'https://open.spotify.com/playlist/{ID}'.
        """       

        match = re.search(r'/playlist/([^/?]+)', url)
        if match:
            self.id_playlist = match.group(1)
        else:
            return "A URL não corresponde ao padrão esperado."
    
        json_playlist = self.spotify.getPlaylist(self.id_playlist)  # Busca playlist
        self.jsonDecodePlaylist(json_playlist)
        print(f'[FIM]')
        
        # return null

    def jsonDecodePlaylist(self, json_playlist):
        """
        Esta função decodifica as informações de uma playlist do Spotify a partir de um objeto JSON.
    
        Args:
            - json_playlist (dict): O objeto JSON contendo informações da playlist.
        """

        for json_track in json_playlist['tracks']['items']:

            time.sleep(1)

            track = Track(self.spotify, self.vagalume) # Instancia Classe Track
            track.jsonDecodeTrack(json_track['track'])
            self.playlist.append(track) # Adiciona Objeto ao array

        # return null

    def createMysqlSyntax(self): 
        """
        Esta função gera uma sintaxe SQL para inserir dados de uma faixa na tabela MySQL.
    
        Returns:
            - str: Uma sintaxe SQL para inserção de dados.
        """
        
        query = ''
        
        for track in self.playlist:
            track.createMysqlSyntax()
            
            # Query Artist
            insert_artist = "INSERT INTO tb_artist (id_artist, name, followers, popularity) VALUES "
            duplicate_artist = " ON DUPLICATE KEY UPDATE "
            query = track.query_artist.split(insert_artist)
            query = query[1].split(duplicate_artist)
            self.csv_query_artist += query[0]
            self.query_artist += track.query_artist
            
            # Query Album
            insert_album = "INSERT INTO tb_album (id_album, name, type, total_tracks, release_date, release_date_precision) VALUES "
            duplicate_album = " ON DUPLICATE KEY UPDATE "
            query = track.query_album.split(insert_album)
            query = query[1].split(duplicate_album)
            self.csv_query_album += query[0]
            self.query_album += track.query_album
            
            # Query Track
            insert_track = "INSERT INTO tb_track (`id_track`, `id_album`, `id_artist`, `name`, `disc_number`, `track_number`, `popularity`, `acousticness`, `danceability`, `duration_ms`, `energy`, `instrumentalness`, `key`, `liveness`, `loudness`, `mode`, `speechiness`, `tempo`, `time_signature`, `valence`, `lang`, `badwords`, `lyric`, `lyric_translate`) VALUES "
            duplicate_track = " ON DUPLICATE KEY UPDATE "
            query = track.query_track.split(insert_track)
            query = query[1].split(duplicate_track)
            self.csv_query_track += query[0]
            self.query_track += track.query_track
            
        self.csv_query_artist = insert_artist + self.csv_query_artist
        self.csv_query_album = insert_album + self.csv_query_album
        self.csv_query_track = insert_track + self.csv_query_track
        
        # return null

    def createSqlFile(self):
        """
        Esta função gera um arquivo SQL contendo a sintaxe fornecida.
    
        Args:
            - sql_syntax (str): A sintaxe SQL a ser escrita no arquivo.
    
        Returns:
            - str: Uma mensagem indicando o sucesso na geração do arquivo.

        Raises:
            - Exception: Se ocorrer um erro ao escrever a sintaxe no arquivo SQL, uma exceção será levantada.
        """

        sql_syntax = self.query_artist + '\n' + self.query_album + '\n' + self.query_track

        file_name = 'data.sql'
        
        try:
            with open(file_name, 'w') as arquivo_sql:
                arquivo_sql.write(sql_syntax)
            print('Arquivo query.sql gerado com sucesso.')
        except Exception as e:
            print(f'Erro ao gerar o arquivo query.sql: {str(e)}')

        # return null
            

    def createCsvFile(self):
        """
        Esta função cria um arquivo CSV a partir da sintaxe SQL fornecida.

        Args:
            - sql_syntax (str): A sintaxe SQL contendo os dados a serem inseridos no CSV.

        Returns:
            - str: Uma mensagem indicando o sucesso na geração do arquivo.
            
        Raises:
            - Exception: Se ocorrer um erro ao escrever os dados no arquivo CSV, uma exceção será levantada.
        """
        
        query_array = [self.csv_query_artist, self.csv_query_album, self.csv_query_track]

        for i, sql_syntax in enumerate(query_array):
            matches = re.findall(r'\((.*?)\)', sql_syntax, re.DOTALL)
            data = []

            for match in matches:
                values = match.split(', ') # Dividir os valores usando vírgulas
                values = [v.strip('""') for v in values] # Remove as aspas
                data.append(values) # Adicionar os valores à lista de dados

            # Escrever os dados no arquivo CSV

            file_name = f'data{i + 1}.csv'
            
            try:
                with open(file_name, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
    
                print(f'Arquivo data{i + 1}.csv gerado com sucesso.')
            except Exception as e:
                print(f'Erro ao gerar o arquivo data.csv: {str(e)}')
            
        # return null