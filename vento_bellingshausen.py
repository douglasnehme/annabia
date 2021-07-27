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

filename1 = u'vento_bellingshausen_direcao.xlsx'
filename2 = u'vento_bellingshausen_velocidade.xlsx'

new_filename = u'vento_u_v_bellingshausen.xlsx'
##############################################################################
# OPENNING AND MANIPULATING DATA #############################################
##############################################################################
# Open files
wdir = pd.read_excel(
    os.path.join(
        DATADIR,
        filename1
    ),
    header=0,
    index_col=0,
    na_values=['', '-']
)
wspd = pd.read_excel(
    os.path.join(
        DATADIR,
        filename2
    ),
    header=0,
    index_col=0,
    na_values=['', '-']
)
# Transform a df with monthly variation on
# columns and years on lines to Series with
# multi-index and all mothly values
wdir = wdir.stack()
wspd = wspd.stack()

# Aggregate month and year info from
# multi-index in one string, transform it
# into datetime and set as Series index
wdir.index = pd.to_datetime((
    wdir.index.get_level_values(0).astype('str') +
    '-' +
    wdir.index.get_level_values(1).astype('str')
))
wspd.index = pd.to_datetime((
    wspd.index.get_level_values(0).astype('str') +
    '-' +
    wspd.index.get_level_values(1).astype('str')
))

# Name Series
wdir.name = 'wdir'
wspd.name = 'wspd'

# Fill gaps with NaN
wdir = wdir.resample('MS').asfreq()
wspd = wspd.resample('MS').asfreq()

# Merge two Series in one df
df = pd.merge(
    wspd,
    wdir,
    left_index=True,
    right_index=True
)

del wdir, wspd

u, v = airsea.pol2cart_wind(
    df.wspd,
    df.wdir,
    rnd=1
)
df_new = pd.DataFrame(
    data={
        'u':u.values,
        'v':v.values
    },
    index=u.index
)

##########################################################
# Transforming index from a daily series from 03/1968 to 
# 01/2021 over all rows length to a yearly series over all
# rows length and monthly variations on columns dimension
##########################################################
df_new = df_new.groupby([
    df_new.index.year,
    df_new.index.month
]).mean()
df_new.index.names = ['', ''] 
df_new = df_new.unstack()
##########################################################

# Save
df_new.to_excel(os.path.join(DATADIR, new_filename))

stop = datetime.now().replace(microsecond=0)

print('Time taken to execute program: {}'.format(stop - start))
