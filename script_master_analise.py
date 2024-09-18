#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 23:34:26 2022

@author: everson
"""

###################### Importando bibliotecas ############################
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.colors 
import metpy.calc as mpcalc
from metpy.units import units
import numpy as np
import xarray as xr
import cartopy.io.shapereader as shpreader # Import shapefiles
import cmocean
import matplotlib.colors as mcolors

# ignora avisos
import warnings
warnings.filterwarnings("ignore")

#%%

# Aviso: Lembre de trocar para seu próprio diretório e instalar corretamente as bibliotecas

# Aviso 2: Para baixar o Shapefile do Brasil, acesse: 
# https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html
# e clique em unidades da Federação

#%%

############################ Dataset ###################################
file_1 = xr.open_mfdataset(
    r'D:\es2\dados\analise\GFS_Global_0p25deg_ana_20240916_1800.grib2.nc4'
    ).metpy.parse_cf()

# Converte longitude
file_1 = file_1.assign_coords(dict(
    longitude = (((file_1.longitude.values + 180) % 360) - 180))
    ).sortby('longitude')

# Extensão (Extent)
lon_slice = slice(-120., -20.)
lat_slice = slice(15., -65.)
lon_slice_2 = slice(-120., -20.,15)
lat_slice_2 = slice(15., -65.,15)

# Seleciona as latitudes e longitudes
lats = file_1.latitude.sel(latitude=lat_slice).values
lons = file_1.longitude.sel(longitude=lon_slice).values
lats_2 = file_1.latitude.sel(latitude=lat_slice_2).values
lons_2 = file_1.longitude.sel(longitude=lon_slice_2).values

#%%

#################### Seleciona os niveis em Z #########################
level_1 = 1000 * units('hPa')
level_2 = 500 * units('hPa')
level_3 = 850 * units('hPa')
level_4 = 250 * units('hPa') 
level_5 = 200 * units('hPa')
level_6 = 925 * units('hPa')

#################### Atribui DX e DY ###################################
dx, dy = mpcalc.lat_lon_grid_deltas(lons, lats)

#%%

######################### Escalas de cores ##############################

# Linhas geopotencial em 500 hPa
colors = ["#0000CD","#FF0000"]
cmap_1 = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap_1.set_over("#FF0000")
cmap_1.set_under("#0000CD")

# Espessura
colors = ["#2d001c", "#5b0351", "#780777", "#480a5e", "#1e1552", 
          "#1f337d", "#214c9f", "#2776c6", "#2fa5f1", "#1bad1d", 
          "#8ad900", "#ffec00", "#ffab00", "#f46300", "#de3b00", 
          "#ab1900", "#6b0200", '#3c0000']

cmap_2 = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
cmap_2.set_over('#3c0000')
cmap_2.set_under('#28000a')

# Umidade especifica
# define os intervalos da legenda
clevs = np.array([2, 4, 6, 8, 10, 12, 14, 16, 18])

# lista de cores, em ordem crescete. RGBA
colors = np.array([ # (R, G, B, A)
    [242, 98, 0, 255],
    [249, 155, 77, 255],
    [254, 217, 118, 255],
    [255, 247, 188, 255],
    [190, 220, 230, 255],
    [156, 194, 255, 255],
    [59, 118, 255, 255],
    [0, 77, 182, 255]
]) / 255 # divide por 255

# cria um novo cmap a partir do pre-existente
cmap_3 = mcolors.LinearSegmentedColormap.from_list(
    'specific humidity cmap', colors, clevs.shape[0] - 1)
cmap_3.set_over(np.array([0, 37, 89, 255])/255)
cmap_3.set_under('white')

# nromaliza com base nos intervalos
norm = mcolors.BoundaryNorm(clevs, cmap_3.N) # usado no PColorMesh

#%%

################### Looping do calculos ###############################
for i in range(len(file_1.variables['time'])):
    
    args_0 = dict(
        time = file_1.time[i], 
        latitude=lat_slice, 
        longitude=lon_slice
        )
    
    args_1 = dict(
        time = file_1.time[i], 
        latitude=lat_slice, 
        longitude=lon_slice
        )
    
    args_2 = dict(
        time = file_1.time[i], 
        vertical=level_2, 
        latitude=lat_slice, 
        longitude=lon_slice
        )
    
    args_3 = dict(
        time = file_1.time[i], 
        vertical = level_3, 
        latitude = lat_slice, 
        longitude = lon_slice
        )
    
    args_4 = dict(
        time = file_1.time[i], 
        vertical=level_3, 
        latitude=lat_slice_2, 
        longitude=lon_slice_2
        )
    
    args_5 = dict(
        time = file_1.time[i], 
        vertical=level_4, 
        latitude=lat_slice, 
        longitude=lon_slice)
    
    args_6 = dict(
        time = file_1.time[i], 
        vertical=level_1,
        latitude=lat_slice, 
        longitude=lon_slice
        )
    
    args_7 = dict(
        time = file_1.time[i], 
        vertical=level_5, 
        latitude=lat_slice, 
        longitude=lon_slice)
    
    args_8 = dict(
        time = file_1.time[i], 
        vertical=level_6, 
        latitude=lat_slice, 
        longitude=lon_slice)
    
    args_9 = dict(
        time = file_1.time[i], 
        vertical=level_1, 
        latitude=lat_slice, 
        longitude=lon_slice)

#%%
    ################# Variáveis #################

    # Geopotencial em 1000 hPa (Adv. temp e vort)
    geopotencial_1000 = file_1.Geopotential_height_isobaric.metpy.sel(**args_6).metpy.unit_array.squeeze()
    
    # Geopotencial em 500 hPa (Adv. temp e vort)
    geopotencial_500 = file_1.Geopotential_height_isobaric.metpy.sel(**args_2).metpy.unit_array.squeeze()
    
    # Componente U em 850 hPa (Adv. temp e vort)
    u_500 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_2).metpy.unit_array.squeeze().to('kt')
    
    # Componente V em 850 hPa (Adv. temp e vort)
    v_500 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_2).metpy.unit_array.squeeze().to('kt')
    
    # Componente U em 850 hPa (Adv. temp e vort)
    u_850 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_3).metpy.unit_array.squeeze().to('kt')
    
    # Componente V em 850 hPa (Adv. temp e vort)
    v_850 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_3).metpy.unit_array.squeeze().to('kt')
    
    # Componete U_2 em 850 hPa (Adv. temp e vort)
    u_850_2 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_4).metpy.unit_array.squeeze().to('kt')
    
    # Componente V_2 em 850 hPa (Adv. temp e vort)
    v_850_2 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_4).metpy.unit_array.squeeze().to('kt')
    
    # Componente U em 1000 hPa (Vort rel 1000)
    u_1000 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_6).metpy.unit_array.squeeze()
    
    # Componente V em 1000 hPa (Vort rel 1000)
    v_1000 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_6).metpy.unit_array.squeeze()
    
    # Componente U em 250 hPa (Corrente de jato 250)
    u_250 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_5).metpy.unit_array.squeeze()
    
    # Componente V em 250 hPa (Corrente de jato 250)
    v_250 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_5).metpy.unit_array.squeeze()
    
    # Componente U em 200 hPa (Corrente de jato 200)
    u_200 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_7).metpy.unit_array.squeeze()
    
    # Componente V em 200 hPa (Corrente de jato 200)
    v_200 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_7).metpy.unit_array.squeeze()
    
    # Componente U em 925 hPa
    u_925 = file_1['u-component_of_wind_isobaric'].metpy.sel(**args_8).metpy.unit_array.squeeze()
    
    # Componente V em 925 hPa
    v_925 = file_1['v-component_of_wind_isobaric'].metpy.sel(**args_8).metpy.unit_array.squeeze()
    
    # Pressão ao nivel medio do mar
    pnmm = file_1.Pressure_reduced_to_MSL_msl.metpy.sel(**args_1).metpy.unit_array.squeeze()* 0.01 * units.hPa/units.Pa
    
    # Temperatura em 850 hPa
    temp = file_1.Temperature_isobaric.metpy.sel(**args_3).metpy.unit_array.squeeze().to('degC')
    
    # Umidade Relativa
    umi_rel_1000 = file_1.Relative_humidity_isobaric.metpy.sel(**args_9).metpy.unit_array.squeeze()
    
    # Umidade especifica
    q = file_1.Specific_humidity_isobaric.metpy.sel(**args_3).metpy.unit_array.squeeze()* 1e3
    
    # Movimento Vertical (Omega)
    omega = file_1.Vertical_velocity_pressure_isobaric.metpy.sel(**args_2).metpy.unit_array.squeeze()

#%%
    ############################### DATA ######################################
    vtempo = file_1.time.data[i].astype('datetime64[ms]').astype('O') # Manter para Linux e trocar vtempo_str por vtempo
    vtempo_str = vtempo.strftime('%Y-%m-%d_%H-%M-%S')  # Formata a data e hora para Windows

#%%    
    ######################## Advecção de Temperatura ##########################
    
    ###################### Especificações do Plot #############################
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # Calculo Adv. de temperatura
    adv_temp = mpcalc.advection(temp, u = u_850, v = v_850, dx = dx, dy = dy, x_dim = -1, y_dim = -2) * 1000
    
    # Intevalos da adv de temp
    intervalo_min_1 = -2.5
    intervalo_max_1 = 2.6
    interval_1 = 0.1              # de quanto em quanto voce quer que varie
    levels_1 = np.arange(intervalo_min_1, intervalo_max_1, interval_1)
    
    # intevalos da geopotencial
    intervalo_min_2 = np.amin(np.array(geopotencial_500))
    intervalo_max_2 = np.amax(np.array(geopotencial_500))
    interval_2 = 50              # de quanto em quanto voce quer que varie
    levels_2 = np.arange(intervalo_min_2, intervalo_max_2, interval_2)

    # Plota a imagem adv de temp
    adv_temp_sombreado = ax.contourf(lons, 
                            lats, 
                            adv_temp, 
                            cmap='seismic', 
                            levels = levels_1, 
                            extend = 'neither'
                            )
    
    # Plota a imagem geopotencial
    geopotencial_500_contorno = ax.contour(lons,
                          lats, 
                          geopotencial_500,
                          cmap = cmap_1,
                          linewidths=3, 
                          linestyles='dashed',
                          levels=levels_2
                          )
    
    ax.clabel(geopotencial_500_contorno, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=24,
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    ax.streamplot(lons, 
                  lats, 
                  u_850, 
                  v_850, 
                  density=[4,4], 
                  linewidth=1.5, 
                  arrowsize=1.8,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
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
    barra_de_cores = plt.colorbar(adv_temp_sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
   
    # Add a title
    plt.title('Adveccao de temperatura (K/s) - 850 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    # Titulo da previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/adv_temp/adveccao_de_temperatura_{vtempo_str}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%    
    ######################### Advecção de vorticidade relativa negativa ##############################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # Calculo Adv. vorticidade relativa negativa
    vorticidade = mpcalc.vorticity(u_1000, v_1000, dx = dx, dy = dy, x_dim = -1, y_dim = -2)*10**5
    adv_vort = mpcalc.advection(vorticidade, u = u_500, v = v_500, dx = dx, dy = dy, x_dim = -1, y_dim = -2)*100
    
    # Intevalos da advecção de vorticidade
    intervalo_min_3 = -1.6
    intervalo_max_3 = 0
    interval_3 = 0.10
    levels_3 = np.arange(intervalo_min_3, intervalo_max_3, interval_3)
    
    # intevalos da geopotencial
    intervalo_min_4 = np.amin(np.array(geopotencial_500))
    intervalo_max_4 = np.amax(np.array(geopotencial_500))
    interval_4 = 50              # de quanto em quanto voce quer que varie
    levels_4 = np.arange(intervalo_min_4, intervalo_max_4, interval_4)

    # plota a imagem adv vorticidade
    adv_vort_sombreado = ax.contourf(lons, 
                            lats, 
                            adv_vort, 
                            cmap='gist_heat', 
                            levels = levels_3, 
                            extend = 'min'
                            )

    # plota a imagem geopotencial
    adv_vort_contorno = ax.contour(lons,
                            lats, 
                            geopotencial_500,
                            linestyle='--',
                            cmap=cmap_1, 
                            linewidths=3, 
                            levels=levels_4
                            )
    
    ax.clabel(adv_vort_contorno, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=24,
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    ax.streamplot(lons, 
                  lats, 
                  u_500, 
                  v_500, 
                  density=[4,4], 
                  linewidth=1.5, 
                  arrowsize=1.8,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
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
    barra_de_cores = plt.colorbar(adv_vort_sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('Adv de vort relativa (1/s²) - 500 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    # Titulo da Análise
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
   
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/adv_vorticidade/adveccao_de_vorticidade_{vtempo_str}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%    
    ################################### Corrente de jato 250 hPa ###################################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Defina os limites do gráfico para América do Sul
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # Calculo Corrente de jato 250 hPa
    mag_1 = np.sqrt(u_250**2+v_250**2)

    # intevalos da corrente de jato
    intervalo_min_5 = 30
    intervalo_max_5 = 90
    interval_5 = 10            # de quanto em quanto voce quer que varie
    levels_5 = np.arange(intervalo_min_5, intervalo_max_5, interval_5)
    
    # corrente de jato
    corrente_jato_sobreado = plt.contourf(lons,
                       lats, 
                       mag_1, 
                       cmap=cmocean.cm.amp, 
                       levels = levels_5, 
                       extend='both')
    
    ax.streamplot(lons, 
                  lats, 
                  u_250, 
                  v_250, 
                  density=[4,4], 
                  linewidth=1.5, 
                  arrowsize=1.8,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    # adiciona mascara de terra
    ax.add_feature(cfeature.LAND)
    
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(corrente_jato_sobreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    # Add a title
    plt.title('Corrente de jato (m/s) - 250 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/corrente_de_jato/corrente_de_jato_250_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%       
    ################################### Corrente de jato 200 hPa ###################################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # Calculo Corrente de jato 250 hPa
    mag_2 = np.sqrt(u_200**2+v_200**2)

    # intevalos da corrente de jato
    intervalo_min_6 = 30
    intervalo_max_6 = 90
    interval_6 = 10            # de quanto em quanto voce quer que varie
    levels_6 = np.arange(intervalo_min_6, intervalo_max_6, interval_6)
    
    # corrente de jato
    corrente_jato_sobreado = plt.contourf(lons,
                       lats, 
                       mag_2, 
                       cmap=cmocean.cm.amp, 
                       levels = levels_6, 
                       extend='both')
    
    ax.streamplot(lons, 
                  lats, 
                  u_200, 
                  v_200, 
                  density=[4,4], 
                  linewidth=1.5, 
                  arrowsize=1.8,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    # adiciona mascara de terra
    ax.add_feature(cfeature.LAND)
    
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(corrente_jato_sobreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    # Add a title
    plt.title('Corrente de jato (m/s) - 200 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/corrente_de_jato/corrente_de_jato_200_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%
    #################################### Divergencia ################################################
    
    ###################### Especificações do Plot #############################
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Defina os limites do gráfico para América do Sul
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
    
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
    
    
    # Calculo da divergencia
    divergencia = mpcalc.divergence(u_1000, v_1000, dx = dx, dy = dy, x_dim=- 1, y_dim=- 2) *  1e6
    
    # intevalos da divergencia - umidade
    divq_min_7 = -50
    divq_max_7 = -20
    interval_7 = 2              # de quanto em quanto voce quer que varie
    levels_7 = np.arange(divq_min_7, divq_max_7, interval_7)
    
    # plota a imagem divergencia
    div_sombreado = ax.contourf(lons, 
                            lats, 
                            divergencia, 
                            cmap = cmocean.cm.algae_r, 
                            levels = levels_7, 
                            extend = 'min'
                            )

    ax.streamplot(lons, lats, u_1000, v_1000, density=[4,4], linewidth=1.5, arrowsize=1.8, color='black', transform=ccrs.PlateCarree())

    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    #adiciona legenda 
    barra_de_cores = plt.colorbar(div_sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    

    
    # Add a title
    plt.title('Convergência em 1000hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    plt.subplots_adjust(right=0.85)  # Ajuste o valor conforme necessário (valor padrão é 0.8)
    
    plt.savefig(f'D:/es2/imagens/analise/divergencia/divergencia_{vtempo_str}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%
    #################################### Espessura ################################################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # Calculo da espessura
    espessura = geopotencial_500 - geopotencial_1000
    
    # intevalos da espessura
    intervalo_min_8 = 4900
    intervalo_max_8 = 5880
    interval_8 = 25             # de quanto em quanto voce quer que varie
    levels_8 = np.arange(intervalo_min_8, intervalo_max_8, interval_8)
    
    # intevalos da pnmm
    intervalo_min_9 = np.amin(np.array(pnmm))
    intervalo_max_9 = np.amax(np.array(pnmm))
    interval_9 = 2              # de quanto em quanto voce quer que varie
    levels_9 = np.arange(intervalo_min_9, intervalo_max_9, interval_9)
    
    # plota a imagem espessura
    espessura_sombreado = ax.contourf(lons, 
                            lats, 
                            espessura, 
                            cmap=cmap_2, 
                            levels = levels_8, 
                            extend = 'neither'
                            )
    
    # plota a imagem pressao
    espessura_contorno = ax.contour(lons,
                          lats, 
                          pnmm, 
                          colors='black', 
                          linewidths=2, 
                          levels=levels_9
                          )
    
    ax.clabel(espessura_contorno, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=20, 
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona mascara de terra
    ax.add_feature(cfeature.LAND)
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(espessura_sombreado,
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('Espessura (500-1000)hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/espessura/espessura_{vtempo_str}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%
    #################################### Vorticidade ################################################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # Calculo da vorticidade
    vorticidade_1000 = mpcalc.vorticity(u_1000, v_1000, dx = dx, dy = dy, x_dim = -1, y_dim = -2)*10**5
    
    # intevalos da pnmm
    intervalo_min_10 = np.amin(np.array(pnmm))
    intervalo_max_10 = np.amax(np.array(pnmm))
    interval_10 = 2              # de quanto em quanto voce quer que varie
    levels_10 = np.arange(intervalo_min_10, intervalo_max_10, interval_10)
    
    # intevalos da vorticidade
    intervalo_min_11 = -20
    intervalo_max_11 = -2
    interval_11 = 2             # de quanto em quanto voce quer que varie
    levels_11 = np.arange(intervalo_min_11, intervalo_max_11, interval_11)
    
    # adiciona mascara de terra
    ax.add_feature(cfeature.LAND)
    
    # plota a imagem da vorticidade
    vort_sombreado = ax.contourf(lons, 
                            lats, 
                            vorticidade_1000, 
                            cmap=cmocean.cm.dense_r, 
                            levels = levels_11, 
                            extend = 'min'
                            )
    
    # plota a imagem pressao
    pressao_contorno = ax.contour(lons,
                          lats, 
                          pnmm, 
                          colors='black', 
                          linewidths=2, 
                          levels=levels_10
                          )
    
    ax.clabel(pressao_contorno, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=20, 
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(vort_sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    # Add a title
    plt.title('Vorticidade relativa (1/s) - 1000 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/vorticidade/vorticidade_relativa_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()

#%%
    #################################### Umidade especifica ################################################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
   
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    # Defina os limites do gráfico para América do Sul
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # umidade especifica 
    umidade_sombreado = ax.contourf(lons, lats, q, cmap = cmap_3, levels = clevs, extend='both')
    ax.streamplot(lons, lats, u_850, v_850, density=[4,4], linewidth=1.5, arrowsize=1.8, color='black', transform=ccrs.PlateCarree())
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(umidade_sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('Umidade específica 850 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #analise
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    #--------------------------------------------------------------------------
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/umidade_especifica/umidade_especifica_850hPa_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    
#%%
    ########################## PNMM + escoamento em 925 hPa #####################################
    
    ###################### Especificações do Plot #############################

    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    intervalo_min_11 = np.amin(np.array(pnmm))
    intervalo_max_11 = np.amax(np.array(pnmm))
    interval_11 = 4              # de quanto em quanto voce quer que varie
    levels_11 = np.arange(intervalo_min_11, intervalo_max_11, interval_11)
    
    # Calculo vento em 925 hPa
    mag_925 = np.sqrt(u_925**2+v_925**2)
    
    # plota a imagem pressao
    pressao_shaded = ax.contourf(lons,
                          lats, 
                          pnmm, 
                          cmap='RdBu_r',
                          levels=levels_11,
                          extend='both'
                          )
    
    ax.streamplot(lons, 
                  lats, 
                  u_925, 
                  v_925, 
                  density=[4,4], 
                  linewidth=2, 
                  arrowsize=2.5,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(pressao_shaded, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('PNMM + Escoamento em 925 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/pnmm_v925/PNMM_vento_925_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()

#%%    
    #################### PNMM + escoamento em 500 hPa #############################
    
    ###################### Especificações do Plot #############################

    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    intervalo_min_11 = np.amin(np.array(pnmm))
    intervalo_max_11 = np.amax(np.array(pnmm))
    interval_11 = 4              # de quanto em quanto voce quer que varie
    levels_11 = np.arange(intervalo_min_11, intervalo_max_11, interval_11)
    
    # Calculo vento em 925 hPa
    mag_925 = np.sqrt(u_500**2+v_500**2)
    
    # plota a imagem pressao
    pressao_shaded = ax.contourf(lons,
                          lats, 
                          pnmm, 
                          cmap='RdBu_r',
                          levels=levels_11,
                          extend='both'
                          )
    
    ax.streamplot(lons, 
                  lats, 
                  u_500, 
                  v_500, 
                  density=[4,4], 
                  linewidth=2, 
                  arrowsize=2.5,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(pressao_shaded, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('PNMM + Escoamento em 500 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/pnmm_v500/PNMM_vento_500_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%
    ##################### PNMM + escoamento em 250 hPa ##################################
    
    ###################### Especificações do Plot #############################

    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    intervalo_min_11 = np.amin(np.array(pnmm))
    intervalo_max_11 = np.amax(np.array(pnmm))
    interval_11 = 4              # de quanto em quanto voce quer que varie
    levels_11 = np.arange(intervalo_min_11, intervalo_max_11, interval_11)
    
    # Calculo vento em 925 hPa
    mag_925 = np.sqrt(u_500**2+v_500**2)
    
    # plota a imagem pressao
    pressao_shaded = ax.contourf(lons,
                          lats, 
                          pnmm, 
                          cmap='RdBu_r',
                          levels=levels_11,
                          extend='both'
                          )
    
    ax.streamplot(lons, 
                  lats, 
                  u_250, 
                  v_250, 
                  density=[4,4], 
                  linewidth=2, 
                  arrowsize=2.5,
                  color='black', 
                  transform=ccrs.PlateCarree())
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(pressao_shaded, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('PNMM + Escoamento em 250 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/pnmm_v250/PNMM_vento_250_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()

#%%
    
    ###################### PNMM + espessura contorno ##########################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    intervalo_min_12 = np.amin(np.array(pnmm))
    intervalo_max_12 = np.amax(np.array(pnmm))
    interval_12 = 2              # de quanto em quanto voce quer que varie
    levels_12 = np.arange(intervalo_min_12, intervalo_max_12, interval_12)
    
    # intevalos da geopotencial
    intervalo_min_13 = np.amin(np.array(geopotencial_500))
    intervalo_max_13 = np.amax(np.array(geopotencial_500))
    interval_13 = 50              # de quanto em quanto voce quer que varie
    levels_13 = np.arange(intervalo_min_13, intervalo_max_13, interval_13)
    
    # plota a imagem geopotencial
    geo_contorno = ax.contour(lons,
                          lats, 
                          geopotencial_500,
                          cmap = cmap_1,
                          linewidths=2, 
                          linestyles='dashed',
                          levels=levels_13
                          )
    
    ax.clabel(geo_contorno, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=20,
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    # plota a imagem pressao
    pressao_contorno2 = ax.contour(lons,
                          lats, 
                          pnmm, 
                          colors='gray', 
                          linewidths=2, 
                          levels=levels_12
                          )
    
    ax.clabel(pressao_contorno2, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=20, 
              fmt = '%3.0f', 
              colors= 'black'
              )
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(pressao_shaded, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('PNMM + Geopotencial',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/pnmm_geo/PNMM_geo_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%    
    ########################## Umidade Relativa ####################################
    
    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    intervalo_min_14 = np.amin(np.array(pnmm))
    intervalo_max_14 = np.amax(np.array(pnmm))
    interval_14 = 2              # de quanto em quanto voce quer que varie
    levels_14 = np.arange(intervalo_min_14, intervalo_max_14, interval_14)
    
    # intevalos da geopotencial
    intervalo_min_ur = 0
    intervalo_max_ur = 100
    interval_ur = 1              
    levels_ur = np.arange(intervalo_min_ur, intervalo_max_ur, interval_ur)
    
    # Plota umidade
    sombreado = ax.contourf(lons, 
                            lats, 
                            umi_rel_1000, 
                            cmap='PRGn', 
                            levels = levels_ur, 
                            extend = 'both'
                            )
    
    # plota a imagem pressao
    contorno = ax.contour(lons,
                          lats, 
                          pnmm, 
                          colors='black', 
                          linewidths=0.8, 
                          levels=levels_14
                          )
    
    ax.clabel(contorno, 
              inline = 1, 
              inline_spacing = 1, 
              fontsize=20, 
              fmt = '%3.0f', 
              colors= 'black'
              )  
    
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, 
        ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    # adiciona legenda 
    barra_de_cores = plt.colorbar(sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    
    	
    # Add a title
    plt.title('Umidade relativa (%) em 1000 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/umidade_relativa/umd_rel_{format(vtempo_str)}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%
    ########################## Omega (Mov. Vertical) ####################################

    ###################### Especificações do Plot #############################
    
    # escolha o tamanho do plot em polegadas (largura x altura)
    plt.figure(figsize=(25,25))
    
    # usando a projeção da coordenada cilindrica equidistante 
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-90, -20, -60, 10], crs=ccrs.PlateCarree())
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
    
    # intevalos do mov vertical
    intervalo_min1 = -3
    intervalo_max1 = 0
    interval_1 = 0.2              # de quanto em quanto voce quer que varie
    levels_1 = np.arange(intervalo_min1, intervalo_max1, interval_1)
    
    #plot
    sombreado = ax.contourf(lons, 
                            lats, 
                            omega, 
                            cmap = 'inferno', 
                            levels = levels_1, 
                            extend = 'min'
                            )
    #linhas de corrente
    ax.streamplot(lons, 
                  lats, 
                  u_500, 
                  v_500, 
                  density=[4,4], 
                  linewidth=2, 
                  arrowsize=2.5,
                  color='black', 
                  transform=ccrs.PlateCarree())
    #adicionando shapefile
    shapefile = list(
        shpreader.Reader(
        r'D:\es2\GFS-analysis_and_forecast-main\shapefiles\BR_UF_2021\BR_UF_2021.shp'
        ).geometries()
        )
    
    ax.add_geometries(
        shapefile, ccrs.PlateCarree(), 
        edgecolor = 'black', 
        facecolor='none', 
        linewidth=0.5
        )
    
    # adiciona continente e bordas
    ax.coastlines(resolution='10m', color='black', linewidth=3)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=3)
    
    #legenda 
    barra_de_cores = plt.colorbar(sombreado, 
                                  orientation = 'horizontal', 
                                  pad=0.04, 
                                  fraction=0.04
                                  )
    font_size = 20 # Adjust as appropriate.
    barra_de_cores.ax.tick_params(labelsize=font_size)
    

    
    # Add a title
    plt.title('Omega (Pa/s) em 500 hPa',
              fontweight='bold', 
              fontsize=30, 
              loc='left'
              )
    
    #previsao
    #plt.title('Valid time: {}'.format(vtime), fontsize=35, loc='right')
    #analise
    plt.title('Análise: {}'.format(vtempo), fontsize=25, loc='right')
    
    # Salva imagem
    plt.savefig(f'D:/es2/imagens/analise/omega_500/mov_vert-500hpa_{vtempo_str}.png', bbox_inches='tight')
    plt.show()
    plt.close()
    
#%%

# Para dar zoom em uma região de algum campo, utilize o código abaixo:

    ### script para colocar zoom numa região
    # # inset axes....
    # axins = ax.inset_axes([0.58, 0.58, 0.4, 0.4])
    # axins.contourf(sombreado, cmap=cmap, origin="image")
    # contorno_2 = axins.contour(contorno_1, colors='black', origin="image")
    # axins.clabel(contorno_2, 
    #           inline = 1, 
    #           inline_spacing = 1, 
    #           fontsize=15, 
    #           fmt = '%3.0f', 
    #           colors= 'black'
    #           )
    
    # # sub region of the original image
    # x1, x2, y1, y2 = -55, -40, -35 , -15
    # axins.set_xlim(x1, x2)
    # axins.set_ylim(y1, y2)
    # axins.set_xticklabels([])
    # axins.set_yticklabels([])
    # ax.indicate_inset_zoom(axins, edgecolor="black")
    
# Para colocar Barbelas ao invés de linhas de corrente, inclua o código abaixo na área de plot e exclua ax.streamplot:
    
    # plt.barbs(
    #   lons_2,
    #   lats_2,
    #   u_850_2,
    #   v_850_2,
    #   fill_empty=True,
    #   length=7,
    #   sizes=dict(emptybarb=0.1, height=0.8),
    #   barbcolor="black",
    #   barb_increments=dict(flag=50),)