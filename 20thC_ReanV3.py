#!/usr/bin/env python

import os

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap

#########################################

def std_lon(da, lon_name):
    """
    Function to transform longitudes from
    0:359 range to -180:180
    """
    da = da.assign_coords({
        lon_name: (((da[lon_name] + 180) % 360) - 180)
    })

    da = da.sortby(
        lon_name,
        ascending=True
    )

    return da

#########################################

# Different of other folders where SI
# subfolders represented data from 1836
# to 1980 and MO subfolders represented
# data from 1981 to 2015 in monthly files
# was the same wheter in SI or MO

# path = [
#     'https://psl.noaa.gov/thredds/dodsC/Datasets/20thC_ReanV3/Monthlies/miscMO/tco3.eatm.mon.mean.nc',
#     'https://psl.noaa.gov/thredds/dodsC/Datasets/20thC_ReanV3/Monthlies/10mMO/uwnd.10m.mon.mean.nc'
# ]
path = [
    '/home/douglasnehme/Desktop/bia/arquivos/tco3.eatm.mon.mean.nc',
    '/home/douglasnehme/Desktop/bia/arquivos/uwnd.10m.mon.mean.nc'
]


shetland_lat = (-63, -62)
shetland_lon = (-63, -57)

reigeorge_lat = (-63, -62)
reigeorge_lon = (-59, -58)

#########################################

nc = xr.open_mfdataset(
    path,
    concat_dim='time',
    combine='by_coords'
)

nc = nc.drop_dims('nbnds')

nc = std_lon(nc, 'lon')


column_names = {}

for var in nc.variables.keys():
    try:
        ['lat', 'lon', 'time', 'time_bnds'].index(var)
    
    except:
        column_names[var] = nc[var].long_name.replace(' ', '_') + '-(' + nc[var].units.replace(' ', '.') + ')'


nc1 = nc.sel(
    lon=slice(
        shetland_lon[0],
        shetland_lon[1]), 
    lat=slice(
        shetland_lat[0],
        shetland_lat[1])
)

fig, ax = plt.subplots()

# Creating specific variables to customize the map
parallels = nc1.lat.values
meridians = nc1.lon.values

# Defining map settings
m = Basemap (projection='merc',
             llcrnrlat=-64.02, urcrnrlat=-60.98, 
             llcrnrlon=-63.01, urcrnrlon=-56.98, 
             resolution='f', area_thresh=0, ax=ax)
            # resolution -> 'c'=crude, 'l'=low, 'i'=intermediate, 'h'=high and 'f'=full

m.drawcoastlines(linewidth=0.5)
m.drawmapboundary()

m.fillcontinents(color='gray', zorder=1)


m.drawparallels(parallels, labels=[True, True, False, False], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999)
m.drawmeridians(meridians, labels=[False, False, True, True], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999, rotation=45)


lon, lat = np.meshgrid(nc1.lon.values, nc1.lat.values)

# Setting coordinate variables for this especific map
x, y = m(lon, lat)

plt.pcolor(x, y, nc1.tco3[0])
plt.scatter(x, y, c=nc1.tco3[0], zorder=99)

plt.colorbar()

# Spatial mean
nc1 = nc1.mean(dim=['lon', 'lat'], keep_attrs=True)

# Transforming the xr.Dataset into a pd.DataFrame
df1 = nc1.to_dataframe()

# Renaming columns to retain long_name and units info
df1.rename(index=str, columns=column_names, inplace=True)

df1.index = pd.to_datetime(df1.index, yearfirst=True)

df1 = df1.groupby([df1.index.year, df1.index.month]).mean()

df1.index.names = ['', ''] 

df1 = df1.unstack()

# Saving
df1.to_csv(
    os.path.join(
        '/home/douglasnehme/Desktop/bia/arquivos/',
        '20thC_ReanV3_shetland.csv'
))




nc2 = nc.sel(
    lon=slice(
        reigeorge_lon[0],
        reigeorge_lon[1]), 
    lat=slice(
        reigeorge_lat[0],
        reigeorge_lat[1])
)


fig, ax = plt.subplots()

# Creating specific variables to customize the map
parallels = nc2.lat.values
meridians = nc2.lon.values

# Defining map settings
m = Basemap (projection='merc',
             llcrnrlat=-63.02, urcrnrlat=-60.98, 
             llcrnrlon=-60.01, urcrnrlon=-56.98, 
             resolution='f', area_thresh=0, ax=ax)
            # resolution -> 'c'=crude, 'l'=low, 'i'=intermediate, 'h'=high and 'f'=full

m.drawcoastlines(linewidth=0.5)
m.drawmapboundary()

m.fillcontinents(color='gray')


m.drawparallels(parallels, labels=[True, True, False, False], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999)
m.drawmeridians(meridians, labels=[False, False, True, True], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999, rotation=45)


lon, lat = np.meshgrid(nc2.lon.values, nc2.lat.values)

# Setting coordinate variables for this especific map
x, y = m(lon, lat)

plt.pcolor(x, y, nc2.tco3[0])
plt.scatter(x, y, c=nc2.tco3[0], zorder=99)

plt.colorbar()

plt.show()

# Spatial mean
nc2 = nc2.mean(dim=['lon', 'lat'], keep_attrs=True)

# Transforming the xr.Dataset into a pd.DataFrame
df2 = nc2.to_dataframe()

# Renaming columns to retain long_name and units info
df2.rename(index=str, columns=column_names, inplace=True)

df2.index = pd.to_datetime(df2.index, yearfirst=True)

df2 = df2.groupby([df2.index.year, df2.index.month]).mean()

df2.index.names = ['', ''] 

df2 = df2.unstack()

# Saving
df2.to_csv(
    os.path.join(
        '/home/douglasnehme/Desktop/bia/arquivos/',
        '20thC_ReanV3_reigeorge.csv'
))
