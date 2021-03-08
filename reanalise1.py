# -*- coding: utf-8 -*-
#
# AUTOR: Douglas Medeiros Nehme
#
# CONTACT: medeiros.douglas3@gmail.com
#
# CRIATION: fev/2017
#
# LAST MODIFICATION: mar/2017
#
# OBJECTIVE: Manipulating Antartica wind data

import os
import math
import numpy as np
import pandas as pd
import xarray as xr

##################################################################################################################################
#### CONFIG PARAMETERS AND GLOBAL VARIABLES ######################################################################################
##################################################################################################################################
# pep-8 conventions suggest upper case for global variables

ROOTDIR = '/home/douglasnehme/Desktop/bia'
DATADIR = os.path.join(ROOTDIR, 'arquivos')


##################################################################################################################################
#### FUNCTIONS ###################################################################################################################
##################################################################################################################################

def pol2cart_wind(wspd, wdir, axes_rotation = 0, magnetic_declination = 0):
    """
    Converts meteorological stations' wind measure, speed and direction (in degrees), into meridional and zonal components.


    Parameters
    ----------
    wspd = wind speed

    wdir = wind direction (in degrees)

    axes_rotation = permits axes rotation with posite values doing a clockwise moviment and negative values an anticlockwise. It
    allows a better fit between wind components and local wind regime

    magnetic_declination = permits correction between true and magnetic norths

    Reference
    ---------
    MIRANDA, L. B.; CASTRO, B. M.; KJERFVE, B. Redução e Análise de Dados Experimentais: Fluxo e Transporte de Propriedades. In:
    Princípios de Oceanografia Física em Estuários. 2 ed. São Paulo: Editora da Universidade de São Paulo, 2012. Cap. 5, p. 153-192.
    ISBN: 978-85-314-0675-1.

    Steps
    -----
    1 - Decimal places standardization (Input data)

    2 - Transform angles from meteorological (wdir) to cartesian referential (phi), where trigonometric equations are valid

        METEOROLOGICAL REFERENTIAL       CARTESIAN REFERENTIAL
                 360°/0°                         90°
                    |                             |
                    |                             |
         270° ______|______ 90°        180° ______|______ 360°/0°
                    |                             |
                    |                             |
                    |                             |
                   180°                          270°

    3 - Fix all phi values between 0° and 360°

    4 - Transform angles from degrees to radians and calculating wind components

    5 - Decimal places standardization (Output data)
    """
    import math

    # Step 1
    wdir = math.ceil(wdir) # always rounds the float number to next integer, but returns a float number
    wspd = round(wspd, 1)  # round a number to a given precision in decimal digits considering round laws

    # Step 2
    phi = 90. - (wdir + magnetic_declination) + axes_rotation

    # Step 3
    if phi < 0.:

        phi = phi + 360.

    # Step 4
    phi = math.radians(phi)

    u = wspd * math.cos(phi)
    v = wspd * math.sin(phi)
    
    # Step 5
    u = round(u, 2)
    v = round(v, 2)

    return(u, v)


def cart2pol_wind(u, v, axes_rotation = 0, magnetic_declination = 0):
    """
    Converts meridional and zonal wind components into speed and direction (in degrees) values.


    Parameters
    ----------
    u = zonal component

    v = meridional component

    axes_rotation = undo axes rotation with posite values doing a clockwise moviment and negative values an anticlockwise. It
    allows a better fit between wind components and local wind regime

    magnetic_declination = Put here for extension of pol2cart_wind function, but doesn't have usage now, possible in future

    Reference
    ---------
    MIRANDA, L. B.; CASTRO, B. M.; KJERFVE, B. Redução e Análise de Dados Experimentais: Fluxo e Transporte de Propriedades. In:
    Princípios de Oceanografia Física em Estuários. 2 ed. São Paulo: Editora da Universidade de São Paulo, 2012. Cap. 5, p. 153-192.
    ISBN: 978-85-314-0675-1.

    Steps
    -----
    1 - Decimal places standardization (Input data)

    2 - Calculate wind speed and cartesian referential angle (phi) from wind componentes and convert phi from radians to degrees
    
    3 - Transform angles from cartesian (phi) to meteorological referential (wdir)

        METEOROLOGICAL REFERENTIAL       CARTESIAN REFERENTIAL
                 360°/0°                         90°
                    |                             |
                    |                             |
         270° ______|______ 90°        180° ______|______ 360°/0°
                    |                             |
                    |                             |
                    |                             |
                   180°                          270°

    4 - Fix all wdir values between 0° and 360°

    5 - Decimal places standardization (Output data)
    """
    import math
    
    # Step 1
    u = round(u, 2)
    v = round(v, 2)

    # Step 2
    wspd = math.sqrt(u**2 + v**2)
    phi  = math.atan2(v, u)

    phi = math.degrees(phi)

    # Step 3
    wdir = 90. - (phi + magnetic_declination) + axes_rotation

    # Step 4
    if wdir < 0.:

        wdir = wdir + 360.

    # Step 5
    wdir = math.ceil(wdir) # always rounds the float number to next integer, but returns a float number
    wspd = round(wspd, 1) # round a number to a given precision in decimal digits considering round laws

    return(wspd, wdir)



##################################################################################################################################
#### IMPORTING AND MANIPULATING ALL TIME SERIES ##################################################################################
##################################################################################################################################

ncep = xr.open_dataset(os.path.join(DATADIR, 'reanalise1.nc'))

ncep.longitude.data = ncep.longitude.data - 360.

ncep = ncep.resample('A', 'time', how = 'mean')

wspd, wdir = [np.nan] * len(ncep.time), [np.nan] * len(ncep.time)

for i in xrange(len(ncep.time)):
    wspd[i], wdir[i] = cart2pol_wind(ncep.uwnd[ :, 1, 1].data[i], ncep.vwnd[ :, 1, 1].data[i])

df = pd.DataFrame (index = ncep.time.data, columns = ['u', 'v', 'spd'],
                   data = {'u': ncep.uwnd[ :, 1, 1].data, 'v': ncep.vwnd[ :, 1, 1].data, 'spd': wspd} )

df.to_excel(os.path.join(ROOTDIR, 'reanalise', 'reanalise1.xlsx'))