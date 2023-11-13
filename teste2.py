import pandas as pd  
import airportsdata
import numpy as np 

#lendo o dataframe
dataframe_bruto = pd.read_csv("database\\routes.csv")

#carregando dados da biblioteca
dicionario_dos_aeroportos = airportsdata.load('IATA')

#dados que vamos extrai da biblioteca que não existem no dataframe inicial
lista_de_colunas = ["route_id", "source_airport_icao", "source_airport_name", "source_airport_city", "source_airport_country", "source_airport_elevation",
                     "source_airport_lat", "source_airport_lon", "destination_airport_icao", "destination_airport_name", "destination_airport_city", 
                     "destination_airport_country", "destination_airport_elevation", "destination_airport_lat", "destination_airport_lon"]

lista_de_origens = list(dataframe_bruto[" source airport"])
lista_de_destinos = list(dataframe_bruto[" destination apirport"])
lista_de_dados = list()

#extraindo dados da biblioteca
for cada_origem, cada_destino in zip(lista_de_origens, lista_de_destinos):
    try:
        lista_auxiliar = list()
        lista_auxiliar.append(f"{cada_origem}-{cada_destino}")
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["icao"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["name"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["city"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["country"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["elevation"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["lat"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_origem]["lon"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["icao"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["name"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["city"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["country"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["elevation"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["lat"])
        lista_auxiliar.append(dicionario_dos_aeroportos[cada_destino]["lon"])
        lista_de_dados.append(lista_auxiliar)
    except:
        lista_de_dados.append(list())

dataframe_filtrado = pd.DataFrame(data=lista_de_dados, columns=lista_de_colunas)
dataframe_bruto["route_id"] = dataframe_filtrado["route_id"]

#criando o dataframe final
dataframe_final = pd.merge(dataframe_bruto, dataframe_filtrado, on='route_id', how='inner')
dataframe_final = dataframe_final.dropna(thresh=2)
dataframe_final = dataframe_final.groupby("route_id", as_index=False).first().reset_index(drop=True)

#filtrando para aeroportos brasileiros
dataframe_final_brasil = dataframe_final[dataframe_final["source_airport_country"] == "BR"].reset_index(drop=True)

""" TRECHO PARA SALVAR AS NOVAS BASES DE DADOS
dataframe_final.to_csv("database\\dataframe_final_mundo.csv")
dataframe_final_brasil.to_csv("database\\dataframe_final_brasil.csv")
"""

print(dataframe_final.shape)


import math

def cal_dist(lat_inicial:float, lon_inicial:float, lat_final:float, lon_final:float) -> float:
    """
    """
    try:
        dif_lat = math.radians(float(lat_final) - float(lat_inicial))
        dif_lon = math.radians(float(lon_final) - float(lon_inicial))

        raio_terra_km = 6370

        #funções de haversine para distância esférica
        hav_lat = math.sin(dif_lat/2)**2
        hav_lon = math.sin(dif_lon/2)**2

        cos_1 = math.cos(float(math.radians(lat_inicial)))
        cos_2 = math.cos(float(math.radians(lat_final)))

        dist_real = 2*raio_terra_km*math.asin(math.sqrt(hav_lat + cos_1 * cos_2 * hav_lon))

        return round(dist_real, 3)
    
    except:
        return None


def cal_horas(dist_km:float) -> float:
    """
    """
    try:
        velociade_km_h = 850
        tempo_horas = round(float(dist_km)/velociade_km_h, 3)

        return tempo_horas
    
    except:
        return None
    

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

print(dataframe_final.shape)


grafo_com_pesos = dict()

#criando lista com todos os aeroportos
aeroportos_destino = set(dataframe_final[" destination apirport"])
lista_de_aeroportos_unicos = list(set(dataframe_final[" source airport"]).union(aeroportos_destino)) 

#vai iterar sobre cada aeroporto
for cada_aeroporto in lista_de_aeroportos_unicos:
    grafo_com_pesos[cada_aeroporto] = dict()
    dataframe_final_2 = dataframe_final[dataframe_final[" source airport"] == cada_aeroporto]

    #acessando todos destinos e suas distâncias
    lista_de_destinos = list(dataframe_final_2[" destination apirport"])
    lista_de_distancias = list(dataframe_final_2["distancia"])

    #cada destino é uma chave e a distância é o peso
    for cada_destino, cada_distancia in zip(lista_de_destinos, lista_de_distancias):
        grafo_com_pesos[cada_aeroporto][cada_destino] = cada_distancia

#exemplo da estrutura do grafo
print(grafo_com_pesos["BSS"])


def dijkstra(grafo: dict, origem: str | int, destino: str | int) -> tuple:
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

        if len(grafo[vertice_atual]) != 0:
            vizinhos = list(grafo[vertice_atual].keys())
        else:
            break

        print(vertice_atual)

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

print(dijkstra(grafo_com_pesos, "FRA", "STN"))
