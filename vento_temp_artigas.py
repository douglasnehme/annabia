# -*- coding: utf-8 -*-
#
# AUTOR: Douglas Medeiros Nehme
#
# PLACE: Rio de Janeiro - Brazil
#
# CONTACT: douglasnehme@ufrj.br
#
# CRIATION: ago/2018
#
# LAST MODIFICATION: ago/2018
#
# OBJECTIVE: Processing Artigas' meteorological station data for Bia (INUMET)
 
import os
import sys

import pandas as pd

from datetime import datetime

sys.path.insert(0, os.path.expanduser('~/Dropbox/airsea'))

import airsea

start = datetime.now().replace(microsecond = 0)
##############################################################################
#### CONFIG PARAMETERS AND GLOBAL VARIABLES ##################################
##############################################################################
DATADIR = u'/home/douglasnehme/Desktop/bia/arquivos'

filename = u'Datos INUMET Antártida 1998-2016_vento e temp.xlsx'
new_filename = u'Datos INUMET Antártida 1998-2016_vento e temp_groupedby.xlsx'
##############################################################################
# OPENNING AND MANIPULATING DATA #############################################
##############################################################################
columns_name =[
    'datetime',
    'temp',
    'wspd',
    'wdir'
]

# Open file
df = pd.read_excel(
    os.path.join(
        DATADIR,
        filename
    ),
    header=None,
    names=columns_name,
    skiprows=1,
    index_col='datetime',
    na_values=['', 'variable']
)

# # Drop wind direction variable
# df.drop(
#     'wdir',
#     axis=1,
#     inplace=True
# )

# Fill gaps with NaN
df = df.resample('6H').asfreq()

df['u'], df['v'] = airsea.pol2cart_wind(
    df.wspd,
    df.wdir,
    rnd=1
)
##########################################################
# Transforming index from a daily series from 01/1998 to 
# 05/2016 over all rows length to a yearly series over all
# rows length and monthly variations on columns dimension
##########################################################
df = df.groupby([df.index.year, df.index.month]).mean()
df.index.names = ['', ''] 
df = df.unstack()
##########################################################

# Save
df.to_excel(os.path.join(DATADIR, new_filename))

stop = datetime.now().replace(microsecond=0)

print('Time taken to execute program: {}'.format(stop - start))
