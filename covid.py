import numpy as np
import pandas as pd

data_covid = pd.read_csv("MICRODADOS.csv",sep = ';',encoding= "latin1",low_memory= False)

N = int(input("Insira um número de casos:"))
top_municipios = data_covid["Municipio"].value_counts(sort= True,dropna= True)[data_covid["Municipio"].value_counts() > N]
print(top_municipios)
