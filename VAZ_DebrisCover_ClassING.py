# -*- coding: utf-8 -*-
"""
Created on Mon May 30 16:30:31 2022

@author: Juan Cruz
"""

import pandas as pd
import seaborn as sns
import numpy as np
import geopandas as gp

#%%
# --------------- IMPORTO ARCHIVOS -------------------#
# Direccion del shapefile que tiene los datos de interes
path_shape_ING = r"C:\DebrisCoverGlacier_Tesis\shapes\ING_CuencaRioMendoza.shp"

# Importo el archivo como un GeoDataFrame
geo_df = gp.GeoDataFrame.from_file(path_shape_ING)

# Convierto el archivo en un DataFrame
df = pd.DataFrame(geo_df)

#%%
# --------------- GENERO Y APLICO FILTROS -------------------#
# Mascara para glaciares cubiertos
mask_gc = df['tipo_geofo'] == "GC"

# Mascara para glaciares cubiertos con glaciares de escombro
mask_gcge = df['tipo_geofo'] == "GCGE"

# Convirto la columnda clas_prima en valores int; porque estaban como str
df['clas_prima'] = df['clas_prima'].astype(int)

# Convierto las columnas de fechas de imagenes a date time
df["img_ba_f"] = pd.to_datetime(df["img_ba_f"])

# Mascara para glaciares de Valle; El valor 5 corresponde a glaciares de Valle
mask_valley = df['clas_prima'] == 5

#%%
# Aplico el filtro de glaciar de valle
gl_valley = df[mask_valley] # 580 filas

# Veo que tipo de geoformas hay dentro y cuantas hay de cada cual
gl_valley['tipo_geofo'].value_counts()

#%%
# Aplico el filtro de glaciares cubiertos y de escombros
gl_gc_valley = gl_valley[gl_valley['tipo_geofo'] == "GC"]
gl_gcge_valley = gl_valley[gl_valley['tipo_geofo'] == "GCGE"]

# Busco los ID unicos de los glaciares cubiertos y cubiertos con escombros
id_gc_valley = pd.Series(gl_gc_valley["id_local"].unique()) #66 elementos
id_gcge_valley = pd.Series( gl_gcge_valley["id_local"].unique()) #79 elementos

#%%
# Concateno los ID para obtener la lista cruda
id_concat = pd.concat([id_gc_valley, id_gcge_valley]) # 145 elementos

# Filtro la serie obtieniendo los únicos valores de ID
id_unique_concat = pd.Series(id_concat.unique()) # 143 elementos

#%%
# Este es el verdadero DataFrame que necesito, esta filtrado correctamente por ID
df_ID_filtro = df[df.id_local.isin(id_unique_concat)] #592 elementos

#%%
# Genero una tabla dinámica con mi bello df_ID_filtro para calcular las areas
# de cada tipo de geoforma; reemplazo los valores NaN con ceros para 
# poder calcular el área total con fillna(0)

table = pd.pivot_table(df_ID_filtro, values='area', index=["id_local"],
                    columns=['tipo_geofo'], aggfunc=np.sum).fillna(0) 

# Calculo el área total para cada glaciar
table["area_total"] = table.sum(axis=1) #143 elementos

#%%
# Filtro para encontrar aquellos glaciares superiores a 5km2
glaciers_5km2 = table[table["area_total"] >= 5] 
# glaciers_5km2.area_total.describe()
# count    16.000000
# mean     11.232238
# std       6.428746
# min       5.124400
# 25%       7.109725
# 50%       7.765450
# 75%      14.917625
# max      28.070200

#%%
# Filtra para encontrar glaciares cuya area total se encuentre entre 2 y 5 km2
glaciers_2_5km2 = table[(table['area_total'] > 2) & (table['area_total'] < 5)]
# glaciers_2_5km2.area_total.describe()
# count    28.000000
# mean      2.838821
# std       0.688501
# min       2.008700
# 25%       2.342425
# 50%       2.607900
# 75%       3.355300
# max       4.768400

