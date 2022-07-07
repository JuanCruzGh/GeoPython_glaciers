#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Este script descarga todas las imágenes disponibles de la colección LandSat
recortadas por un área (o poligono) determinada (filtradas por fecha y 
cobertura de nubes) en un directorio local definido por el usuario. Las 
imágenes se descargan por carpeta y por satélite.

"""

import ee
import geemap

#%% Parametros de entrada

ee.Initialize() #inicializa GEE

# Poligono que cubre el area de estudio
# Area de trabajo del glaciar Alerce
polygon = ee.Geometry.Polygon([[[-71.8490039271704,-41.177144340768784], 
                                [-71.80832018083251,-41.177144340768784], 
                                [-71.80832018083251,-41.15375393907278], 
                                [-71.8490039271704,-41.15375393907278]]])

# Punto dentro del área de estudio
loc = ee.Geometry.Point(-71.83, -41.16)
"""
# Poligono que cubre el area de estudio
# Area de trabajo del glaciar Horcones superior
polygon = ee.Geometry.Polygon([[[-70.09736644223858,-32.65847778166258], 
                                [-70.0214921136253,-32.65847778166258], 
                                [-70.0214921136253,-32.61120657583253], 
                                [-70.09736644223858,-32.61120657583253]]])

# Punto dentro del área de estudio
loc = ee.Geometry.Point(-70.06, -32.63)


# Poligono que cubre el area de estudio
# Area de trabajo del glaciar Vertientes
polygon = ee.Geometry.Polygon([[[-69.44654541157472,-33.012651169991884], 
                                [-69.34492187641847,-33.012651169991884], 
                                [-69.34492187641847,-32.9536132811465], 
                                [-69.44654541157472,-32.9536132811465]]])

# Punto dentro del área de estudio
loc = ee.Geometry.Point(-69.40, -32.98)
"""

# Ventana de años; sintaxis [año inicial, año final, parámetro de funcion]
year = [2015, 2020, "year"]

# Ventana de meses; sintaxis [mes inicial, mes final, parámetro de funcion]
month = [3, 4, "month"]

# Cloud-cover es la cobertura máxima de nubes que vamos a seleccionar
CC = 30

# Direccion donde guardo en las imágenes
path = 'C:/DebrisCoverGlacier_Scrips/Pruebas/'
path = path + str(year[0]) + "-" + str(year[1]) +"/"
          
#%% Funcion
def descarga_masiva(polygon, loc, path, year, month, CC):
    """
    Parameters
    ----------
    polygon : ee.Geometry.Polygon
        Polígono que abarca el área de estudio.
    loc : ee.Geometry.Point
        Punto que está dentro del área de estudio (aproximadamente en el centro).
    path : string
        Dirección donde se guardan las imágenes descargadas.
    years : list
        Ventana de años de trabajo.
    month : list
        Ventana de meses de trabajo.
    CC : INT
        Cloud-cover es la cobertura máxima de nubes que vamos a seleccionar

    Returns:
    Devuelve una serie de imágenes de las colecciones Landsat 5, 7 y 8
    TOA1 (OLI y RAW SCENES) y Sentinel 2, filtrando por la ventana temporal 
    y espacial de trabajo
    
    Nota: En este caso se busca en la colección Landsat Surface Relectance (SR)
    y descarga las imágenes con falso color (5,4,3)

    """
    
    ee.Initialize() #inicializa GEE

    # Coleccion Landsat9
    col_landsat9 = ee.ImageCollection("LANDSAT/LC09/C02/T1_L2")\
                                .filterBounds(polygon)\
                                .filterBounds(loc)\
                                .filter(ee.Filter.lt('CLOUD_COVER',CC))\
                                .select(['SR_B5', 'SR_B4', 'SR_B3'])  
    
    #Filtro la colección por las fechas de interés
    Landsat9 = col_landsat9.filter(ee.Filter.calendarRange(year[0], year[1], year[2]))\
                            .filter(ee.Filter.calendarRange(month[0], month[1], month[2]))

    # Coleccion Landsat8
    col_landsat8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")\
                                .filterBounds(polygon)\
                                .filterBounds(loc)\
                                .filter(ee.Filter.lt('CLOUD_COVER',CC))\
                                .select(['SR_B5', 'SR_B4', 'SR_B3'])  
    
    #Filtro la colección por las fechas de interés
    Landsat8 = col_landsat8.filter(ee.Filter.calendarRange(year[0], year[1], year[2]))\
                            .filter(ee.Filter.calendarRange(month[0], month[1], month[2]))
                        
                                         
    # Coleccion Landsat7
    col_landsat7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2")\
                                        .filterBounds(polygon)\
                                        .filterBounds(loc)\
                                        .filter(ee.Filter.lt('CLOUD_COVER',CC))\
                                        .select(['SR_B5', 'SR_B4', 'SR_B3'])

    # Filtro la colección por las fechas de interés
    Landsat7 = col_landsat7.filter(ee.Filter.calendarRange(year[0], year[1], year[2]))\
                            .filter(ee.Filter.calendarRange(month[0], month[1], month[2]))
                                      
    # Coleccion Landsat5;
    col_landsat5 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2.")\
                                        .filterBounds(polygon)\
                                        .filterBounds(loc)\
                                        .filter(ee.Filter.lt('CLOUD_COVER',CC))\
                                        .select(['SR_B4', 'SR_B3', 'SR_B2'])

    # Filtro la colección por las fechas de interés
    Landsat5 = col_landsat5.filter(ee.Filter.calendarRange(year[0], year[1], year[2]))\
                            .filter(ee.Filter.calendarRange(month[0], month[1], month[2]))
   
    # Exporto las imagenes de Landsat9
    geemap.ee_export_image_collection(Landsat9,
                                      out_dir=path+"L9",
                                      scale=(30), 
                                      crs='EPSG:32719',
                                      region=polygon)

    # Exporto las imagenes de Landsat8
    geemap.ee_export_image_collection(Landsat8,
                                      out_dir=path+"L8",
                                      scale=(30), 
                                      crs='EPSG:32719',
                                      region=polygon)
    
    # Exporto las imagenes de Landsat7    
    geemap.ee_export_image_collection(Landsat7,
                                      out_dir=path+"L7",
                                      scale=(30), 
                                      crs='EPSG:32719',
                                      region=polygon)
    
    # Exporto las imagenes de Landsat5
    geemap.ee_export_image_collection(Landsat5,
                                      out_dir=path+"L5",
                                      scale=(30), 
                                      crs='EPSG:32719',
                                      region=polygon)
    
    msj = print("Larga vida al rey Julien")

    return msj

#%% Sector de prueba
pueba = descarga_masiva(polygon, loc, path, year, month, CC)

