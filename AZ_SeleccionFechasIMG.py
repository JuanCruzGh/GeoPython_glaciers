# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:22:25 2022

@author: Juan Cruz
"""

"""
Este algoritmo es para seleccionar desde una base de datos generada por el
algoritmo de Zeller (2020) llamada "Main_patch", una imagen satelital por
glaciar y por año, para los glaciares Vertientes y Horcones Superior (MDZ-ARG).
Las imágenes seleccionadas son las que tinen mayor SLA aproach, que tienen
una cobertura máxima de nieve inferior a 30% y NO pertenecen a la colección L07
Requiere como entrada cada dataframe que se busca filtrar y luego 
devuelve es un unico dataframe con los datos filtrados de cada base de 
datos analizada.
"""

import pandas as pd
import numpy as np

#%%

# Direccion del shapefile que tiene los datos de interes
path_vertientes = r"C:\DebrisCoverGlacier_Tesis\data\seleccion_fechas_img\Main_patch_ING_G694198O329798S.csv"
path_horcones_superior = r"C:\DebrisCoverGlacier_Tesis\data\seleccion_fechas_img\Main_patch_ING_G700681O326355S.csv"

# Import data y lo leo como csv
df_vertientes = pd.read_csv(path_vertientes)
df_horcones_superior = pd.read_csv(path_horcones_superior)

#%%

# Convierto las columnas de fechas de imagenes a date time
# OJO! porque aca tenes que hacer el paso previo de abrir el csv en excel
# y formatear la fecha desde ahí
df_vertientes["date_MSxlsx"] = pd.to_datetime(df_vertientes["date_MSxlsx"])
df_horcones_superior["date_MSxlsx"] = pd.to_datetime(df_horcones_superior["date_MSxlsx"])

#%%
# Genero una nueva columna con los años
df_vertientes["year"] = df_vertientes["date_MSxlsx"].dt.year
df_horcones_superior["year"] = df_horcones_superior["date_MSxlsx"].dt.year

#%%
# Genero una mascara para filtrar landsat7 viendo si los id de las img
mask_L7 = df_vertientes["system:index"].str.contains('LE07', case=False ,regex=True)
mask_L7_HS = df_horcones_superior["system:index"].str.contains('LE07', case=False ,regex=True)

#%%
# Aplico la mascara para filtrar las que no son de Landsat7
df_vertientes_filter_l7 = df_vertientes[mask_L7==False] #52 elementos
df_horcones_superior_filter_l7 = df_horcones_superior[mask_L7_HS==False] #93 elementos

#%%
# Genero mascara para las img cuya cobertura de nieve supera el 30%
mask_sc_v = df_vertientes_filter_l7["Snow Cover Ratio"] <= 0.3
mask_sc_hs = df_horcones_superior_filter_l7["Snow Cover Ratio"] <= 0.3

#%%
# Filtro aquellas imagenes cuya cobertura de nieve supera el 30%
df_v = df_vertientes_filter_l7[mask_sc_v] #31 elementos
df_hs = df_horcones_superior_filter_l7[mask_sc_hs] #68 elementos

#%%
#Genero tabla dinamica para encontrar los valores mínimos de SLA para cada año
pivot_df_v = pd.DataFrame(pd.pivot_table(df_v, values='SLA MP-Approach', 
                            index=["year"],aggfunc=np.max)) #27 años

pivot_df_hs = pd.DataFrame(pd.pivot_table(df_hs, values='SLA MP-Approach', 
                            index=["year"],aggfunc=np.max)) #25 años

#%%
# Genero una lista a partir de los datos de la tabla pivot
# Vertientes
SLA_v = []
for i in range(len(pivot_df_v)): 
    SLA_v.append(pivot_df_v.values[i][0])
    
SLA_year_v = []
for i in range(len(pivot_df_v)): 
    SLA_year_v.append(pivot_df_v.index[i])

#Horcones Superior
SLA_hs = []
for i in range(len(pivot_df_hs)): 
    SLA_hs.append(pivot_df_hs.values[i][0])

SLA_year_hs = []
for i in range(len(pivot_df_hs)): 
    SLA_year_hs.append(pivot_df_hs.index[i])

#%%
# Genero DataFrames que voy a completar
df_v_max_SLA = pd.DataFrame() #Vertientes
df_hs_max_SLA = pd.DataFrame() #Horcones Superior

#%%
# Genero un for para filtrar los datos con los valores menores de SLA y generar 
#el verdadero dataframe que necesito
# Vertientes; 27 años
for i in range(len(SLA_v)):
    df_v_mask = (df_v['SLA MP-Approach'] == SLA_v[i]) & (df_v['year'] == SLA_year_v[i])
    filter_df = df_v[df_v_mask]
    df_v_max_SLA = pd.concat([filter_df, df_v_max_SLA], axis=0)

# Horcones Superior; 25 años
for i in range(len(SLA_hs)):
    df_hs_mask = (df_hs['SLA MP-Approach'] == SLA_hs[i]) & (df_hs['year'] == SLA_year_hs[i])
    filter_df = df_hs[df_hs_mask]
    df_hs_max_SLA = pd.concat([filter_df, df_hs_max_SLA], axis=0)

#%%
# Uno los datasets y seteo el indice
df_join = pd.concat([df_v_max_SLA, df_hs_max_SLA]).set_index("system:index")

#%%
# Exporto
df_join.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\seleccion_fechas_img\Main_patch_seleccion_revisado.csv')