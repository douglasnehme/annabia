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
# OBJECTIVE: Tranforming Julian data for Bia
 
import os
import pandas as pd

from datetime import datetime, timedelta

start = datetime.now().replace(microsecond = 0)
##############################################################################
#### CONFIG PARAMETERS AND GLOBAL VARIABLES ##################################
##############################################################################
if os.path.expanduser('~') == '/home/numa7':
    ROOTDIR = '/home/numa7/douglas/Dropbox/profissional/bia'
if os.path.expanduser('~') == '/home/douglasnehme':
    ROOTDIR = '/home/douglasnehme/Desktop/bia/scripts/julian4datetime/'

##############################################################################
# OPENNING AND MANIPULATING DATA #############################################
##############################################################################

# Open files
ssi = pd.read_csv(os.path.join(ROOTDIR, 'nrl2_ssi_P1D-279nm-1882-2017-daily'), header=0)
tsi = pd.read_csv(os.path.join(ROOTDIR, 'nrl2_tsi_P1D-1882a2017-daily'), header=0)

# Setting columns name by Emilia Correia information
# julian = days since 1610-01-01
# wavelength = nm
# irradiance = W/m^2/nm
# error = ?
ssi.columns = ['julian', 'wavelength', 'irradiance', 'error']
tsi.columns = ['julian', 'irradiance', 'error']

# Calculate datetime dates from julian dates
start_julian = datetime(1610, 1, 1) 

datetime_index = []

for i in range(len(ssi)):
    delta = timedelta(ssi.julian[i])
    datetime_index.append(start_julian + delta)

ssi.index = datetime_index
ssi.index.name = 'datetime'


datetime_index = []

for i in range(len(tsi)):
    delta = timedelta(tsi.julian[i])
    datetime_index.append(start_julian + delta)

tsi.index = datetime_index
tsi.index.name = 'datetime'


ssi_monthly = ssi.resample('MS').mean()
tsi_monthly = tsi.resample('MS').mean()

##########################################################
# Transforming index from a monthly series from 01/1882 to 
# 12/2017 over all rows length to a yearly series over all
# rows length and monthly variations on columns dimension
ssi_monthly_groupedby = ssi_monthly.groupby([ssi_monthly.index.year, ssi_monthly.index.month]).mean()
tsi_monthly_groupedby = tsi_monthly.groupby([tsi_monthly.index.year, tsi_monthly.index.month]).mean()

ssi_monthly_groupedby.index.names = ['', '']
tsi_monthly_groupedby.index.names = ['', '']

ssi_monthly_groupedby = ssi_monthly_groupedby.unstack()
tsi_monthly_groupedby = tsi_monthly_groupedby.unstack()
##########################################################

# Save
ssi.to_csv(os.path.join(ROOTDIR, 'nrl2_ssi_P1D-279nm-1882-2017-daily_NEW.csv'))
tsi.to_csv(os.path.join(ROOTDIR, 'nrl2_tsi_P1D-1882a2017-daily_NEW.csv'))

ssi_monthly.to_csv(os.path.join(ROOTDIR, 'nrl2_ssi_P1D-279nm-1882-2017-monthly_NEW.csv'))
tsi_monthly.to_csv(os.path.join(ROOTDIR, 'nrl2_tsi_P1D-1882a2017-monthly_NEW.csv'))

ssi_monthly_groupedby.to_csv(os.path.join(ROOTDIR, 'nrl2_ssi_P1D-279nm-1882-2017-monthly_groupedby_NEW.csv'))
tsi_monthly_groupedby.to_csv(os.path.join(ROOTDIR, 'nrl2_tsi_P1D-1882a2017-monthly_groupedby_NEW.csv'))