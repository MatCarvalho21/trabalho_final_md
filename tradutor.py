import pandas as pd  
import airportsdata

dataframe_01 = pd.read_csv("database\\routes.csv")

dicionario_dos_aeroportos = airportsdata.load('IATA')

lista_de_colunas = ["route_id", "source_airport_icao", "source_airport_name", "source_airport_city", "source_airport_country", "source_airport_elevation", "source_airport_lat", "source_airport_lon",
                    "destination_airport_icao", "destination_airport_name", "destination_airport_city", "destination_airport_country", "destination_airport_elevation", "destination_airport_lat", "destination_airport_lon"]

lista_de_origens = list(dataframe_01[" source airport"])
lista_de_destinos = list(dataframe_01[" destination apirport"])
lista_de_dados = list()


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

dataframe_02 = pd.DataFrame(data=lista_de_dados, columns=lista_de_colunas)
dataframe_01["route_id"] = dataframe_02["route_id"]

dataframe_final = pd.merge(dataframe_01, dataframe_02, on='route_id', how='inner')
dataframe_final_brasil = dataframe_final[dataframe_final["source_airport_country"] == "BR"].reset_index(drop=True)

dataframe_final.to_csv("database\\dataframe_final_mundo.csv")
dataframe_final_brasil.to_csv("database\\dataframe_final_brasil.csv")