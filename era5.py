# -*- coding: utf-8 -*-
#
# AUTOR: Douglas Medeiros Nehme
#
# CONTACT: medeiros.douglas3@gmail.com
#
# CRIATION: mar/2017
#
# LAST MODIFICATION: mar/2017
#
# OBJECTIVE: Master Study Area Map

import os
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as PathEffects # Handle text effects, in this case, background color

# from cmocean import cm # Oceanography ColorMap - http://matplotlib.org/cmocean/
from netCDF4 import Dataset
from datetime import datetime
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


start = datetime.now().replace(microsecond = 0)
##################################################################################################################################
#### CONFIG PARAMETERS AND GLOBAL VARIABLES ######################################################################################
##################################################################################################################################
# pep-8 conventions suggest upper case for global variables
ROOTDIR = os.path.expanduser('~/Desktop/bia/arquivos/')


mpl.rcParams['figure.figsize'] = (12, 8)
mpl.rcParams['figure.autolayout'] = True # Similar of fig.tight_layout()

mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight' # Don't cut nothing in the figure saved
mpl.rcParams['savefig.format'] = 'jpeg'


# m_lat = (-30.0, -15.0)
# m_lon = (-51.0, -30.0)

##################################################################################################################################
#### IMPORTING AND MANIPULATING ALL TIME SERIES ##################################################################################
##################################################################################################################################

# Openning the netCDF archive
nc = xr.open_dataset(os.path.join(ROOTDIR, 'era5.nc'))

column_names = {}

for var in nc.variables.keys():
    try:
        # nc.coords.keys().index(var)
        ['latitude', 'longitude', 'time'].index(var)
    
    except:

        column_names[var] = nc[var].long_name.replace(' ', '_') + '-(' + nc[var].units.replace(' ', '.') + ')'


##################################################################################################################################
#### PLOTTING DATA ###############################################################################################################
##################################################################################################################################

fig, ax = plt.subplots()

shetland_lat = (-63.5, -61.8)
shetland_lon = (-63.1, -57.4)

nc1 = nc.sel(
    longitude=slice(
        shetland_lon[0],
        shetland_lon[1]), 
    latitude=slice(
        shetland_lat[1],
        shetland_lat[0])
)

# Creating specific variables to customize the map
# parallels = np.arange(shetland_lat[0], shetland_lat[1] + 0.5, 0.5)
# meridians = np.arange(shetland_lon[0], shetland_lon[1] + 1, 1)
parallels = nc1.latitude.values
meridians = nc1.longitude.values

# Defining map settings
m = Basemap (projection='merc',
             llcrnrlat=shetland_lat[0] - 0.001, urcrnrlat=shetland_lat[1] + 0.001, 
             llcrnrlon=shetland_lon[0] - 0.001, urcrnrlon=shetland_lon[1] + 0.001, 
             resolution='f', area_thresh=0, ax=ax)
            # resolution -> 'c'=crude, 'l'=low, 'i'=intermediate, 'h'=high and 'f'=full

# m.drawstates(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary()

m.fillcontinents(color='gray')


m.drawparallels(parallels, labels=[True, True, False, False], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999)
m.drawmeridians(meridians, labels=[False, False, True, True], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999, rotation=45)

# m.drawmapscale(-48.7, -16, -40, -22, 400, barstyle = 'fancy', zorder = 3)
# # os dois primeiros argumentos se referem a posição da escala no mapa
# # os dois seguintes se referem a latitude e longitude central para cálculo da escala no mapa
# # o quarto argumento se refere ao tamanho, em Km, da escala
# # o quinto argumento se refere ao estilo.

# # Plotting zonal section in 22°S
# m.plot([-40.46, -39., -39], [-22., -22., -22.], '-',
#        color='r', linewidth=4, latlon=True, zorder=3)

# Because our lon and lat variables are 1D, use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.

lon, lat = np.meshgrid(nc1.longitude.values, nc1.latitude.values)

# Setting coordinate variables for this especific map
x, y = m(lon, lat)

plt.pcolor(x, y, nc1.tco3[0])
plt.scatter(x, y, c=nc1.tco3[0])

plt.colorbar()

# Spatial mean
nc1 = nc1.mean(dim=['longitude', 'latitude'], keep_attrs=True)

# Transforming the xr.Dataset into a pd.DataFrame
df1 = nc1.to_dataframe()

# Renaming columns to retain long_name and units info
df1.rename(index=str, columns=column_names, inplace=True)

# Saving
df1.to_csv(os.path.join(ROOTDIR, 'era5_shetland.csv'))





fig, ax = plt.subplots()

reigeorge_lat = (-62.5, -61.8)
reigeorge_lon = (-59.3, -57.4)

nc2 = nc.sel(
    longitude=slice(
        reigeorge_lon[0],
        reigeorge_lon[1]), 
    latitude=slice(
        reigeorge_lat[1],
        reigeorge_lat[0])
)


