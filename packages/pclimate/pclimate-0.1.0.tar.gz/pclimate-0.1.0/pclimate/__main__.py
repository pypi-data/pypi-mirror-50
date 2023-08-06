# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 17:07:19 2019

@author: travis
"""
import warnings
warnings.filterwarnings('ignore')
import argparse
import os
from .functions import Site_Weather

def main():
    # Call help statements
    description=(
        """
        pclimate for "Point Climate". \n

        Use a lat/long point coordinate to retrieve daily weather estimations
        from the PRISM data set via northwestknowledge.net. Available since 
        1979.
        
        Minimum Input Needed:
    
            Latitude and longitude of the weather station (lat lon)
            
        Option Input
        
            first and last year desired (year1 year2)
    
        Returns:
    
            Daily values of incoming solar radiation (MJ/m²-day)
            Maximum and minimum daily air temperature (ºC)
            Daily total rainfall (mm)
        """)

    crd_help = (
        """
        Input lat/lon coordinates where you want weather information as a 
        simple list (lat lon).  Defaults to the Southwestern Colorado 
        Research Station at 37.54, -108.74
        """)

    dest_help = (
        """
        Specify the location and filename (.csv) of the resulting dataframe. 
        Defaults to data/pquery_<coordinate_string>_<year_string>.csv
        """)

    year_help = (
        """
        First and last year desired. Defaults to full record from 1979 to
        present, which takes a while.
        """)

    # Call arguments
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-coords',  type=float, dest='coords', nargs="+",
                        default=[37.54, -108.74], help=crd_help)
    parser.add_argument('-dest', dest='dest',
                        default='data/pquery_', help=dest_help)
    parser.add_argument('-years',  type=int, dest='years', nargs="+",
                        default=[2016, 2019], help=year_help)
    parser.add_argument
    args = parser.parse_args()
    dest=args.dest
    lat = args.coords[0]
    lon = args.coords[1]
    if len(args.years) > 1:    
        years = range(args.years[0], args.years[1] + 1)
    else:
        years = args.years

    # If they didn't specify a destination file
    if dest == 'data/pquery_':
        iden = "{}_{}_{}_{}".format(lat, lon, years[0], years[-1])
        iden = iden.replace(".", "").replace("-", "")
        iden = iden + ".csv"
        dest = os.path.join("data", "pquery_" + iden)

    # if they specified the wrong extension
    if os.path.splitext(dest)[1] != '.csv':
        root, ext = os.path.splitext(dest)
        dest = root + ".csv"

    # make sure there is a home for this
    dest_folder = os.path.dirname(dest)
    if not os.path.exists(dest_folder):
        os.mkdir(dest_folder)

    # retrieve and save data
    print("Retrieving daily weather history...")
    wth = Site_Weather(lat, lon, years).getWeather()
    print("Saving file to " + dest + "...")
    wth.to_csv(dest, index=False)

# Call
if __name__ == "__main__":
    main()
