# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:40:23 2022

@author: Usuario
"""
# Librerías necesaarias
from osgeo import ogr, gdal, osr
import subprocess
import rasterio
import os

#%% funcion para rasterizar poligonos 
def shape2raster(pathshape,path_reference_raster,path_final_raster):
    """
    Esta funcion requiere el path del shape que queres rasterizar, el path
    del raster de referencia (el cual va a usar como "molde") y la carpeta
    de destino. Genera mascaras binarias de 1 y 0. 
    """

    InputVector = pathshape
    OutputImage = path_final_raster

    RefImage = path_reference_raster

    gdalformat = 'GTiff'
    datatype = gdal.GDT_Byte
    burnVal = 1 #value for the output image pixels
    
    # Get projection info from reference image
    Image = gdal.Open(RefImage, gdal.GA_ReadOnly)

    # Open Shapefile
    Shapefile = ogr.Open(InputVector)
    Shapefile_layer = Shapefile.GetLayer()

    # Rasterise
    Output = gdal.GetDriverByName(gdalformat).Create(OutputImage, Image.RasterXSize, Image.RasterYSize, 1, datatype, options=['COMPRESS=DEFLATE'])
    Output.SetProjection(Image.GetProjectionRef())
    Output.SetGeoTransform(Image.GetGeoTransform()) 

    # Write data to band 1
    Band = Output.GetRasterBand(1)
    Band.SetNoDataValue(0) 
    gdal.RasterizeLayer(Output, [1], Shapefile_layer, burn_values=[burnVal])

    # Close datasets
    Band = None
    Output = None
    Image = None
    Shapefile = None
    # Build image overviews
    subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+OutputImage+" 2 4 8 16 32 64", shell=True)
    print("Done.")
    
#%% funcion para transformar array en raster
def array2raster(raster_mask_path,rasterpath,array):
    '''genera un geotiff del array de la mascara binaria y la metadata del geotiff inicial.
    Devuelve el path del raster con la mascara binaria'''
    
    # lenguafecha='mask_lengua_'+rasterpath[-12:]
    new_rasterpath=os.path.join(raster_mask_path)
    
    raster = gdal.Open(rasterpath) #abre el raster de referencia
    proj = raster.GetProjection() #toma la proyeccion del raster de ref
    geotransform = raster.GetGeoTransform() #toma la geotransformacion
    originX = geotransform[0] #parametros?
    originY = geotransform[3] #parametros?
    pixelWidth = geotransform[1] #parametros?
    pixelHeight = geotransform[5] #parametros?
    cols = array.shape[1] #parametros?
    rows = array.shape[0] #parametros?

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(new_rasterpath, cols, rows, 1, gdal.GDT_Byte)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(proj)
    outband.FlushCache()
    return new_rasterpath

#%%   parametros de entrada (cubierto)

# Genero una mascara binaria para todo lo que es glaciar cubierto
path_reference_raster = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\Raster_Zeller_Combinado.tif"
path_final_raster = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_filtrado_cubierto.tif"
pathshape = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_filtrado_cubierto.shp"

# Aplico la función 
raster_cubierto = shape2raster(pathshape,path_reference_raster,path_final_raster)

#%%   parametros de entrada (descubierto)
# Genero una mascara binaria para todo lo que es glaciar descubierto
path_reference_raster = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\Raster_Zeller_Combinado.tif"
path_final_raster = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_filtrado_descubierto.tif"
pathshape = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_filtrado_descubierto.shp"

# Aplico la función 
raster_descubierto = shape2raster(pathshape,path_reference_raster,path_final_raster)

#%% genero array con valores categoricos
# Genero un array vacío con el tamaño de los raster que quiero trabajar
# Aca estan los paths de las mascaras binarias descubierto y cubierto
path_final_raster_descubierto = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_filtrado_descubierto.tif"
path_final_raster_cubierto = r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_filtrado_cubierto.tif"

# Direccion donde voy a guardar el resultado (raster clasificado)
path_salida =  r"C:\DebrisCoverGlacier_Scrips\Muestreo_rasters\gdf_clasificado_ING.tif"

# Abro los rasters
dc = rasterio.open(path_final_raster_cubierto)
un = rasterio.open(path_final_raster_descubierto)

# Trabajando con rasterio
arr_dc = dc.read(1) + dc.read(1) # de esta forma la clasificación de DC es el valor 2
arr_uc = un.read(1) # la clasificacion de UN es 1
arr_classify = arr_dc + arr_uc

# Cierro los rasters
dc.close()
un.close()

#%% aplico la funcion array2raster
raster_clasificado_ING = array2raster(path_salida,path_final_raster_descubierto,arr_classify)
