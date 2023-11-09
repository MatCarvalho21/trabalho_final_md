from tradutor import dataframe_final
from duracao_das_viagens import cal_dist, cal_horas
import math

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