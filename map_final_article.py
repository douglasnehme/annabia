# -*- coding: utf-8 -*-
#
# AUTOR: Douglas Medeiros Nehme
#
# CONTACT: medeiros.douglas3@gmail.com
#
# CRIATION: may/2017
#
# LAST MODIFICATION: may/2017
#
# OBJECTIVE: Bia's Master Study Area Map

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

##################################################################################################################################
#### CONFIG PARAMETERS AND GLOBAL VARIABLES ######################################################################################
##################################################################################################################################
# pep-8 conventions suggest upper case for global variables
ROOTDIR = '/home/dnehme/Desktop/bia/arquivos'


METADICT = {
'lago'           : { 'lon': -58.88, 'lat': -62.183, 'name': 'Profound Lake'           },
'bellingshausen' : { 'lon': -59.  , 'lat': -62.2  , 'name': 'Bellingshausen'          },
'marion'         : { 'lon': 37.9  , 'lat': -46.9  , 'name': 'Marion Island'           },
'amsterdam'      : { 'lon': 77.5  , 'lat': -37.8  , 'name': 'Ile Nouvelle\nAmsterdam' },
'hobart'         : { 'lon': 147.3 , 'lat': -42.9  , 'name': 'Hobart'                  },
'christchurch'   : { 'lon': 172.6 , 'lat': -43.5  , 'name': 'Christchurch'            },
'puerto_montt'   : { 'lon': -73.1 , 'lat': -39.6  , 'name': 'Puerto\nMontt'           },
'gough'          : { 'lon': -9.9  , 'lat': -40.4  , 'name': 'Gough Island'            },
'novolazara'     : { 'lon': 11.8  , 'lat': -70.8  , 'name': 'Novolazarevskaya'        },
'mawson'         : { 'lon': 62.9  , 'lat': -67.6  , 'name': 'Mawson'                  },
'mirny'          : { 'lon': 93.0  , 'lat': -66.6  , 'name': 'Mirny'                   },
'casey'          : { 'lon': 110.5 , 'lat': -66.3  , 'name': 'Casey'                   },
'dumont'         : { 'lon': 140.0 , 'lat': -66.7  , 'name': u'Dumont D’urville'       },
'faraday'        : { 'lon': -64.3 , 'lat': -65.2  , 'name': 'Faraday'                 },
'vernadsky'      : { 'lon': -64.25, 'lat': -65.25 , 'name': 'Vernadsky'               },
'palmer'         : { 'lon': -64.05, 'lat': -64.767, 'name': 'Palmer'                  },
}


mpl.rcParams['font.weight'] = 'bold'
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.labelweight'] = 'bold'
mpl.rcParams['axes.labelsize'] = 12

mpl.rcParams['figure.figsize'] = (12, 8)
mpl.rcParams['figure.autolayout'] = True # Similar of fig.tight_layout()

mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['savefig.bbox'] = 'tight' # Don't cut nothing in the figure saved
mpl.rcParams['savefig.format'] = 'jpeg'

##################################################################################################################################
#### PLOTTING RIGHT MAP ##########################################################################################################
##################################################################################################################################

merra2_lon = (-63.30, -63.30, -58.00, -58.00)
merra2_lat = (-63.00, -62.00, -62.00, -63.00)
twenty_lon = (-59.00, -59.00, -58.00, -58.00)
twenty_lat = (-63.00, -62.00, -62.00, -63.00)
era5_lon = (-59.30, -59.30, -57.40, -57.40)
era5_lat = (-62.50, -61.80, -61.80, -62.50)

fig, [ax1, ax2] = plt.subplots(nrows = 1, ncols = 2)

# setup lambert azimuthal equal area basemap.
# lat_ts is latitude of true scale.
# lon_0,lat_0 is central point.

lat_0, lon_0 = -62.5, -60.5

m2 = Basemap(width = 330000, height = 220000, resolution = 'f', projection = 'laea',
            lat_ts = lat_0, lat_0 = lat_0, lon_0 = lon_0, ax = ax2)

m2.drawparallels(np.arange(-63.5, -61.5, 0.5), labels = [False, True, False, False], 
                color = 'gray', linewidth = 0)
m2.drawmeridians(np.arange(-63.5, -57.0, 1.0), labels = [False, False, True, True],
                color = 'gray', linewidth = 0)


m2.drawcoastlines(linewidth = 0.5, zorder = 1)
m2.fillcontinents(color = 'silver', zorder = 1)

m2.drawmapscale(-58, -63.3, lat_0, lon_0, 60, barstyle = 'fancy')
# os dois primeiros argumentos se referem a posição da escala no mapa
# os dois seguintes se referem a latitude e longitude central para cálculo do mapa
# o quarto argumento se refere ao tamanho, em Km da escala
# o quinto argumento se refere ao estilo.



m2.scatter(METADICT['lago']['lon'], METADICT['lago']['lat'],
          s = 35, latlon = True, marker = '^', color = 'k', linewidths = 1.5, zorder = 3)

ax2.annotate('(b)', (0.01, 0.95), xycoords = 'axes fraction', fontsize = 12)

ax2.annotate(u'KGI', (0.9, 0.755), xycoords = 'axes fraction', color = 'k',
              fontsize = 10, horizontalalignment = 'center', zorder = 4)

ax2.annotate(METADICT['lago']['name'], (0.865, 0.555), xycoords = 'axes fraction', horizontalalignment = 'center')

ax2.annotate(METADICT['bellingshausen']['name'], (0.63, 0.65), xycoords = 'axes fraction', horizontalalignment = 'center')


m2.plot([-58.86, -58.76], [-62.22, -62.315], color = 'k', linewidth = 1, latlon = True, zorder = 3)


