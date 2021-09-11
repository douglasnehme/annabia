# -*- coding: utf-8 -*-
# AUTOR: Douglas Medeiros Nehme
# CONTACT: medeiros.douglas3@gmail.com
# CRIATION: sep/2021
# LAST MODIFICATION: sep/2021
# OBJECTIVE: Processing MetReader wind data for
#            Decepetion Island to Bia apply in
#            WRPlot for the final work of
#            Hysplit PhD course
import os

import numpy as np
import pandas as pd

from datetime import datetime

################################################
#### Config Parameters and Global Variables ####
################################################

rootdir = (
    'https://legacy.bas.ac.uk/met/READER/' +
    'surface'
)

station = 'Deception'

vardict = {
    'wspd': 'wind_speed.txt',
    'wdir': 'wind_direction.txt',
}

# Month number array padded with leading zero
cols = np.char.zfill(
    np.arange(1, 13).astype(str),
    2)

################################################
#### Data Processing ###########################
################################################
df = pd.DataFrame()

for var in  vardict.keys():
    fname = station + '.All.' + vardict[var]

    data = pd.read_csv(
        os.path.join(
            rootdir,
            fname),
        skiprows=1,
        sep='\\s+',
        names=range(1, 13),
        na_values='-')

    # Name columns and index to make easier work
    # with MultiIndex
    data.columns.name = 'month'
    data.index.name = 'year'

    data = data.transpose()

    # Transform a DataFrame with year on columns
    # and months on index into a MultiIndex
    # Series 
    data = data.unstack()

    # Name the series with variable name
    data = data.rename(var)

    # Reset MultiIndex to DatetimeIndex
    idx = []
    for y, m in data.index:
        idx.append(datetime(y, m, 1))

    data.index = idx

    # Concatenate each wind data Series with an
    # empty DataFrame
    df = pd.concat([
        df,
        data],
        axis='columns',
        names=var)

# Drop the rows in which all values are NaN
df.dropna(
    axis='index',
    inplace=True,
    how='all')

# Transform the monthly index into a daily one
hourly_idx = pd.date_range(
   df.index.min(),
   df.index.max(),
   freq='H')

df = df.reindex(hourly_idx)

# Create columns with each datetime information
# to be used in WRPlot
df['year'] = df.index.year
df['month'] = df.index.month
df['day'] = df.index.day
df['hour'] = df.index.hour

# Transform NaN cells to empty ones to follow
# WRPlot needs
df = df.astype(str)

df.replace(
    'nan',
    '',
    inplace=True)

df.to_excel((
    '/home/dnehme/Desktop/bia/arquivos/' +
    'dados_vento_Decepetion_WRPlot.xlsx'))