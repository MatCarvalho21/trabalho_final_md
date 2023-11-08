from tradutor import dataframe_final
from duracao_das_viagens import cal_dist, cal_horas

lista_lat_inicial = list(dataframe_final["source_airport_lat"])
lista_lon_inicial = list(dataframe_final["source_airport_lon"])
lista_lat_final = list(dataframe_final["destination_airport_lat"])
lista_lon_final = list(dataframe_final["destination_airport_lon"])

lista_distancias = list()
lista_tempo_de_viagem = list()
for index in range(0, len(lista_lat_inicial)):

    #extraindo os dados
    lat_inicial = lista_lat_inicial[index]
    lon_inicial = lista_lon_inicial[index]
    lat_final = lista_lat_final[index]
    lon_final = lista_lon_final[index]

    #claculando a distância e o tempo
    dist = cal_dist(lat_inicial, lon_inicial, lat_final, lon_final)
    tempo = cal_horas(dist)

    lista_distancias.append(dist)
    lista_tempo_de_viagem.append(tempo)

#criando as colunas com os novos dados 
dataframe_final["distancia"] = lista_distancias
dataframe_final["tempo_de_viagem"] = lista_tempo_de_viagem

#excluindo linhas, que por algum problema, não foi possível calcular ou a distância, ou o tempo de viagem
dataframe_final = dataframe_final.dropna(thresh=2).reset_index(drop=True)

"""
lista_de_cidades_ordenadas_nao_visitadas = ["Paris", "Rio De Janeiro", "Miami", "Sao Paulo", "Belo Horizonte", "Doha"]

while len(lista_de_cidades_ordenadas_nao_visitadas) > 1:
    cidade_inicial = lista_de_cidades_ordenadas_nao_visitadas[0]
    cidade_final = lista_de_cidades_ordenadas_nao_visitadas[1]
    dataframe_final_2 = dataframe_final[dataframe_final["source_airport_city"] == cidade_inicial]
    dataframe_final_3 = dataframe_final_2[dataframe_final_2["destination_airport_city"] == cidade_final]

    try:
        print(f"A menor distância entre {cidade_inicial} e {cidade_final} é {dataframe_final_3['distancia'].min()} quilômetros e esse voo vai durar {dataframe_final_3['tempo_de_viagem'].min()} horas.")
    except:
        print(f"Não tem voo direto entre {cidade_inicial} e {cidade_final}.")

    lista_de_cidades_ordenadas_nao_visitadas.pop(lista_de_cidades_ordenadas_nao_visitadas.index(cidade_inicial))
"""
grafo = dict()
lista_de_aeroportos_unicos = list(set(dataframe_final[" source airport"])) 
for cada_aeroporto in lista_de_aeroportos_unicos:
    grafo[cada_aeroporto] = dict()
    dataframe_final_2 = dataframe_final[dataframe_final[" source airport"] == cada_aeroporto]

    lista_de_destinos = list(dataframe_final_2[" destination apirport"])
    lista_de_distancias = list(dataframe_final_2["distancia"])

    for cada_destino, cada_distancia in zip(lista_de_destinos, lista_de_distancias):
        grafo[cada_aeroporto][cada_destino] = cada_distancia

import sys

# Função do algoritmo de Dijkstra
def calcular_dijkstra(grafo, origem):
    try:
        # Inicialização das distâncias com infinito, exceto a origem que é zero
        distancias = {v: sys.maxsize for v in grafo}
        distancias[origem] = 0

        # Conjunto de vértices visitados
        visitados = set()

        while visitados != set(distancias):
            # Encontra o vértice não visitado com menor distância atual
            vertice_atual = None
            menor_distancia = sys.maxsize
            for v in grafo:
                if v not in visitados and distancias[v] < menor_distancia:
                    vertice_atual = v
                    menor_distancia = distancias[v]

            # Marca o vértice atual como visitado
            visitados.add(vertice_atual)

            # Atualiza as distâncias dos vértices vizinhos
            for vizinho, peso in grafo[vertice_atual].items():
                if distancias[vertice_atual] + peso < distancias[vizinho]:
                    distancias[vizinho] = distancias[vertice_atual] + peso

        # Retorna as distâncias mais curtas a partir da origem
        return distancias
    except:
        return None

print(grafo["AJU"])
