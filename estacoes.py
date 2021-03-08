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
import matplotlib as mpl
import matplotlib.pyplot as plt

##################################################################################################################################
#### CONFIG PARAMETERS AND GLOBAL VARIABLES ######################################################################################
##################################################################################################################################
# pep-8 conventions suggest upper case for global variables

ROOTDIR = '/home/douglasnehme/Desktop/bia'


METADICT = {
'arturo_prat'    : { 'file': 'arturo_prat',    'name': 'Arturo Prat',    'id': '89057', 'lat': '62.5S', 'lon': '59.7W', 'alt': 5   },
'bellingshausen' : { 'file': 'bellingshausen', 'name': 'Bellingshausen', 'id': '89050', 'lat': '62.2S', 'lon': '58.9W', 'alt': 16  },
'deception'      : { 'file': 'deception',      'name': 'Deception',      'id': '88938', 'lat': '63.0S', 'lon': '60.7W', 'alt': 8   },
'esperanza'      : { 'file': 'esperanza',      'name': 'Esperanza',      'id': '88963', 'lat': '63.4S', 'lon': '57.0W', 'alt': 13  },
'faraday'        : { 'file': 'faraday',        'name': 'Faraday',        'id': '89063', 'lat': '65.4S', 'lon': '64.4W', 'alt': 11  },
'ferraz'         : { 'file': 'ferraz',         'name': 'Ferraz',         'id': '89252', 'lat': '62.1S', 'lon': '58.4W', 'alt': 20  },
'great_wall'     : { 'file': 'great_wall',     'name': 'Great Wall',     'id': '89058', 'lat': '62.2S', 'lon': '59.0W', 'alt': 10  },
'jubany'         : { 'file': 'jubany',         'name': 'Jubany',         'id': '89053', 'lat': '62.2S', 'lon': '58.6W', 'alt': 4   },
'king_sejong'    : { 'file': 'king_sejong',    'name': 'King Sejong',    'id': '89251', 'lat': '62.2S', 'lon': '58.7W', 'alt': 11  },
'marambio'       : { 'file': 'marambio',       'name': 'Marambio',       'id': '89055', 'lat': '64.2S', 'lon': '56.7W', 'alt': 198 },
'marsh'          : { 'file': 'marsh',          'name': 'Marsh',          'id': '89056', 'lat': '62.2S', 'lon': '58.9W', 'alt': 10  },
'o_higgins'      : { 'file': 'o_higgins',      'name': "O'Higgins",      'id': '89059', 'lat': '63.3S', 'lon': '57.9W', 'alt': 10  },
'orcadas'        : { 'file': 'orcadas',        'name': 'Orcadas',        'id': '88968', 'lat': '60.7S', 'lon': '44.7W', 'alt': 6   },
'palmer'         : { 'file': 'palmer',         'name': 'Palmer',         'id': '89061', 'lat': '64.3S', 'lon': '64.0W', 'alt': 8   },
'signy'          : { 'file': 'signy',          'name': 'Signy',          'id': '89042', 'lat': '60.7S', 'lon': '45.6W', 'alt': 6   },
}

mpl.rcParams['axes.labelsize'] = 10

mpl.rcParams['xtick.labelsize'] = 10
mpl.rcParams['ytick.labelsize'] = 10

mpl.rcParams['figure.autolayout']   = True # Similar of fig.tight_layout()

mpl.rcParams['savefig.dpi'] = 200
mpl.rcParams['savefig.format'] = 'jpeg'


MESES = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']

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


