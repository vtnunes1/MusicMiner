import statistics
import re
import pprint
import csv
import plotly.graph_objects as go
import plotly.io as pio

class Analyse:
    ## Construtor ##
    def __init__(self, renderer='jupyterlab'):
        self.data1 = None
        self.data3 = None
        pio.renderers.default = renderer # Outros renderers: 'notebook', 'notebook_connected', 'colab'

    def displayDataStats(self, dataset):
        """
        Esta função exibe o conteúdo de um dataset de forma legível.

        Args:
            dataset (str): O nome do dataset ('data1' ou 'data3').
        """
        
        if dataset not in ['data1', 'data3']:
            print("Dataset inválido. Escolha 'data1' ou 'data3'.")
            return

        data = getattr(self, dataset)
        if not data:
            print("Nenhuma estatística disponível para exibir.")
            return

        pprint.pprint(data, width=1)

    def analyzeDataCsv(self, filename, dataset):
        """
        Esta função realiza análises estatísticas básicas a partir de um arquivo CSV.

        Args:
            filename (str): O nome do arquivo CSV.
            dataset (str): O nome do dataset ('data1' ou 'data3').

        Returns:
            dict: Um dicionário contendo as estatísticas básicas.
        """
        
        columns = {
            'data1': {
                'followers': [],
                'popularity': []
            },
            'data3': {
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
        }

        if dataset not in columns:
            print("Dataset inválido. Escolha 'data1' ou 'data3'.")
            return

        data_columns = columns[dataset]
        record_count = 0

        try:
            with open(filename, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)

                for row in csv_reader:
                    record_count += 1
                    for col in data_columns.keys():
                        if col in headers:
                            index = headers.index(col)
                            value = row[index]
                            if value != 'NULL':
                                data_columns[col].append(float(value))

        except Exception as e:
            print(f'Erro ao ler o arquivo CSV: {str(e)}')
            return

        stats = {'record_count': record_count}
        for key, values in data_columns.items():
            if values:
                stats[key] = {
                    'values': values,
                    'Média': statistics.mean(values),
                    'Mediana': statistics.median(values),
                    'Desvio Padrão': statistics.stdev(values),
                    'Maior Valor': max(values),
                    'Menor Valor': min(values)
                }
            else:
                stats[key] = 'Não há dados disponíveis'

        setattr(self, dataset, stats)

    def generateDataGraphs(self, dataset):
        """
        Esta função gera gráficos interativos de barras a partir das análises estatísticas fornecidas.

        Args:
            dataset (str): O nome do dataset ('data1' ou 'data3').
        """
        
        if dataset not in ['data1', 'data3']:
            print("Dataset inválido. Escolha 'data1' ou 'data3'.")
            return

        data = getattr(self, dataset)
        if not data:
            print("Nenhuma estatística disponível para gerar gráficos.")
            return

        pio.renderers.default = 'jupyterlab'

        record_count = data.get('record_count', 'Não disponível')

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

        metrics = ['Média', 'Mediana', 'Desvio Padrão', 'Maior Valor', 'Menor Valor']
        for key, values in data.items():
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

    def generateBoxPlot(self, column_name, dataset):
        """
        Esta função gera um gráfico Box Plot para a coluna especificada.

        Args:
            column_name (str): O nome da coluna para a qual o Box Plot será gerado.
            dataset (str): O nome do dataset ('data1' ou 'data3').
        """
        
        if dataset not in ['data1', 'data3']:
            print("Dataset inválido. Escolha 'data1' ou 'data3'.")
            return

        data = getattr(self, dataset)
        if not data:
            print("Nenhuma estatística disponível para gerar gráficos.")
            return

        if column_name not in data or isinstance(data[column_name], str):
            print(f"Coluna {column_name} não encontrada ou não possui dados disponíveis.")
            return

        values = data[column_name]['values']
        fig = go.Figure()
        fig.add_trace(go.Box(y=values, name=column_name))
        fig.update_layout(
            title=f'Box Plot para {column_name}',
            yaxis_title=column_name
        )
        fig.show()
