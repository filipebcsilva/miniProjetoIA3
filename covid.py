import numpy as np
import pandas as pd
from datetime import date,datetime
import seaborn as sns
import matplotlib.pyplot as plt

def transforma_data(string):
    partes = string.split(',')
    anos_str = partes[0]
    anos = anos_str.split()[0]
    return float(anos)  
data_covid = pd.read_csv("MICRODADOS.csv",sep = ';',encoding= "latin1",low_memory= False)
#Cidades com mais de N casos
N = int(input("Insira um número de casos:"))
top_municipios = data_covid["Municipio"].value_counts(sort= True,dropna= True)[data_covid["Municipio"].value_counts() > N]
print(top_municipios)

#Pega duas datas que será usadas durante a execução
day1,month1,year1 = input("Insira uma data:").split("/")
day2,month2,year2 = input("Insira outra data:").split("/")

date1 = datetime(year = int(year1),month= int(month1),day= int(day1))
date2 = datetime(year = int(year2),month= int(month2),day= int(day2))

#As 10 cidades com mais casos entre as datas
data_covid["DataDiagnostico"] = pd.to_datetime(data_covid["DataDiagnostico"])
condition = (data_covid["DataDiagnostico"] >= date1) & (data_covid["DataDiagnostico"] <= date2)
data_filtrada = data_covid[condition]
print(data_filtrada.shape[0] - 1)

top_municipios_data = data_filtrada["Municipio"].value_counts(dropna= True)
print(top_municipios_data.nlargest(10))

#Analisa a porcentagem de internados, mortos e internados que foram a óbito dentro de uma cidade ou no total
municipio = input("Deseja inserir um municipio para analise:")

data_internadas = data_covid[(data_covid["FicouInternado"] == "Sim")  &  (data_covid["Classificacao"] == "Confirmados")]

data_obitos = data_covid[data_covid["DataObito"].notna() & (data_covid["Classificacao"] == "Confirmados")]

data_internado_obito = data_covid[(data_covid["FicouInternado"] == "Sim") & (data_covid["DataObito"].notna())& (data_covid["Classificacao"] == "Confirmados")]

data_confirmados = data_covid[(data_covid["Classificacao"] == "Confirmados")]
if(municipio != ""):
    
    num_internado= data_internadas[(data_covid["Municipio"] == municipio)].shape[0] - 1

    num_obitos = data_obitos[(data_covid["Municipio"] == municipio)].shape[0] - 1

    num_internado_obito = data_internado_obito[(data_covid["Municipio"] == municipio)].shape[0] - 1

    num_total = data_confirmados[(data_covid["Municipio"] == municipio)].shape[0] - 1

    print("Porcentagem de internados em",municipio,(num_internado/num_total) * 100)
    print("Porcentagem de obitos em",municipio,(num_obitos/num_total) * 100)
    print("Porcentagem de internados com obito em",municipio,(num_internado_obito/num_total) * 100)
else:
    num_internado = data_internadas.shape[0] - 1

    num_obitos = data_obitos.shape[0] - 1

    num_internado_obito = data_internado_obito.shape[0] - 1

    num_total = data_confirmados.shape[0] - 1

    print("Porcentagem de internados",(num_internado/num_total) * 100)
    print("Porcentagem de obitos",(num_obitos/num_total) * 100)
    print("Porcentagem de internados com obito",(num_internado_obito/num_total) * 100)

#Analise o numero de obitos entre as datas e calcula a media e desvio padrao das idades
data_obitos_copy = data_obitos.copy()
data_obitos_copy["IdadeNaDataNotificacao"] = data_obitos_copy["IdadeNaDataNotificacao"].apply(transforma_data)
data_obitos_date = data_obitos_copy[(condition)]

print("Média idade de obitos entre as datas = ", data_obitos_date["IdadeNaDataNotificacao"].mean())
print("Desvio padrao de obitos entre as datas = ", data_obitos_date["IdadeNaDataNotificacao"].std())

#Porcetagem de mortos sem comorbidade entre as duas datas
num_mortos_date = data_obitos_date.shape[0] - 1

condition_comobirdade = ((data_obitos_date["ComorbidadePulmao"] == "Não") & (data_obitos_date["ComorbidadeCardio"] == "Não" )
                                        & (data_obitos_date["ComorbidadeRenal"] == "Não") & (data_obitos_date["ComorbidadeDiabetes"] == "Não")
                                        & (data_obitos_date["ComorbidadeTabagismo"] == "Não") & (data_obitos_date["ComorbidadeObesidade"] == "Não"))
num_mortos_sem_comobirdade = data_obitos_date[condition_comobirdade].shape[0] - 1

print("Porcetagem de mortos sem comobirdade:",(num_mortos_sem_comobirdade/num_mortos_date)*100)

casos_por_dia = data_confirmados[data_confirmados["Municipio"] == municipio].groupby("DataNotificacao").size().reset_index(name="TotalCasos")
obitos_por_dia = data_obitos[data_obitos["Municipio"] == municipio].groupby("DataNotificacao").size().reset_index(name="TotalMortos")

casos_por_dia["DataNotificacao"] = pd.to_datetime(casos_por_dia["DataNotificacao"], errors='coerce')
obitos_por_dia["DataNotificacao"] = pd.to_datetime(obitos_por_dia["DataNotificacao"], errors='coerce')

fig, ax1 = plt.subplots(figsize=(14, 6))

sns.lineplot(ax=ax1, data=casos_por_dia, x="DataNotificacao", y="TotalCasos", label="Casos", color="blue")
ax1.set_ylabel("Total de Casos", color="blue")
ax1.tick_params(axis='y', labelcolor="blue")

ax2 = ax1.twinx()
sns.lineplot(ax=ax2, data=obitos_por_dia, x="DataNotificacao", y="TotalMortos", label="Óbitos", color="red")
ax2.set_ylabel("Total de Óbitos", color="red")
ax2.tick_params(axis='y', labelcolor="red")

plt.show()



