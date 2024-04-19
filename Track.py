import json # Usado para trabalhar com dados no formato JSON
import re # Usado para trabalhar com manipulação de strings
import io # Usado para leitura e escrita de arquivos
import csv # Usado para leitura e escrita de arquivos CSV

class Track:

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
        # Album
        self.album_id = 'NULL'
        self.album_name = 'NULL'
        self.album_type = 'NULL'
        self.album_total_tracks = 'NULL'
        self.album_release_date = 'NULL'
        self.album_release_date_precision = 'NULL'
        # Artista
        self.artist_id = 'NULL'
        self.artist_name = 'NULL'
        self.artist_popularity = 'NULL'
        self.artist_followers = 'NULL'
        # Música
        self.track_id = 'NULL'
        self.track_name = 'NULL'
        self.track_disc_number = 'NULL'
        self.track_number = 'NULL'
        self.track_popularity = 'NULL'
        self.track_acousticness = 'NULL'
        self.track_danceability = 'NULL'
        self.track_duration_ms = 'NULL'
        self.track_energy = 'NULL'
        self.track_instrumentalness = 'NULL'
        self.track_key = 'NULL'
        self.track_liveness = 'NULL'
        self.track_loudness = 'NULL'
        self.track_mode = 'NULL'
        self.track_speechiness = 'NULL'
        self.track_tempo = 'NULL'
        self.track_time_signature = 'NULL'
        self.track_valence = 'NULL'
        self.track_lang = 'NULL'
        self.track_badwords = 'NULL'
        self.track_lyric = 'NULL'
        self.track_lyric_translate = 'NULL' 

    ## Métodos ##
    def searchSpotifyTrack(self, url):
        """
        Esta função extrai o ID da faixa a partir da URL do Spotify e busca as informações correspondentes.

        Args:
            - url (str): A URL da faixa no formato 'https://open.spotify.com/track/{ID}'.
        """
        
        match = re.search(r'/track/([^/?]+)', url)
        
        if match:
            json_track = self.spotify.getTrack(match.group(1))  # Busca track
            self.jsonDecodeTrack(json_track)
            print(f'[FIM]')
        else:
            print('A URL não corresponde ao padrão esperado.')

        # return null

    def jsonDecodeTrack(self, json_track):
        """
        Esta função decodifica as informações de uma faixa do Spotify a partir de um objeto JSON.
    
        Args:
            - json_track (dict): O objeto JSON contendo informações da faixa.
        """

        # Album
        if 'id' in json_track['album']:
            self.album_id = json_track['album']['id']
        if 'name' in json_track['album']:
            self.album_name = json_track['album']['name']
        if 'album_type' in json_track['album']:
            self.album_type = json_track['album']['album_type']
        if 'total_tracks' in json_track['album']:
            self.album_total_tracks = json_track['album']['total_tracks']
        if 'release_date' in json_track['album']:
            self.album_release_date = json_track['album']['release_date']
        if 'release_date_precision' in json_track['album']:
            self.album_release_date_precision = json_track['album']['release_date_precision']
            
        # Artista
        if 'id' in json_track['artists'][0]:
            self.artist_id = json_track['artists'][0]['id']
        if 'name' in json_track['artists'][0]:
            self.artist_name = json_track['artists'][0]['name']

        
        # Música  
        if 'id' in json_track:
            self.track_id = json_track['id']
        if 'name' in json_track:
            self.track_name = json_track['name']
        if 'popularity' in json_track:
            self.track_popularity = json_track['popularity']
        if 'disc_number' in json_track:
            self.track_disc_number = json_track['disc_number']
        if 'track_number' in json_track:
            self.track_number = json_track['track_number']

        self.searchSpotifyArtist()
        self.searchSpotifyAudioFeature()
        self.searchVagalumeLyric()
        
        specialChars = ["'", "\"", "(", ")", "{", "}", "[", "]", ","]
        for character in specialChars:
            self.track_name = self.track_name.replace(character, "")
            self.artist_name = self.artist_name.replace(character, "")
            self.album_name = self.album_name.replace(character, "")

        print(f'[OK] {self.artist_name}: {self.track_name}')
           
        # return null

    def searchSpotifyArtist(self):
        """
        Esta função busca informações do artista no Spotify para a faixa atual.
        """

        if self.artist_id is not None:
            json_artist = self.spotify.getArtist(self.artist_id)
            self.jsonDecodeArtist(json_artist)
        else:
            print('"artist_id" inválido!')

        # return null

    def jsonDecodeArtist(self, json_artist):
        """
        Esta função decodifica as informações de um artista no Spotify a partir de um objeto JSON.
    
        Args:
            - json_artist (dict): O objeto JSON contendo informações do artista.
        """
        
        if 'popularity' in json_artist:
            self.artist_popularity = json_artist['popularity']
        if 'total' in json_artist['followers']:
            self.artist_followers = json_artist['followers']['total']
        
    def searchSpotifyAudioFeature(self):
        """
        Esta função busca características de áudio no Spotify para a faixa atual.
        """

        if self.track_id is not None:
            json_audio = self.spotify.getAudioFeatures(self.track_id)
            self.jsonDecodeAudioFeature(json_audio)
        else:
            print('"id_track" inválido!')

        # return null
    
    def jsonDecodeAudioFeature(self, json_audio):
        """
        Esta função decodifica as características de áudio de uma faixa do Spotify a partir de um objeto JSON.
    
        Args:
            - json_audio (dict): O objeto JSON contendo informações sobre as características de áudio.
        """
        
        # Música
        if 'acousticness' in json_audio:
            self.track_acousticness = json_audio['acousticness']
        if 'duration_ms' in json_audio:
            self.track_duration_ms = json_audio['duration_ms']
        if 'danceability' in json_audio:
            self.track_danceability = json_audio['danceability']
        if 'duration_ms' in json_audio:
            self.track_duration_ms = json_audio['duration_ms']
        if 'energy' in json_audio:
            self.track_energy = json_audio['energy']
        if 'instrumentalness' in json_audio:
            self.track_instrumentalness = json_audio['instrumentalness']
        if 'key' in json_audio:
            self.track_key = json_audio['key']
        if 'liveness' in json_audio:
            self.track_liveness = json_audio['liveness']
        if 'loudness' in json_audio:
            self.track_loudness = json_audio['loudness']
        if 'mode' in json_audio:
            self.track_mode = json_audio['mode']
        if 'speechiness' in json_audio:
            self.track_speechiness = json_audio['speechiness']
        if 'tempo' in json_audio:
            self.track_tempo = json_audio['tempo'] 
        if 'time_signature' in json_audio:
            self.track_time_signature = json_audio['time_signature'] 
        if 'valence' in json_audio:
            self.track_valence = json_audio['valence']

        # return null

    def searchVagalumeLyric(self):
        """
        Esta função busca letras da música no Vagalume com base no artista e título da faixa.
        """

        if self.artist_name is not None and self.track_name is not None:
            json_lyric = self.vagalume.getLyric(self.artist_name, self.track_name)
            if not ('type' in json_lyric and json_lyric['type'] == 'notfound'):
                self.jsonDecodeLyric(json_lyric)
            
        # return null
        
    def jsonDecodeLyric(self, json_lyric):
        """
        Esta função decodifica as informações da letra de uma música do Vagalume a partir de um objeto JSON.
    
        Args:
            - json_lyric (dict): O objeto JSON contendo informações sobre a letra da música.
        """

        if 'mus' in json_lyric and json_lyric['mus']:
            self.track_lyric = json_lyric['mus'][0]['text']
            self.track_lang = json_lyric['mus'][0]['lang']
            if 'translate' in json_lyric['mus'][0]:
                self.track_lyric_translate = json_lyric['mus'][0]['translate'][0]['text']
            
            self.badwords = json_lyric['badwords']
        
            specialChars = ["'", "\"", "(", ")", "{", "}", "[", "]", ","]
            newLyric = self.track_lyric
            newLyricTranslate = self.track_lyric_translate
        
            for character in specialChars:
                newLyric = newLyric.replace(character, " ")
                newLyricTranslate = newLyricTranslate.replace(character, " ")
        
            self.track_lyric = newLyric
            self.track_lyric_translate = newLyricTranslate
    
        # return null
        
    def createMysqlSyntax(self):
        """
        Esta função gera uma sintaxe SQL para inserir dados de uma faixa na tabela MySQL.
    
        Returns:
            - str: Uma sintaxe SQL para inserção de dados.
        """

        insert_artist = ('INSERT INTO tb_artist (id_artist, name, followers, popularity) VALUES ({}, {}, {}, {}) ON DUPLICATE KEY UPDATE id_artist = {}, name = {}, followers = {}, popularity = {};'.format(
            f'"{self.artist_id}"' if self.artist_id != 'NULL' else self.artist_id,
            f'"{self.artist_name}"' if self.artist_name != 'NULL' else self.artist_name,
            self.artist_followers,
            self.artist_popularity,
            #
            f'"{self.artist_id}"' if self.artist_id != 'NULL' else self.artist_id,
            f'"{self.artist_name}"' if self.artist_name != 'NULL' else self.artist_name,
            int(self.artist_followers) if self.artist_followers and self.artist_followers != 'NULL' else 'NULL',
            int(self.artist_popularity) if self.artist_popularity and self.artist_popularity != 'NULL' else 'NULL',
            )
        )

        self.query_artist += insert_artist

        insert_album = ('INSERT INTO tb_album (id_album, name, type, total_tracks, release_date, release_date_precision) VALUES ({}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE id_album = {}, name = {}, type = {}, total_tracks = {}, release_date = {}, release_date_precision = {};'.format(
            f'"{self.album_id}"' if self.album_id != 'NULL' else self.album_id,
            f'"{self.album_name}"' if self.album_name != 'NULL' else self.album_name,
            f'"{self.album_type}"' if self.album_type != 'NULL' else self.album_type,
            int(self.album_total_tracks) if self.album_total_tracks and self.album_total_tracks != 'NULL' else 'NULL',
            f'"{self.album_release_date}"' if self.album_release_date != 'NULL' else self.album_release_date,
            f'"{self.album_release_date_precision}"' if self.album_release_date_precision != 'NULL' else self.album_release_date_precision,
            #    
            f'"{self.album_id}"' if self.album_id != 'NULL' else self.album_id,
            f'"{self.album_name}"' if self.album_name != 'NULL' else self.album_name,
            f'"{self.album_type}"' if self.album_type != 'NULL' else self.album_type,
            int(self.album_total_tracks) if self.album_total_tracks and self.album_total_tracks != 'NULL' else 'NULL',
            f'"{self.album_release_date}"' if self.album_release_date != 'NULL' else self.album_release_date,
            f'"{self.album_release_date_precision}"' if self.album_release_date_precision != 'NULL' else self.album_release_date_precision,
            )
        )

        self.query_album += insert_album

        insert_track = ('INSERT INTO tb_track (`id_track`, `id_album`, `id_artist`, `name`, `disc_number`, `track_number`, `popularity`,`acousticness`, `danceability`, `duration_ms`, `energy`, `instrumentalness`, `key`, `liveness`, `loudness`, `mode`, `speechiness`, `tempo`, `time_signature`, `valence`, `lang`, `badwords`, `lyric`, `lyric_translate`) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE `id_track` = {}, `id_album` = {}, `id_artist` = {}, `name` = {}, `disc_number` = {}, `track_number` = {}, `popularity` = {}, `acousticness` = {}, `danceability` = {}, `duration_ms` = {}, `energy` = {}, `instrumentalness` = {}, `key` = {}, `liveness` = {}, `loudness` = {}, `mode` = {}, `speechiness` = {}, `tempo` = {}, `time_signature` = {}, `valence` = {}, `lang` = {}, `badwords` = {}, `lyric` = {}, `lyric_translate` = {};'.format(
            f'"{self.track_id}"' if self.track_id != 'NULL' else self.track_id,
            f'"{self.album_id}"' if self.album_id != 'NULL' else self.album_id,
            f'"{self.artist_id}"' if self.artist_id != 'NULL' else self.artist_id,
            f'"{self.track_name}"' if self.track_name != 'NULL' else self.track_name,
            int(self.track_disc_number) if self.track_disc_number and self.track_disc_number != 'NULL' else 'NULL',
            int(self.track_number) if self.track_number and self.track_number != 'NULL' else 'NULL',
            int(self.track_popularity) if self.track_popularity and self.track_popularity != 'NULL' else 'NULL',
            int(self.track_acousticness) if self.track_acousticness and self.track_acousticness != 'NULL' else 'NULL',
            int(self.track_danceability) if self.track_danceability and self.track_danceability != 'NULL' else 'NULL',
            int(self.track_duration_ms) if self.track_duration_ms and self.track_duration_ms != 'NULL' else 'NULL',
            int(self.track_energy) if self.track_energy and self.track_energy != 'NULL' else 'NULL',
            int(self.track_instrumentalness) if self.track_instrumentalness and self.track_instrumentalness != 'NULL' else 'NULL',
            int(self.track_key) if self.track_key and self.track_key != 'NULL' else 'NULL',
            int(self.track_liveness) if self.track_liveness and self.track_liveness != 'NULL' else 'NULL',
            int(self.track_loudness) if self.track_loudness and self.track_loudness != 'NULL' else 'NULL',
            int(self.track_mode) if self.track_mode and self.track_mode != 'NULL' else 'NULL',
            int(self.track_speechiness) if self.track_speechiness and self.track_speechiness != 'NULL' else 'NULL',
            int(self.track_tempo) if self.track_tempo and self.track_tempo != 'NULL' else 'NULL',
            int(self.track_time_signature) if self.track_time_signature and self.track_time_signature != 'NULL' else 'NULL',
            int(self.track_valence) if self.track_valence and self.track_valence != 'NULL' else 'NULL',
            int(self.track_lang) if self.track_lang and self.track_lang != 'NULL' else 'NULL',
            f'"{self.track_badwords}"' if self.track_badwords != 'NULL' else self.track_badwords,
            f'"{self.track_lyric}"' if self.track_lyric != 'NULL' else self.track_lyric,
            f'"{self.track_lyric_translate}"' if self.track_lyric_translate != 'NULL' else self.track_lyric_translate,
            #
            f'"{self.track_id}"' if self.track_id != 'NULL' else self.track_id,
            f'"{self.album_id}"' if self.album_id != 'NULL' else self.album_id,
            f'"{self.artist_id}"' if self.artist_id != 'NULL' else self.artist_id,
            f'"{self.track_name}"' if self.track_name != 'NULL' else self.track_name,
            int(self.track_disc_number) if self.track_disc_number and self.track_disc_number != 'NULL' else 'NULL',
            int(self.track_number) if self.track_number and self.track_number != 'NULL' else 'NULL',
            int(self.track_popularity) if self.track_popularity and self.track_popularity != 'NULL' else 'NULL',
            int(self.track_acousticness) if self.track_acousticness and self.track_acousticness != 'NULL' else 'NULL',
            int(self.track_danceability) if self.track_danceability and self.track_danceability != 'NULL' else 'NULL',
            int(self.track_duration_ms) if self.track_duration_ms and self.track_duration_ms != 'NULL' else 'NULL',
            int(self.track_energy) if self.track_energy and self.track_energy != 'NULL' else 'NULL',
            int(self.track_instrumentalness) if self.track_instrumentalness and self.track_instrumentalness != 'NULL' else 'NULL',
            int(self.track_key) if self.track_key and self.track_key != 'NULL' else 'NULL',
            int(self.track_liveness) if self.track_liveness and self.track_liveness != 'NULL' else 'NULL',
            int(self.track_loudness) if self.track_loudness and self.track_loudness != 'NULL' else 'NULL',
            int(self.track_mode) if self.track_mode and self.track_mode != 'NULL' else 'NULL',
            int(self.track_speechiness) if self.track_speechiness and self.track_speechiness != 'NULL' else 'NULL',
            int(self.track_tempo) if self.track_tempo and self.track_tempo != 'NULL' else 'NULL',
            int(self.track_time_signature) if self.track_time_signature and self.track_time_signature != 'NULL' else 'NULL',
            int(self.track_valence) if self.track_valence and self.track_valence != 'NULL' else 'NULL',
            int(self.track_lang) if self.track_lang and self.track_lang != 'NULL' else 'NULL',
            f'"{self.track_badwords}"' if self.track_badwords != 'NULL' else self.track_badwords,
            f'"{self.track_lyric}"' if self.track_lyric != 'NULL' else self.track_lyric,
            f'"{self.track_lyric_translate}"' if self.track_lyric_translate != 'NULL' else self.track_lyric_translate,
            )
        )

        self.query_track += insert_track
        
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
            print('Arquivo track.sql gerado com sucesso.')
        except Exception as e:
            print(f'Erro ao gerar o arquivo track.sql: {str(e)}')

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

        query_array = [self.query_artist, self.query_album, self.query_track]

        for i, sql_syntax in enumerate(query_array):
            matches = re.findall(r'\((.*?)\)', sql_syntax, re.DOTALL)
            data = []
    
            for match in matches:
                values = match.split(', ') # Dividir os valores usando vírgulas
                values = [v.strip('""') for v in values] # Remove as aspas
                data.append(values) # Adicionar os valores à lista de dados
    
            # Escrever os dados no arquivo CSV
            file_name = f'data_{i + 1}.csv'
            
            try:
                with open(file_name, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerows(data)
        
                print('Arquivo data.csv gerado com sucesso.')
            except Exception as e:
                print(f'Erro ao gerar o arquivo data.csv: {str(e)}')
            
        # return null
