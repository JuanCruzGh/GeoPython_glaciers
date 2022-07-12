# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 17:24:53 2022

@author: Juan Cruz
"""
# Librerías necesaarias

import rasterio
import geopandas as gp
import matplotlib.pyplot as plt
from rasterio.plot import show

#%%
# version modificada de https://gidahatari.com/ih-es/tutorial-para-extraer-informacion-puntual-de-un-raster-con-python-geopandas-y-rasterio
def extract_raster_values_from_points(path_pointData, path_rasterData):
    """
    Esta función muestrea datos de un raster a partir de una capa de puntos
    y genera un geodataframe con los valores muestreados.
    
    Parameters
    ----------
    pointData : Shapefile (puntos)
        Shape de puntos dode vamos a tomar los valores de muestra
    rasterData : Raster
        Raster de donde se va a tomar la información.

    Returns
    -------
    Geodataframe que contiene los puntos de muestreo y los valores extraídos
    del raster.

    """
    #open point shapefile
    pointData = gp.read_file(path_pointData)
    
    #open raster file
    rasterData = rasterio.open(path_rasterData)
    
    #create Geodataframe for export
    df_sample = pointData
    df_sample["value"] = 9999 #9999 is only for check
    
    #show point and raster on a matplotlib plot
    fig, ax = plt.subplots(figsize=(12,12))
    pointData.plot(ax=ax, color='orangered')
    show(rasterData, ax=ax)
    
    #extract point value from raster
    n = 0
    for point in df_sample['geometry']:
        x = point.xy[0][0]
        y = point.xy[1][0]
        row, col = rasterData.index(x,y)
        df_sample["value"][n] = rasterData.read(1)[row,col]
        n = n + 1
    
    return df_sample.set_index('id')
    
#%% parametros de entrada
path_pointData =  r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\sample_points.shp"
path_rasterData =  r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_clasificado_ING.tif"

#%% aplico la funcion
SampleDF = extract_raster_values_from_points(path_pointData, path_rasterData)

#%% exporto resultados ING
# ATENCION! SI SE TRABAJA CON LOS DATOS DE ZELLER CORRER LA CELDA DE ABAJO
# PORQUE ES NECESARIO RECLASIFICAR
Sample_ING = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\MuestreoClasificacion_ING.csv"
SampleDF.to_csv(Sample_ING)

#%% ajuste datos de Zeller
#### ATENCION!!! CORRER ESTA CELDA SOLO EN CASO DE QUE SE TRATE DEL RASTER DE ZELLER #########

# Recordemos que los valores de categorías varían entre Zeller y el ING
# Hielo descubierto:        ING = 1      |       ZELLER = 0, 1 y 5
# Hielo cubierto: ZELLER =  ING = 2      |       ZELLER = 3

SampleDF.loc[SampleDF.value == 0,'value']= 1
SampleDF.loc[SampleDF.value == 1,'value']= 1
SampleDF.loc[SampleDF.value == 5,'value']= 1
SampleDF.loc[SampleDF.value == 3,'value']= 2

#%%
#export para Zeller
Sample_Zeller = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\MuestreoClasificacion_Zeller.csv"
SampleDF.to_csv(Sample_Zeller)