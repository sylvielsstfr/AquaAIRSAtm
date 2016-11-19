"""
Copyright (C) 2014 The HDF Group
Copyright (C) 2014 John Evans

This example code illustrates how to access and visualize a GESDISC AIRS grid
in Python.

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python AIRS_L3_Temperature_MW_A_Lvls11.py

The HDF file must either be in your current working directory or in a directory
specified by the environment variable HDFEOS_ZOO_DIR.

The netcdf library must be compiled with HDF4 support in order for this example
code to work.  Please see the README for details.
"""

import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

USE_NETCDF4 = False

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(f):
        os.makedirs(f)

def run(FILE_NAME):


    DATAFIELD_NAME =  'TotH2OVap_D'
    
    
    #print 'INPUT SEL',FILE_NAME,DATAFIELD_NAME
    
    
    if USE_NETCDF4:
        from netCDF4 import Dataset    
        nc = Dataset(FILE_NAME)

        # The variable has a fill value, 
        # so netCDF4 converts it to a float64 masked array for us.
        data = nc.variables[DATAFIELD_NAME][11,:,:]
        latitude = nc.variables['Latitude'][:]
        longitude = nc.variables['Longitude'][:]

    else:
        from pyhdf.SD import SD, SDC
        
        
        hdf = SD(FILE_NAME, SDC.READ)
        

        # List available SDS datasets.
        #print hdf.datasets()

        # Read dataset.
        data3D = hdf.select(DATAFIELD_NAME)
        
        
        #data = data3D[11,:,:]
        data = data3D[:,:]

        # Read geolocation dataset.
        lat = hdf.select('Latitude')
        latitude = lat[:,:]
        lon = hdf.select('Longitude')
        longitude = lon[:,:]

        # Handle fill value.
        attrs = data3D.attributes(full=1)
        fillvalue=attrs["_FillValue"]

        # fillvalue[0] is the attribute value.
        fv = fillvalue[0]
        data[data == fv] = np.nan
        data = np.ma.masked_array(data, np.isnan(data))

    
    # Draw an equidistant cylindrical projection using the low resolution
    # coastline database.
    m = Basemap(projection='cyl', resolution='l',
                llcrnrlat=-90, urcrnrlat = 90,
                llcrnrlon=-180, urcrnrlon = 180)
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(-180., 181., 45.), labels=[0, 0, 0, 1])
    m.pcolormesh(longitude, latitude, data, latlon=True, alpha=0.90)
    cb = m.colorbar()
    cb.set_label('Unit:kg/m2')
    basename = os.path.basename(FILE_NAME)
    plt.title('{0}\n {1}'.format(basename, DATAFIELD_NAME))
    fig = plt.gcf()
    # plt.show()
    
    # for latex, no points inside the filename
    p = re.compile('[.]')
    rootname=p.sub('_',basename) 
    # in mage dir put the image inside the directory related to the file
    rootimg_dir=os.path.join('images',rootname)
    ensure_dir(rootimg_dir)
    
    jpegfile = "{0}_{1}.jpg".format(rootname, DATAFIELD_NAME)
    jpegfullfile=os.path.join(rootimg_dir,jpegfile)
    fig.tight_layout()
    fig.savefig(jpegfullfile)

if __name__ == "__main__":
    
    os.environ["HDFEOS_ZOO_DIR"] = "/Users/dagoret-campagnesylvie/MacOsX/LSST/MyWork/GitHub/NASA_AIRS_AQUA_DATA/AIRH3STM/2016/h4"

    # If a certain environment variable is set, look there for the input
    # file, otherwise look in the current directory.
    #hdffile = 'AIRS.2002.08.01.L3.RetStd_H031.v4.0.21.0.G06104133732.hdf'
    
    #hdffile = 'AIRS.2016.01.01.L3.RetStd031.v6.0.31.0.G16034171018.hdf'
    #hdffile = 'AIRS.2016.02.01.L3.RetStd029.v6.0.31.0.G16063171358.hdf'
    #hdffile = 'AIRS.2016.03.01.L3.RetStd031.v6.0.31.0.G16095175654.hdf'
    #hdffile = 'AIRS.2016.04.01.L3.RetStd030.v6.0.31.0.G16122185324.hdf'
    #hdffile = 'AIRS.2016.05.01.L3.RetStd031.v6.0.31.0.G16153184258.hdf'
    #hdffile = 'AIRS.2016.06.01.L3.RetStd030.v6.0.31.0.G16189154115.hdf'
    #hdffile = 'AIRS.2016.07.01.L3.RetStd031.v6.0.31.0.G16223152110.hdf'
    #hdffile = 'AIRS.2016.08.01.L3.RetStd031.v6.0.31.0.G16245202845.hdf'
    hdffile = 'AIRS.2016.09.01.L3.RetStd030.v6.0.31.0.G16281134124.hdf'
    try:
        hdffile = os.path.join(os.environ['HDFEOS_ZOO_DIR'], hdffile)
    except KeyError:
        pass

    run(hdffile)
    