def tendency_line_plot(xaxis_variable, yaxis_variable):
    """
    This function calculates a linear regression. Beyond the tendency line parameters
    (slope and y-intercept point), it gives the correlation coefficient (rvalue), the
    value of null hypothesis (pvalue) and the standard error of the estimate (stderr).

    Through the tendency line parameters and the x-axis variable, this function plots
    the tendency line in a figure with another plots.

    Requirements
    ------------
    NEED NUMPY MODULE IMPORTED -> import numpy as np
    NEED STATS MODULE IMPORTED -> from scipy import stats
    
    Returns
    -------
    slope : float
        slope of the regression line
    intercept : float
        intercept of the regression line
    r-value : float
        correlation coefficient
    p-value : float
        two-sided p-value for a hypothesis test whose null hypothesis is that the slope is zero.
    stderr : float
        Standard error of the estimate
    plot : matplotlib plot
        tendency line
    """
    import numpy as np
    from scipy import stats

    tendency_line = []
    slope, intercept, rvalue, pvalue, stderr = stats.linregress(xaxis_variable, yaxis_variable)

    for i in xrange(len(xaxis_variable)):
        tendency_line.append(intercept + (slope * xaxis_variable[i]))

    plot = plt.plot(tendency_line, yaxis_variable, color = 'red', linewidth = 0.4)

    return slope, intercept, rvalue, pvalue, stderr, plot


##################################################################################################################################
#### IMPORTING AND MANIPULATING ALL TIME SERIES ##################################################################################
##################################################################################################################################
c = 1