# Creating specific variables to customize the map
# parallels = np.arange(reigeorge_lat[0], reigeorge_lat[1] + 0.5, 0.5)
# meridians = np.arange(reigeorge_lon[0], reigeorge_lon[1] + 1, 1)
parallels = nc2.latitude.values
meridians = nc2.longitude.values

# Defining map settings
m = Basemap (projection='merc',
             llcrnrlat=reigeorge_lat[0] - 0.001, urcrnrlat=reigeorge_lat[1] + 0.001, 
             llcrnrlon=reigeorge_lon[0] - 0.001, urcrnrlon=reigeorge_lon[1] + 0.001, 
             resolution='f', area_thresh=0, ax=ax)
            # resolution -> 'c'=crude, 'l'=low, 'i'=intermediate, 'h'=high and 'f'=full

# m.drawstates(linewidth=0.5)
m.drawcoastlines(linewidth=0.5)
m.drawmapboundary()

m.fillcontinents(color='gray')


m.drawparallels(parallels, labels=[True, True, False, False], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999)
m.drawmeridians(meridians, labels=[False, False, True, True], color='k',
                linewidth=0.5, fontweight='bold', fontsize=10, zorder=999, rotation=45)

# m.drawmapscale(-48.7, -16, -40, -22, 400, barstyle = 'fancy', zorder = 3)
# # os dois primeiros argumentos se referem a posição da escala no mapa
# # os dois seguintes se referem a latitude e longitude central para cálculo da escala no mapa
# # o quarto argumento se refere ao tamanho, em Km, da escala
# # o quinto argumento se refere ao estilo.

# # Plotting zonal section in 22°S
# m.plot([-40.46, -39., -39], [-22., -22., -22.], '-',
#        color='r', linewidth=4, latlon=True, zorder=3)

# Because our lon and lat variables are 1D, use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.

# lon, lat = np.meshgrid(nc.longitude.values, nc.latitude.values)
lon, lat = np.meshgrid(nc2.longitude.values, nc2.latitude.values)

# Setting coordinate variables for this especific map
x, y = m(lon, lat)


plt.pcolor(x, y, nc2.tco3[0])
plt.scatter(x, y, c=nc2.tco3[0])

plt.colorbar()

# Spatial mean
nc2 = nc2.mean(dim=['longitude', 'latitude'], keep_attrs=True)

# Keep only datetime part that is varing
nc1['time'] = nc1.indexes['time'].normalize()

# Transforming the xr.Dataset into a pd.DataFrame
df2 = nc2.to_dataframe()

# Renaming columns to retain long_name and units info
df2.rename(index=str, columns=column_names, inplace=True)

# Saving
df2.to_csv(os.path.join(ROOTDIR, 'era5_reigeorge.csv'))


plt.show()


# # pad keyword controls colorbar's horizontal position. Default is 0.05 if vertical, 0.15 if horizontal
# cbar = plt.colorbar(pad=0.015)
# # labelpad keyword controls colorbar label's horizontal position
# cbar.ax.set_ylabel('Profundidade (m)', labelpad=15, fontweight='bold', fontsize=16)
# cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=16)


# isobaths = plt.contour(x, y, z, [-6000, -5000, -4000, -3000, -2000, -1000, -100, -50],
#                        colors='k', linewidths=0.5, linestyles='solid')

# isobaths_labels = plt.clabel(isobaths, fmt='%i', fontsize=16)

# plt.setp(isobaths_labels, path_effects=[PathEffects.withStroke(linewidth=2, foreground="w")]) # creats a white backgraound on
# isobaths_labels


# ##### Adding Global Map ####
# axin = inset_axes(ax, width="30%", height="30%", loc=1)

# global_map = Basemap(projection='ortho', lon_0=-50, lat_0=-13,
#                      ax=axin, anchor='NE')

# global_map.drawcountries(color='white')
# # Dashes represents the distance between two dashes markes in parallels and meridians, it's default values are [1, 1]. I change it to
# # [0.01 , 0.01], beacause I want solid line style for this and how 0.01 of distance is small it become equal of solid lines.
# global_map.drawparallels(np.arange(-80, 80, 20), dashes=[0.01, 0.01], linewidth=0.3, color='gray')
# global_map.drawmeridians(np.arange(-180, 30, 20), dashes=[0.01, 0.01], linewidth=0.3, color='gray')

# global_map.fillcontinents(color='gray')

# bx, by = global_map(m.boundarylons, m.boundarylats)

# xy = list(zip(bx, by)) # Getting biggest map's corners positions (lon and lat) to draw the polygon above

# mapboundary = Polygon(xy, facecolor='red', edgecolor='r', linewidth=1, alpha=0.3)

# global_map.ax.add_patch(mapboundary)


# plt.savefig(os.path.join(FIGDIR, 'area_de_estudo'))
# plt.close('all')


# stop = datetime.now().replace(microsecond=0)

# print 'Time taken to execute program: {}'.format(stop - start)
