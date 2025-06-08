import numpy as np
import pandas as pd
from datetime import date,datetime

data_covid = pd.read_csv("MICRODADOS.csv",sep = ';',encoding= "latin1",low_memory= False)

N = int(input("Insira um número de casos:"))
top_municipios = data_covid["Municipio"].value_counts(sort= True,dropna= True)[data_covid["Municipio"].value_counts() > N]
print(top_municipios)

day1,month1,year1 = input("Insira uma data:").split("/")
day2,month2,year2 = input("Insira outra data:").split("/")

date1 = datetime(year = int(year1),month= int(month1),day= int(day1))
date2 = datetime(year = int(year2),month= int(month2),day= int(day2))

data_covid["DataDiagnostico"] = pd.to_datetime(data_covid["DataDiagnostico"])
condition = (data_covid["DataDiagnostico"] >= date1) & (data_covid["DataDiagnostico"] <= date2)
data_filtrada = data_covid[condition]
print(data_filtrada.shape[0])

top_municipios_data = data_filtrada["Municipio"].value_counts(dropna= True)
print(top_municipios_data.nlargest(10))


