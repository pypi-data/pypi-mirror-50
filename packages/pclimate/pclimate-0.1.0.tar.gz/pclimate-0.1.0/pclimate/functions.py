# -*- coding: utf-8 -*-
"""
Functions to help work with DSSAT. Eventually I would like to work with
pyDSSAT, but for now these are primarily for retrieving the info needed to run
the models.

Created on Mon May 20 13:36:39 2019

@author: Travis
"""
import warnings
warnings.filterwarnings('ignore')
from functools import reduce
import numpy as np
import pandas as pd
import xarray as xr


class Site_Weather:
    '''
    Minimum Data Needed:

        Latitude and longitude of the weather station
    
    Returns:

        Daily values of incoming solar radiation (MJ/m²-day)
        Maximum and minimum daily air temperature (ºC)
        Daily total rainfall (mm)
    '''
    def __init__(self, lat, lon, years):
        self.lat = lat
        self.lon = lon
        self.years = years

    def nearest_wgs(self, data):
        '''
        Take a coordinate from some where and return the index positions of the
        closest grid cell.
        '''
        lats = data.lat.values
        lons = data.lon.values
        lat = self.lat
        lon = self.lon
        lat_diffs = abs(lats - lat)
        lon_diffs = abs(lons - lon)
        y = np.where(lat_diffs == min(lat_diffs))[0][0]
        x = np.where(lon_diffs == min(lon_diffs))[0][0]

        return y, x

    def getSRAD(self):
        # Establish containers
        dates = []
        srads = []

        # We can use thredds
        for year in self.years:
            srad_path = ('http://thredds.northwestknowledge.net:8080/' +
                         'thredds/dodsC/MET/srad/srad_' + str(year) +
                         '.nc#fillmismatch')
            data = xr.open_dataset(srad_path)
            data_set = 'surface_downwelling_shortwave_flux_in_air'
        
            # Use coordinates to retrieve data from the closest point
            y, x = self.nearest_wgs(data)
            srad = data.variables[data_set][:, y, x]
            
            # We'll have to see how we need to pacakge this
            [dates.append(d) for d in data.day.values]
            [srads.append(s) for s in srad.values]

        # This may need to be packaged differently
        df = pd.DataFrame({'date': dates, 'srad': srads})

        return df

    def getTempMax(self):
        # Establish containers
        dates = []
        temps = []

        # We can use thredds
        for year in self.years:
            srad_path = ('http://thredds.northwestknowledge.net:8080/' +
                         'thredds/dodsC/MET/tmmx/tmmx_' + str(year) +
                         '.nc#fillmismatch')
            data = xr.open_dataset(srad_path)
            data_set = 'air_temperature'
        
            # Use coordinates to retrieve data from the closest point
            y, x = self.nearest_wgs(data)
            temp = data.variables[data_set][:, y, x]
            
            # We'll have to see how we need to pacakge this
            [dates.append(d) for d in data.day.values]
            [temps.append(s) for s in temp.values]

        # We need our data in celsius, this is in Kelvin
        temps = [t - 273.15 for t in temps]

        # This may need to be packaged differently
        df = pd.DataFrame({'date': dates, 'tmax': temps})

        return df

    def getTempMin(self):
        # Establish containers
        dates = []
        temps = []

        # We can use thredds
        for year in self.years:
            srad_path = ('http://thredds.northwestknowledge.net:8080/' +
                         'thredds/dodsC/MET/tmmn/tmmn_' + str(year) +
                         '.nc#fillmismatch')
            data = xr.open_dataset(srad_path)
            data_set = 'air_temperature'
        
            # Use coordinates to retrieve data from the closest point
            y, x = self.nearest_wgs(data)
            temp = data.variables[data_set][:, y, x]
            
            # We'll have to see how we need to pacakge this
            [dates.append(d) for d in data.day.values]
            [temps.append(s) for s in temp.values]

        # We need our data in celsius, this is in Kelvin
        temps = [t - 273.15 for t in temps]

        # This may need to be packaged differently
        df = pd.DataFrame({'date': dates, 'tmin': temps})

        return df

    def getPrecip(self):
        # Establish containers
        dates = []
        precips = []

        # We can use thredds
        for year in self.years:
            srad_path = ('http://thredds.northwestknowledge.net:8080/' +
                         'thredds/dodsC/MET/pr/pr_' + str(year) +
                         '.nc#fillmismatch')
            data = xr.open_dataset(srad_path)
            data_set = 'precipitation_amount'
        
            # Use coordinates to retrieve data from the closest point
            y, x = self.nearest_wgs(data)
            precip = data.variables[data_set][:, y, x]
            
            # We'll have to see how we need to pacakge this
            [dates.append(d) for d in data.day.values]
            [precips.append(s) for s in precip.values]

        # This may need to be packaged differently
        df = pd.DataFrame({'date': dates, 'precip': precips})

        return df

    def getWeather(self):
        # Get each data set
        srad = self.getSRAD()
        tmin = self.getTempMin()
        tmax = self.getTempMax()
        precip = self.getPrecip()
        dflist = [srad, tmin, tmax, precip]
        

        # Merge
        df = reduce(lambda x, y: pd.merge(x, y, on='date'), dflist)

        # Go ahead and add coordinaes
        df['lat'] = self.lat
        df['lon'] = self.lon

        return df


