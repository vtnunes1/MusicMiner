import statistics
import re
import pprint
import csv

import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'notebook'

class Analyse:
    ## Construtor ##
    def __init__(self):
        self.stats1 = ''
        self.stats3 = ''

    def displayData3Stats(self):
        """
        Esta função exibe o conteúdo da variável stats de forma legível.
        """
        
        if not self.stats3:
            print("Nenhuma estatística disponível para exibir.")
            return
        
        pprint.pprint(self.stats3, width=1)

    def analyzeData3Csv(self):
        """
        Esta função realiza análises estatísticas básicas a partir de um arquivo CSV.

        Returns:
            dict: Um dicionário contendo as estatísticas básicas.
        """

        # Definir as colunas que queremos analisar
        columns = {
            '`duration_ms`': [],
            '`acousticness`': [],
            '`danceability`': [],
            '`energy`': [],
            '`instrumentalness`': [],
            '`liveness`': [],
            '`loudness`': [],
            '`speechiness`': [],
            '`tempo`': [],
            '`popularity`': []
        }
        record_count = 0
        
        try:
            with open('data3.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)
                
                for row in csv_reader:
                    record_count += 1
                    for col in columns.keys():
                        if col in headers:
                            index = headers.index(col)
                            value = row[index]
                            if value != 'NULL':
                                columns[col].append(float(value))

        except Exception as e:
            print(f'Erro ao ler o arquivo CSV: {str(e)}')
            return {}
        
        # Calcular estatísticas
        stats = {'record_count': record_count}
        for key, values in columns.items():
            if values:
                stats[key] = {
                    'Média': statistics.mean(values),
                    'Mediana': statistics.median(values),
                    'Desvio Padrão': statistics.stdev(values),
                    'Maior Valor': max(values),
                    'Menor Valor': min(values)
                }
            else:
                stats[key] = 'Não há dados disponíveis'
        
        self.stats3 = stats

    def generateData3Graphs(self):
        """
        Esta função gera gráficos interativos de barras a partir das análises estatísticas fornecidas.
        """
        if not self.stats3:
            print("Nenhuma estatística disponível para gerar gráficos.")
            return

        # Configurar o renderizador do Plotly para exibir gráficos no ambiente correto
        pio.renderers.default = 'jupyterlab'  # Outros renderers: ['notebook', 'notebook_connected', 'colab']

        # Exibir o contador de registros de forma elegante
        record_count = self.stats3.get('record_count', 'Não disponível')

        # Criar uma figura para exibir o total de registros
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0.5], y=[0.5],
            text=[f'Total de registros: {record_count}'],
            mode='text',
            textfont=dict(size=20, color='black')
        ))
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=200,
            title="Informações Gerais"
        )
        fig.show()

        # Preparar dados para os gráficos
        metrics = ['Média', 'Mediana', 'Desvio Padrão', 'Maior Valor', 'Menor Valor']
        for key, values in self.stats3.items():
            if key == 'record_count' or isinstance(values, str):
                continue

            fig = go.Figure(data=[
                go.Bar(
                    x=metrics,
                    y=[values[metric] for metric in metrics],
                    text=[f"{metric}: {values[metric]}" for metric in metrics],
                    textposition='auto',
                    hoverinfo='text'
                )
            ])
            fig.update_layout(
                title=f'Estatísticas para {key}',
                xaxis_title="Métricas",
                yaxis_title=key,
                height=400
            )
            fig.show()





















    def displayData1Stats(self):
        """
        Esta função exibe o conteúdo da variável stats de forma legível.
        """

        if not self.stats1:
            print("Nenhuma estatística disponível para exibir.")
            return

        pprint.pprint(self.stats1, width=1)

    def analyzeData1Csv(self):
        """
        Esta função realiza análises estatísticas básicas a partir de um arquivo CSV.

        Returns:
            dict: Um dicionário contendo as estatísticas básicas.
        """

        # Definir as colunas que queremos analisar
        columns = {
            'followers': [],
            'popularity': []
        }
        record_count = 0
        
        try:
            with open('data1.csv', 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)
                
                for row in csv_reader:
                    record_count += 1
                    for col in columns.keys():
                        if col in headers:
                            index = headers.index(col)
                            value = row[index]
                            if value != 'NULL':
                                columns[col].append(float(value))

        except Exception as e:
            print(f'Erro ao ler o arquivo CSV: {str(e)}')
            return {}

        # Calcular estatísticas
        stats = {'record_count': record_count}
        for key, values in columns.items():
            if values:
                stats[key] = {
                    'Média': statistics.mean(values),
                    'Mediana': statistics.median(values),
                    'Desvio Padrão': statistics.stdev(values),
                    'Maior Valor': max(values),
                    'Menor Valor': min(values)
                }
            else:
                stats[key] = 'Não há dados disponíveis'
        
        self.stats1 = stats

    def generateData1Graphs(self):
        """
        Esta função gera gráficos interativos de barras a partir das análises estatísticas fornecidas.
        """
        if not self.stats1:
            print("Nenhuma estatística disponível para gerar gráficos.")
            return

        # Configurar o renderizador do Plotly para exibir gráficos no ambiente correto
        pio.renderers.default = 'jupyterlab'  # Outros renderers: ['notebook', 'notebook_connected', 'colab']

        # Exibir o contador de registros de forma elegante
        record_count = self.stats1.get('record_count', 'Não disponível')

        # Criar uma figura para exibir o total de registros
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[0.5], y=[0.5],
            text=[f'Total de registros: {record_count}'],
            mode='text',
            textfont=dict(size=20, color='black')
        ))
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=200,
            title="Informações Gerais"
        )
        fig.show()

        # Preparar dados para os gráficos
        metrics = ['Média', 'Mediana', 'Desvio Padrão', 'Maior Valor', 'Menor Valor']
        for key, values in self.stats1.items():
            if key == 'record_count' or isinstance(values, str):
                continue

            fig = go.Figure(data=[
                go.Bar(
                    x=metrics,
                    y=[values[metric] for metric in metrics],
                    text=[f"{metric}: {values[metric]}" for metric in metrics],
                    textposition='auto',
                    hoverinfo='text'
                )
            ])
            fig.update_layout(
                title=f'Estatísticas para {key}',
                xaxis_title="Métricas",
                yaxis_title=key,
                height=400
            )
            fig.show()