# mx, my = m2(merra2_lon, merra2_lat)
# mxy = list(zip(mx, my))
mxy = [
    (23698.10185438237, 51957.97097811287),
    (23698.10185438237, 163074.8576896538),
    (295473.6435049328, 163074.8576896538),
    (295473.6435049328, 51957.97097811287)]

merra_polygon = Polygon(
    mxy,
    edgecolor='r',
    linewidth=1.25,
    fill=False,
    zorder=3)
m2.ax.add_patch(merra_polygon)

# tx, ty = m2(twenty_lon, twenty_lat)
# txy = list(zip(tx, ty))
txy = [
    (243297.5020316471, 53522.56142991928),
    (243297.5020316471, 164689.1333857780),
    (298473.6435049328, 164689.1333857780),
    (298473.6435049328, 53522.56142991928)]
twenty_polygon = Polygon(
    txy,
    edgecolor='g',
    linewidth=1.25,
    fill=False,
    zorder=3)
m2.ax.add_patch(twenty_polygon)

# ex, ey = m2(era5_lon, era5_lat)
# exy = list(zip(ex, ey))
exy = [
    (228051.5885396924, 109427.70710035652),
    (228051.5885396924, 187251.16695777007),
    (327826.7655075394, 187251.16695777007),
    (327826.7655075394, 109427.70710035652)]
era5_polygon = Polygon(
    exy,
    edgecolor='b',
    linewidth=1.25,
    fill=False,
    zorder=3)
m2.ax.add_patch(era5_polygon)

##################################################################################################################################
#### PLOTTING LEFT MAP ###########################################################################################################
##################################################################################################################################
# setup lambert azimuthal equal area basemap.
# lat_ts is latitude of true scale.
# lon_0,lat_0 is central point.

m1 = Basemap(width = 12000000, height = 12000000, resolution = 'h', projection = 'laea',
             lat_ts = -60, lat_0 = -90, lon_0 = 0, ax = ax1)

m1.drawparallels(np.arange(-80.,81.,20), labels = [False, False, False, False], dashes = [0.01, 0.01], color = 'gray', zorder = 1)
m1.drawmeridians(np.arange(-180.,181.,20), labels = [False, False, True, True], dashes = [0.01, 0.01], color = 'gray', zorder = 1)
# Dashes represents the distance between two dashes markes in parallels and meridians, it's default values are [1, 1]. I change it
# to [0.01 , 0.01], beacause I want solid line style for this and how 0.01 of distance is small it become equal of solid lines.

m1.fillcontinents(color = 'silver', zorder = 2)

bx, by = m1(m2.boundarylons, m2.boundarylats)

xy = list(zip(bx, by)) # Getting right map's corners positions (lon and lat) to draw the polygon above

mapboundary = Polygon(xy, facecolor='k', edgecolor = 'k', linewidth = 1, alpha = 0.3, fill = False, hatch = 'xxxxxxxx', zorder = 3)

m1.ax.add_patch(mapboundary)


m1.scatter(METADICT['faraday']['lon'], METADICT['faraday']['lat'],
          s = 10, latlon = True, marker = 'o', color = 'g', linewidths = 1.5, zorder = 4)

m1.scatter(METADICT['vernadsky']['lon'], METADICT['vernadsky']['lat'],
          s = 65, latlon = True, marker = 's', color = 'k', linewidths = 1.5, zorder = 3)

m1.scatter(METADICT['palmer']['lon'], METADICT['palmer']['lat'],
          s = 55, latlon = True, marker = '*', color = 'r', linewidths = 1.5, zorder = 3)

m1.scatter([ METADICT['marion']['lon'],       METADICT['amsterdam']['lon'], METADICT['hobart']['lon'],
            METADICT['christchurch']['lon'], METADICT['puerto_montt']['lon'],  METADICT['gough']['lon'],
            METADICT['novolazara']['lon'],   METADICT['mawson']['lon'],    METADICT['mirny']['lon'],
            METADICT['casey']['lon'],        METADICT['dumont']['lon'] ],

          [ METADICT['marion']['lat'],       METADICT['amsterdam']['lat'], METADICT['hobart']['lat'],
            METADICT['christchurch']['lat'], METADICT['puerto_montt']['lat'],  METADICT['gough']['lat'],
            METADICT['novolazara']['lat'],   METADICT['mawson']['lat'],    METADICT['mirny']['lat'],
            METADICT['casey']['lat'],        METADICT['dumont']['lat'] ],
          s = 55, latlon = True, marker = 'P', color = 'k', linewidths = 1.5, zorder = 3)


ax1.annotate('(a)', (0.01, 0.97), xycoords = 'axes fraction', fontsize = 12)

ax1.annotate(METADICT['marion']['name'], (0.85, 0.8), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['amsterdam']['name'], (0.91, 0.63), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['hobart']['name'], (0.72, 0.165), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['christchurch']['name'], (0.45, 0.08), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['puerto_montt']['name'], (0.07, 0.565), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['gough']['name'], (0.35, 0.9), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['novolazara']['name'], (0.58, 0.70), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['mawson']['name'], (0.76, 0.59), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['mirny']['name'], (0.775, 0.485), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['casey']['name'], (0.765, 0.415), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['dumont']['name'], (0.775, 0.32), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['faraday']['name'], (0.375, 0.6), color='g', xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['vernadsky']['name'], (0.22, 0.56), xycoords = 'axes fraction', horizontalalignment = 'center')

ax1.annotate(METADICT['palmer']['name'], (0.375, 0.56), color='r', xycoords = 'axes fraction', horizontalalignment = 'center')


plt.savefig(os.path.join(ROOTDIR, u'map_data_distribuition_article'))
plt.close('all')