# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 11:50:48 2022

@author: Juan Cruz
"""

#%%
def date_to_DOY (date, fmt):
    """
    Esta función toma como entrada una fecha (str) y devuelve
    el día del año (DOY) como un entero. Para lograr correctamente 
    esta transformación hay que definir el formato de la fecha
    
    Parameters
    ----------
    dates : str
        Fecha que quiero convertir
    fmt: str
        Formato en el que cargo las fechas; 
        ejemplos: '%d-%m-%Y' es '15-04-2021'
                    '%d/%m/%Y' es '15/04/2021'
    Returns
    -------
    la fecha convertida en día del año (int)

    """

    import datetime
    
    #Convierte las fechas a datetime
    dt = datetime.datetime.strptime(date, fmt)
    tt = dt.timetuple()
    #Toma el dato del día del año
    doy = tt.tm_yday

    return doy

#%%
# Ejemplo

# Tengo una lista de fechas
dates = [ "11/04/1986", "13/04/2021", "21/03/2020", "11/04/2019",
           "30/03/2018", "06/04/2017", "04/04/2016",
            "17/03/2015", "15/04/2014", "02/04/2013", "07/04/2011",
            "13/04/2010", "01/04/2009","20/03/2007", "09/04/2006",
            "15/04/2005", "27/03/2004","22/03/2002", "19/03/2001",
            "01/04/2000", "21/03/1996","11/04/1995", "20/03/1993",
            "13/04/1990"]

# Defino el formato
fmt = '%d/%m/%Y'

# Creo una lista vacía donde van a estar las fechas covertidas
DOY = []

# Aplico la funció en un ciclo for
for i in dates:
    DOY.append(date_to_DOY (i, fmt))  
    
