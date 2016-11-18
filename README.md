# AquaAIRSAtm
==============


Get the data form AIRS instrument onboard Acqua satellite on Water Vapor and Ozone
We want to retrieve monthly averaged data to buid standard LSST models


## hierarchy of directories:



- **doc** : usefull documentation
- **test** : basic tests with AIRS files and HDF-python format
- **utils** : very usefull code to know about
- **worldL3Data** : first exploration of AIRS L3 data



## To remember:


### in working directory:
--------------------------

ln -s /Users/dagoret-campagnesylvie/anaconda/envs/pyastrophys/lib/libjpeg.8.dylib 


### define the path of input files
--------------------------------

export HDFEOS_ZOO_DIR="/Users/dagoret-campagnesylvie/MacOsX/LSST/MyWork/GitHub/NASA_AIRS_AQUA_DATA/2016/h4" 