for key in METADICT.iterkeys():
# for key in ['king_sejong']:
    print key
    c = c + 1


    #### Opening all data ####


    wspd, wdir = [], []
    
    spd = pd.read_excel(os.path.join(ROOTDIR, METADICT[key]['file'] + '.xlsx'), sheetname = 'Sheet1', na_values = ['-'],
                        index_col = 'Year')

    spd_flag = spd.copy()


    dire = pd.read_excel(os.path.join(ROOTDIR, METADICT[key]['file'] + '.xlsx'), sheetname = 'Sheet2', na_values = ['-'],
                        index_col = 'Year')

    dire_flag = dire.copy()

    # These loops equalize the initial year of speed and direction DataFrames
    if spd.index.min() > dire.index.min():                                                     

        spd_begin = spd.reindex(index = np.arange(dire.index.min(), spd.index.min()))

        spd = pd.concat([spd_begin, spd])

    elif dire.index.min() > spd.index.min():

        dire_begin = dire.reindex(index = np.arange(spd.index.min(), dire.index.min()))

        dire = pd.concat([dire_begin, dire])


    #### Loops for creating the lists from DataFrames ####


    for i in xrange(len(spd.index)):

        for ii in xrange(len(spd.columns)):

            a = spd.ix[spd.index[i], spd.columns[ii]]
            
            if type(a) != float:

                b = a.replace(')','').split('(')

                spd.ix[spd.index[i], spd.columns[ii]] = b[0]
                spd_flag.ix[spd.index[i], spd.columns[ii]] = b[1]

                wspd.append(float(b[0]))

            if type(a) == float:

                wspd.append(a)
        

    for i in xrange(len(dire.index)):

        for ii in xrange(len(dire.columns)):

            a = dire.ix[dire.index[i], dire.columns[ii]]
            
            if type(a) != float:

                b = a.replace(')','').split('(')

                dire.ix[dire.index[i], dire.columns[ii]] = b[0]
                dire_flag.ix[dire.index[i], dire.columns[ii]] = b[1]

                # Function 'math.ceil' rounds the float number to next integer, that is different of function 'int', that rounds
                # for the before integer. In this case 'math.ceil' was choosen to avoid having 0 degree in wind direction and 
                # making possible having 360 degree.
                wdir.append(math.ceil(float(b[0])))

            if type(a) == float:

                wdir.append(a)


    #### Loop for creating the wind components (u and v) DataFrames ####


    spd = spd.astype(float)
    spd_flag = spd_flag.astype(float)

    dire = dire.astype(float)
    dire_flag = dire_flag.astype(float)

    u = spd.copy()
    v = spd.copy()

    for i in xrange(len(spd.index)):

        for ii in xrange(len(spd.columns)):

            u.iloc[i, ii], v.iloc[i, ii] = pol2cart_wind(spd.iloc[i, ii], dire.iloc[i, ii])

    # The slice from 0 to -5 is done to cut final years and transform 2012, testimony collection year, in the last.
    u = u[0:-5]
    v = v[0:-5]


    #### Data that will be analysed by python plots ####


    spd_month = spd.mean(axis = 0)
    spd_year  = spd.mean(axis = 1)

    u_month   = u.mean(axis = 0)
    u_year    = u.mean(axis = 1)

    v_month   = v.mean(axis = 0)
    v_year    = v.mean(axis = 1)
    
    # These data can't be used, because mean of directions is a wrong method to obtain this estatistical value of a vector
    # dire_month = dire.mean(axis = 0)
    # dire_year  = dire.mean(axis = 1)


    #### Creating WRPlot DataFrame from data in lists ####


    # windex = pd.date_range(start = str(spd.index.min()), end = str(spd.index.max() + 1), freq = 'M')

    # c = np.full(len(windex), np.nan) # creating a array of nans with same length of windex

    # data = {'wspd': wspd, 'wdir': wdir, 'year': c, 'month': c, 'day': c, 'hour': c}

    # wind = pd.DataFrame(data = data, columns = ['year', 'month', 'day', 'hour', 'wspd', 'wdir'], index = windex, dtype = int)

    # wind = wind.asfreq('H')

    # wind.year  = wind.index.year
    # wind.month = wind.index.month
    # wind.day   = wind.index.day
    # wind.hour  = wind.index.hour

    # wind.to_excel (os.path.join(ROOTDIR, METADICT[key]['file'] + '_wrplot' + '.xlsx'), na_rep = 'NaN')

    stop
    ##################################################################################################################################
    #### PLOTTING DATA ###############################################################################################################
    ##################################################################################################################################

    #### Plotting Data - Separated Yearly and Monthly Plots ####
    # fig, ax = plt.subplots(figsize = (5, 7))

    # This plot wasn't do normally (u_year.plot()), because we want to put the years (Serie's index) in the y-axis and the u data
    # (Serie's values) in x-axis.
    # plt.plot(u_year.values, u_year.index, color = 'k')

    # ax.set_title(u'{0} ({1} {2})'.format(METADICT[key]['name'], METADICT[key]['lat'], METADICT[key]['lon']), y = 1.07, fontweight = 'bold')

    # ax.set_xlabel('Componente Zonal do Vento ($\mathregular{m.s^{-1}}$)')
    # ax.set_ylabel('Anos')

    # ax.xaxis.set_label_position('top') # Putting the x-axis label in top border
    # ax.xaxis.set_ticks_position('top') # Putting the x-axis ticks in top border

    # ax.axvline(0, linestyle = '--', color = 'gray', linewidth = 1) # Plotting a vertical line in position 0 of x-axis

    # tendency_line_plot(u_year.values, u_year.index)

    # plt.savefig(os.path.join(ROOTDIR, METADICT[key]['file']) + '_anual')
    
    # plt.close()


    # fig, ax = plt.subplots(figsize = (5, 3))

    # u_month.plot(color = 'k')

    # ax.set_title(u'{0} ({1} {2})'.format(METADICT[key]['name'], METADICT[key]['lat'], METADICT[key]['lon']), y = 1.02, fontweight = 'bold')

    # ax.set_ylabel('Componente Zonal do Vento ($\mathregular{m.s^{-1}}$)')
    # ax.set_xlabel('Meses')

    # ax.axhline(0, linestyle = '--', color = 'gray', linewidth = 1) # Plotting a vertical line in position 0 of x-axis

    # ax.set_xticks(np.arange(12))
    # ax.set_xticklabels((MESES), rotation = False)

    # plt.savefig(os.path.join(ROOTDIR, METADICT[key]['file']) + '_mensal')

    # plt.close()

    #### Plotting Data - Plots Together ####



    # Comands to clear top and right borders of a plot
    # ax1.spines['right'].set_visible(False)
    # ax1.spines['top'].set_visible(False)

