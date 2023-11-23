import pandas as pd   

dataframe  = pd.read_csv("database/dataframe_final_mundo.csv", low_memory=False)
contagem = dataframe["source_airport_name"].value_counts()
dataframe = dataframe[dataframe['source_airport_name'].map(contagem) == 1].reset_index(drop=True)
print(dataframe["destination_airport_name"].value_counts())