#%%
# Filtra para encontrar glaciares cuya area total sea menor a 2 km2
glaciers_2km2 = table[table["area_total"] <= 2] 
#glaciers_2km2.area_total.describe()
# count    99.000000
# mean      0.869445
# std       0.484742
# min       0.119900
# 25%       0.511200
# 50%       0.786800
# 75%       1.266100
# max       1.943900

#%%
# Obtengo una serie con los ID unicos de los glaciares
id_glaciers_5km2 = pd.Series(glaciers_5km2.index) # 16 glaciares

# Obtengo una serie con los ID unicos de los glaciares
id_glaciers_2_5km2 = pd.Series(glaciers_2_5km2.index) #  28 glaciares

# Obtengo una serie con los ID unicos de los glaciares
id_glaciers_2km2 = pd.Series(glaciers_2km2.index) #  99 glaciares

#%%
"""
#--------------------- TOMA DE MUESTRAS ----------------------#
Esto que esta entre comillas lo hago una vez para muestrear lo voy a sileciar 
ahora y leo el csv con la muestra que tome...

# Como hay muchos glaciares menores a 2km2 (99) y entre 5 y 2km2 (28)
# voy a tomar una muestra aleatoria de 10 ID para cada grupo
#sample_id_glaciers_2_5km2 = id_glaciers_2_5km2.sample(n=10, random_state=1) #10 glaciares
#sample_id_glaciers_2km2 = id_glaciers_5km2.sample(n=10, random_state=1) #10 glaciares
"""

# ------------------ IMPORTO DATAFRAME CON MUESTRAS -----------------#
# Import data del muestreo 5 y 2 km2
sample_id_glaciers_2_5km2 = pd.read_csv(r'C:\DebrisCoverGlacier_Tesis\data\ID_dates_2-5km2.csv')
sample_id_glaciers_2_5km2 = pd.Series(sample_id_glaciers_2_5km2["id_local"]) #10 gl

# Import data del muestreo entre 2 km2 o menor
sample_id_glaciers_2km2 =  pd.read_csv(r'C:\DebrisCoverGlacier_Tesis\data\ID_dates_2km2.csv')
sample_id_glaciers_2km2 = pd.Series(sample_id_glaciers_2km2["id_local"]) #10 gl

#%%
# -------------------- FILTRADO FINAL DEL DATAFRAME -----------------#
# Vuelvo al dataframe de base, filtro por los glaciares identificados
# y obtengo el dataframe del ING filtrado por glaciares de valle con 
# algun tipo de cobertura mayores o iguales a 5km2
df_glaciers_5km2 = df[df.id_local.isin(id_glaciers_5km2)] #160 elementos

# hago lo mismo para los glaciares entre 2 y 5 km2
df_glaciers_2_5km2 = df[df.id_local.isin(sample_id_glaciers_2_5km2)] # 44 elementos

# y lo mismo para los menores o iguales a 2 km2
df_glaciers_2km2 = df[df.id_local.isin(sample_id_glaciers_2km2)] # 23 elementos

#%%
# Unicamente para los glaciares menores o iguales a 5 km2 voy a tener que 
# filtrar por las muestras para generar el dataframe de Facies_ING
glaciers_2_5km2_sample = glaciers_2_5km2[glaciers_2_5km2.index.isin(sample_id_glaciers_2_5km2)] # 10 elementos
glaciers_2km2_sample = glaciers_2km2[glaciers_2km2.index.isin(sample_id_glaciers_2km2)] # 10 elementos

#%%
# -------------------- FECHAS DE LAS IMÁGENES ---------------------#
# Genero otra tabla dinámica para extraer el promedio de las fechas de cada imagen
table_date_5km2 = pd.pivot_table(df_glaciers_5km2, values='img_ba_f', 
                            index=["id_local"],aggfunc=np.mean) #16 glaciares

