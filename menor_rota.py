from tradutor import dataframe_final
from duracao_das_viagens import cal_dist, cal_horas
import math
import numpy as np


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
dataframe_final["peso"] = max(lista_distancias) + 1

#excluindo linhas, que por algum problema, não foi possível calcular ou a distância, ou o tempo de viagem
dataframe_final = dataframe_final.dropna(thresh=2).reset_index(drop=True)

grafo = dict()
dict_dijskra = dict()

lista_de_aeroportos_unicos = list(set(dataframe_final[" source airport"])) 
for cada_aeroporto in lista_de_aeroportos_unicos:
    grafo[cada_aeroporto] = dict()
    dataframe_final_2 = dataframe_final[dataframe_final[" source airport"] == cada_aeroporto]

    lista_de_destinos = list(dataframe_final_2[" destination apirport"])
    lista_de_distancias = list(dataframe_final_2["distancia"])

    for cada_destino, cada_distancia in zip(lista_de_destinos, lista_de_distancias):
        grafo[cada_aeroporto][cada_destino] = cada_distancia

    dict_dijskra[cada_aeroporto] = dict()
    dict_dijskra[cada_aeroporto]["ORIGEM"] = 0
    dict_dijskra[cada_aeroporto]["PESO"] = max(lista_distancias) + 1

origem = "AAL"
destino = "CGH"

dict_dijskra[origem]["PESO"] = 0

vertice_da_vez = origem
chave = 0
menor_peso = max(lista_distancias) + 1
while True:
    print(vertice_da_vez)
    dicionario_auxiliar = dict()

    lista_de_conexoes = list(grafo[vertice_da_vez].keys())
    lista_pesos = list(grafo[vertice_da_vez].values())

    for cada_conexao, cada_peso in zip(lista_de_conexoes, lista_pesos):

        if cada_peso + dict_dijskra[vertice_da_vez]["PESO"] < dict_dijskra[cada_conexao]["PESO"]:
            dict_dijskra[cada_conexao]["PESO"] = cada_peso + dict_dijskra[vertice_da_vez]["PESO"]
            dicionario_auxiliar[cada_conexao] = cada_peso + dict_dijskra[vertice_da_vez]["PESO"]



    if vertice_da_vez == destino:
        break


def dijkstra(grafo: dict, origem: str | int, destino: str | int) -> tuple(list, int):
    """Recriação do algorítmo de Dijkstra.

    Parameters
    ----------
    grafo : dict
        O grafo com pesos desejado.
    origem : str or int
        o vértice de origem.
    destino : str or int
        o vértice de destino.

    Returns
    -------
    tuple
        uma tupla contendo o menor caminho e a distância do caminho, sendo que cada elemento da lista
        é um vértice do grafo, onde o primeiro é a origem e o último o destino, cada elemento representa
        o próximo vértice do caminho a ser percorrido.
    """
    # Inicializador:
    rotas_pesos = dict()
    for vertice in grafo.keys():
        rotas_pesos[vertice] = np.inf
    rotas_pesos[origem] = 0

    lista_rotas = list()
    visitados = set()
    nao_visitados = set(grafo.keys())
    vertice_atual = origem

    while destino != vertice_atual:
        vizinhos = list(grafo[vertice_atual].keys())

        # Fixando o vértice atual
        visitados.add(vertice_atual)
        if vertice_atual in nao_visitados:
            nao_visitados.remove(vertice_atual)

        # Rotulando vizinhos
        for vizinho in vizinhos:
            peso_vizinho = grafo[vertice_atual][vizinho]
            if rotas_pesos[vizinho] > rotas_pesos[vertice_atual] + peso_vizinho:
                rotas_pesos[vizinho] = rotas_pesos[vertice_atual] + peso_vizinho

            # Criando a lista de rotas para refazer a rota
            if abs(rotas_pesos[vertice_atual] - rotas_pesos[vizinho]) == grafo[vertice_atual][vizinho]:
                menor_rota_atual = [vertice_atual, vizinho, rotas_pesos[vizinho]]
                lista_rotas.append(menor_rota_atual)


        # Escolhendo o novo vértice com o menor peso
        menor_caminho = np.inf

        for cada_vertice in nao_visitados:
            if rotas_pesos[cada_vertice] < menor_caminho:
                menor_caminho = rotas_pesos[cada_vertice]
                novo_vertice_atual = cada_vertice

        vertice_atual = novo_vertice_atual

    # Refazendo o caminho de trás para frente
    lista_rotas.reverse()
    rota_final = [destino]

    while origem != rota_final[-1]:
        vertice_selecionado = rota_final[-1]

        for cada_menor_rota in lista_rotas:
            vertice_1 = cada_menor_rota[0]
            vertice_2 = cada_menor_rota[1]
    
            if vertice_2 == vertice_selecionado:
                if rotas_pesos[vertice_1] == rotas_pesos[vertice_selecionado] - grafo[vertice_1][vertice_2]:
                    rota_final.append(vertice_1)
                    break

    rota_final.reverse()

    return rota_final, rotas_pesos[destino]