class Site_Soil:
    '''
    Cortez Area Soil Survey:
    https://www.nrcs.usda.gov/Internet/FSE_MANUSCRIPTS/colorado/CO671/0/CO671%20Cortez.pdf

    SSURGO Metadata:
    http://www.nrcs.usda.gov/wps/PA_NRCSConsumption/download?cid=stelprdb1241115&ext=pdf
    https://data.nal.usda.gov/system/files/SSURGO_Metadata_-_Table_Column_Descriptions.pdf

    gSSURGO Source:
    https://nrcs.app.box.com/v/soils

    Minimum Data Needed:

        Upper and lower horizon depths (cm)
        Percentage sand, silt, and clay content
        1/3 bar bulk density
        Organic carbon
        pH in water
        Aluminum saturation
        Root abundance information
    
    Could also use:
        Soil series name
        Soil Classification
        Color
        Percent Slope
        Runoff Potential
        Fertility Factor
        Color
        Drainage
        Cation Exchange Capacity (cmol/kg)
        Percent Stones
        Percent Total Nitrogen
        Root Growth Factor (0 - 1)
    
    Okay, the current strategy is to download the gridded SSURGO (gSSURGO)
    geographic data base and work from the local file. To make this work, use
    ArcMap to pull in the 10m map from the geodatabase (One state at a time
    for now), join the components table with mukey and use that to join the
    chorizon table to that. This will give you all of the soil horizon needed
    to calculate the parameters needed for DSSAT, I think...hopefully.
    '''
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.soldf = pd.read_csv('data/co_soil.csv')
        self.solnc = xr.open_dataset('data/co_soil.nc')
        # self.densities = pd.read_csv('data/tables/bulk_densities.txt', sep='|')

    def nearest_albers(self, y, x):
        '''
        Take a coordinate from some where and return the index positions of the
        closest grid cell.
        '''
        data = self.solnc
        ys = data.y.values
        xs = data.x.values
        y_range = [ys[ys>y][0], ys[ys<y][-1]]
        y_diff = [abs(y-l) for l in y_range]
        y_idx = y_diff.index(min(y_diff))
        target_y = y_range[y_idx]
        x_range = [xs[xs>x][0], xs[xs<x][-1]]
        x_diff = [abs(x-l) for l in x_range]
        x_idx = x_diff.index(min(x_diff))
        target_x = x_range[x_idx]
        y = np.where(ys == target_y)[0][0]
        x = np.where(xs == target_x)[0][0]
        
        return y, x

    def getMukey(self):
        
        # We have to project lat lon to albers equal area conic USGS
        wgs = Proj(init='epsg:4326')
        albers = Proj('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 ' +
                      '+lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 ' +
                      '+towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
        x, y = transform(wgs, albers, self.lon, self.lat)
        y, x = self.nearest_albers(y, x)

        # Now find that spot in the soil netcdf
        data = self.solnc
        mukey = data.variables['Band1'][y, x].data

        return int(mukey)

    def getHorizonDepths(self):
        df = self.soldf
        mukey = self.getMukey()
        hzdept_r = df['hzdept_r'][df['MUKEY'] == mukey].values
        hzdepb_r = df['hzdepb_r'][df['MUKEY'] == mukey].values

        return hzdept_r, hzdepb_r

    def getBulkDensity(self):
        df = self.soldf
        mukey = self.getMukey()
        dbthirbar_r = df['dbthirdbar'][df['MUKEY'] == mukey].values
        return dbthirbar_r

    def getPercentFines(self):
        df = self.soldf
        mukey = self.getMukey()
        dbthirbar_r = self.getBulkDensity()
        sandtotal_r = df['sandtotal_'][df['MUKEY'] == mukey].values
        silttotal_r = df['silttotal_'][df['MUKEY'] == mukey].values
        claytotal_r = df['claytotal_'][df['MUKEY'] == mukey].values

        psand = sandtotal_r / dbthirbar_r  # Is this somehow already in %?
        psilt = silttotal_r / dbthirbar_r
        pclay = claytotal_r / dbthirbar_r

        return psand, psilt, pclay

    def getMapUnit(self):
        df = self.soldf
        mukey = self.getMukey()
        muname = df['muname'][df['MUKEY'] == mukey].values

        return muname
