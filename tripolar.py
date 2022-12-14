#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 23:17:33 2022

@author: coqueiro
"""

#importando bibliotecas
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.colors 
import metpy.calc as mpcalc
from metpy.units import units
import numpy as np
import xarray as xr
import cartopy.io.shapereader as shpreader # Import shapefiles
from datetime import datetime, timedelta  # basicas datas e tipos de tempo
import cmocean

#dataset
file_1 = xr.open_dataset(
    '/home/ladsin/Downloads/GFS_analise_11_13.nc4'
    ).metpy.parse_cf()

file_1 = file_1.assign_coords(dict(
    longitude = (((file_1.longitude.values + 180) % 360) - 180))
    ).sortby('longitude')

#
#extent
lon_0 = -120.
lon_1 = -20.
lat_0 = 10.
lat_1 = -55.

lon_slice = slice(lon_0, lon_1)
lat_slice = slice(lat_0, lat_1)

#pega as lat/lon
lats = file_1.latitude.sel(latitude=lat_slice).values
lons = file_1.longitude.sel(longitude=lon_slice).values

#seta as variaveis
level_2 = 500 * units('hPa')
level_1 = 250 * units('hPa')

# cria uma escala de cores:
colors = ["#0000CD","#FF0000"]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap.set_over("#FF0000")
cmap.set_under("#0000CD")


for i in range(len(file_1.variables['time'])):
    
    geopotencial = file_1.Geopotential_height_isobaric.metpy.sel(
        time = file_1.time[i], 
        vertical=level_2, 
        latitude=lat_slice, 
        longitude=lon_slice
        ).metpy.unit_array.squeeze()
    
    u = file_1['u-component_of_wind_isobaric'].metpy.sel(
        time = file_1.time[i], 
        vertical=level_1, 
        latitude=lat_slice, 
        longitude=lon_slice
        ).metpy.unit_array.squeeze()
    
    v = file_1['v-component_of_wind_isobaric'].metpy.sel(
        time = file_1.time[i], 
        vertical=level_1, 
        latitude=lat_slice, 
        longitude=lon_slice
        ).metpy.unit_array.squeeze()
    
    pnmm = file_1.Pressure_reduced_to_MSL_msl.metpy.sel(
        time = file_1.time[i], 
        latitude=lat_slice, 
        longitude=lon_slice
        ).metpy.unit_array.squeeze()* 0.01 * units.hPa/units.Pa
    
    mag = np.sqrt(u**2+v**2)
    
    #data
    vtime = file_1.time.data[i].astype('datetime64[ms]').astype('O')
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a proje????o da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    gl = ax.gridlines(crs=ccrs.PlateCarree(),
                      color='gray',
                      alpha=1.0, 
                      linestyle='--', 
                      linewidth=0.5, 
                      xlocs=np.arange(-180, 180, 10), 
                      ylocs=np.arange(-90, 90, 10), 
                      draw_labels=True
                      )
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 29, 'color': 'black'}
    gl.ylabel_style = {'size': 29, 'color': 'black'}
    
    
    # intevalos da pnmm
    intervalo_min2 = np.amin(np.array(pnmm))
    intervalo_max2 = np.amax(np.array(pnmm))
    interval_2 = 2              # de quanto em quanto voce quer que varie
    levels_2 = np.arange(intervalo_min2, intervalo_max2, interval_2)
    
    # intevalos do jato
    intervalo_min3 = 30
    intervalo_max3 = 110
    interval_3 = 10              # de quanto em quanto voce quer que varie
    levels_3 = np.arange(intervalo_min3, intervalo_max3, interval_3)
    
    # intevalos da geopotencial
    intervalo_min1 = np.amin(np.array(geopotencial))
    intervalo_max1 = np.amax(np.array(geopotencial))
    interval_1 = 50              # de quanto em quanto voce quer que varie
    levels_1 = np.arange(intervalo_min1, intervalo_max1, interval_1)

    
    # corrente de jato
    jato = plt.contourf(lons,
                       lats, 
                       mag, 
                       cmap=cmocean.cm.deep, 
                       levels = levels_3, 
                       extend='neither')

    #plota a imagem pressao
    pressao = ax.contour(lons,
                          lats, 
                          pnmm, 
                          colors='black', 
                          linewidths=2, 
                          levels=levels_2
                          )
    
    ax.clabel(pressao, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=20, 
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    # plota a imagem geopotencial
    geopot = ax.contour(lons,
                          lats, 
                          geopotencial,
                          cmap=cmap, 
                          linewidths=3, 
                          linestyles='dashed',
                          levels=levels_1
                          )
    
    # ax.clabel(geopot, 
    #           inline = 1, 
    #           inline_spacing = 1, 
    #           fontsize=24,
    #           fmt = '%3.0f', 
    #           colors= 'black'
    #           )

    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        '/work/archive/Everson/Coqueiro/script_gfs/GFS-analysis_and_forecast-main/shapefiles/BR_UF_2021/BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.add_feature(cfeature.LAND)
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(jato, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
   
    # Add a title
    plt.title('Pnmm (black), Geop.500 (red/blue), Jato 250 (shaded)',
              fontweight='bold', 
              fontsize=28, 
              loc='left'
              )
    
    #previsao
    plt.title('Valid Time: {}'.format(vtime), fontsize=20, loc='right')
    #analise
    #plt.title('An??lise: {}'.format(vtime), fontsize=35, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'/work/archive/Everson/Coqueiro/Estagio/plots/tripolar/tripolar_250_{vtime}.png', bbox_inches='tight')