table_date_2_5km2 = pd.pivot_table(df_glaciers_2_5km2, values='img_ba_f', 
                            index=["id_local"],aggfunc=np.mean) #10 gl

table_date_2km2 = pd.pivot_table(df_glaciers_2km2, values='img_ba_f', 
                            index=["id_local"],aggfunc=np.mean) #10 gl

#%%
# ----------------GENERO DATAFRAME DE EXPORTACION -------------#
# Como me interesa comparar coberturas voy a generar un dataframe específico
# para analizar las facies según el mapeo del inventario

Facies_ING_5km2 = pd.DataFrame({"area_descubierta": glaciers_5km2["GD"]+glaciers_5km2["MN"],
                           "area_cubierta": glaciers_5km2["GC"]+glaciers_5km2["GCGE"]+ glaciers_5km2["GEI"]+ glaciers_5km2["GEA"],
                           "area_total":glaciers_5km2["area_total"], 
                           "ratio_area_cubierta_total": ((glaciers_5km2["GC"]+glaciers_5km2["GCGE"]+ glaciers_5km2["GEI"]+ glaciers_5km2["GEA"])/glaciers_5km2["area_total"])*100, 
                           "fecha_imagen": table_date_5km2.img_ba_f })

Facies_ING_2_5km2 = pd.DataFrame({"area_descubierta": glaciers_2_5km2_sample["GD"]+glaciers_2_5km2_sample["MN"],
                           "area_cubierta": glaciers_2_5km2_sample["GC"]+glaciers_2_5km2_sample["GCGE"]+ glaciers_2_5km2_sample["GEI"]+ glaciers_2_5km2_sample["GEA"], 
                           "area_total":glaciers_2_5km2_sample["area_total"], 
                           "ratio_area_cubierta_total": ((glaciers_2_5km2_sample["GC"]+glaciers_2_5km2_sample["GCGE"]+ glaciers_2_5km2_sample["GEI"]+ glaciers_2_5km2_sample["GEA"])/glaciers_2_5km2_sample["area_total"])*100, 
                           "fecha_imagen": table_date_2_5km2.img_ba_f })

Facies_ING_2km2 = pd.DataFrame({"area_descubierta": glaciers_2km2_sample["GD"]+glaciers_2km2_sample["MN"],
                           "area_cubierta": glaciers_2km2_sample["GC"]+glaciers_2km2_sample["GCGE"]+ glaciers_2km2_sample["GEI"]+ glaciers_2km2_sample["GEA"],
                           "area_total":glaciers_2km2_sample["area_total"], 
                           "ratio_area_cubierta_total": ((glaciers_2km2_sample["GC"]+glaciers_2km2_sample["GCGE"]+ glaciers_2km2_sample["GEI"]+ glaciers_2km2_sample["GEA"])/glaciers_2km2_sample["area_total"])*100, 
                           "fecha_imagen": table_date_2km2.img_ba_f })

#%%
#-------------------------- EXPORTACIONES -----------------------------#
# Exporto los dataframes filtrado como csv
Facies_ING_5km2.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\FaciesGlaciar_ING_5km2.csv')
Facies_ING_2_5km2.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\FaciesGlaciar_ING_2_5km2.csv')
Facies_ING_2km2.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\FaciesGlaciar_ING_2km2.csv')

"""
# Solo se hace una vez! Exporto tablas con ID seleccionados y las fechas promedio 
table_date_2_5km2.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\Seleccion_2-5km2.csv') # 2 a 5km2
table_date_2km2.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\Seleccion_2km2.csv') # <2km2
table_date_5km2.to_csv(r'C:\DebrisCoverGlacier_Tesis\data\Seleccion_5km2.csv') # <5km2
"""
#%%
#----------------------------- GRAFICOS --------------------------------#
# Genero un histograma para ver las distribución de las areas totales
# de los glaciares de valle que tienen algun tipo de cobertura
sns.set_theme(style="darkgrid")
sns.histplot(data=table, x="area_total", bins= 50, kde=True)
