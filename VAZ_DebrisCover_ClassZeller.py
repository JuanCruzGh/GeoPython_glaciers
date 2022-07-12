# -*- coding: utf-8 -*-
"""
Created on Tue May 31 16:35:08 2022

@author: Juan Cruz
"""

from osgeo import gdal
import pandas as pd
import os

#%% Parametros
# 1. Cambiar directorio de trabajo (carpeta con img clasificadas)
# 2. Poner direccion de carpeta de destino y pones el nombre del archivo con terminación .csv
# la carpeta de destino es donde se va a guardar la tablita de rresultados

# EJEMPLO: carpeta_destino = r"C:\DebrisCoverGlacier_Scrips\prueba.csv"
carpeta_destino = r"C:\DebrisCoverGlacier_Tesis\data\resultados_revisados\Facies_Zeller_Review_5km2.csv" 

# Directorio relativo donde se alvergan las imágenes clasificadas
carpeta_rasters = "."

#%% Funcion
def facies_Zeller(raster_folder):
    """
    Usa como entrada una carpeta que contiene los raster clasificados 
    en función de la clasf. de Zeller y te devuelve varios datos de área.
    
    IMPORTANTE !! Los nombres de los archivos tif tienen un formato específico
    que esta específicado como "IDImagen-IDlocal.tif"

    Parameters
    ----------
    raster_folder : str
        Los raster tienen que tener este formato de nombre si o si
        Ejemplo: "1_1_1_1_LT05_233083_20100319-G700069O329897S.tif"

    Returns
    -------
    Un dataframe con datos de facies de los cuerpos de hielo. 

    """
    
    # Genero dataframe de base donde voy a ir guardando los resultados
    df_Zeller = pd.DataFrame()

    for root, dirs, files in os.walk(raster_folder): 
         
        for i in files:
            
            # Descarto los archivos que no son .tif
            if i[-4:] != ".tif":
               continue
            
            else:
                rasterpath = i
                # Leo el raster
                dataset = gdal.Open(rasterpath, gdal.GA_ReadOnly)
                # Tomo la banda 1 que es la del clasificador
                classify = dataset.GetRasterBand(1)
                # Transformo el raster a un array
                raster_array = classify.ReadAsArray()
                
                # Genero arrays con los píxeles de cada categoría
                ice = raster_array[raster_array == 0]
                snow = raster_array[raster_array == 1]
                water = raster_array[raster_array == 2]
                debris_cover = raster_array[raster_array == 3]
                clouds = raster_array[raster_array == 4]
                shadow_or_snow = raster_array[raster_array == 5]
                undefined_shadow = raster_array[raster_array == 6]
    
                # Dado que un píxel es de 30x30m, cada valor del array tiene 900m2 o 0.0009 km2
                # Podemos calcular el area que ocupa simplemente con la longitud del array
                #Calculo las áreas; en km2
                area_ice = len(ice)*0.0009
                area_snow = len(snow)*0.0009
                area_water = len(water)*0.0009
                area_dc = len(debris_cover)*0.0009
                area_clouds = len(clouds)*0.0009
                area_sha_or_sn = len(shadow_or_snow)*0.0009
                area_un_sha = len(undefined_shadow)*0.0009
                area_uncovered = area_ice + area_snow + area_sha_or_sn
                area_total = area_ice + area_snow + area_dc + area_water\
                            + area_clouds + area_sha_or_sn +area_un_sha
                ratio_dc_total = area_dc/area_total * 100
                
                # Obtengo el ID local en función de una entrada con estas características si o si
                # EJ: 1_1_1_1_LT05_233083_20100319-G700069O329897S
                id_local = rasterpath[-19:-4]
                
                # Fecha de la imagen
                fecha = rasterpath[-28:-24] + "-" + rasterpath[-24:-22] + "-" + rasterpath[-22:-20]
                
                # Genero un dataFrame para colocar los resultados
                results = pd.DataFrame({"id_local": [id_local],
                           "area_descubierta":[area_uncovered],
                           #"area_nieve":[area_snow],
                           "area_cubierta":[area_dc], 
                           "area_total":[area_total], 
                           "ratio_area_cubierta_total":[ratio_dc_total], 
                           "fecha_imagen": [fecha]})
                
                # Voy concatenando cada resultado en el dataframe de base
                df_Zeller = pd.concat([results, df_Zeller])
    
    return df_Zeller.set_index('id_local') 


#%% Aplico la función
Facies_Zeller = facies_Zeller(carpeta_rasters)

#%% Exporto
# Exporta el dataframe filtrado como csv
Facies_Zeller.to_csv(carpeta_destino)
