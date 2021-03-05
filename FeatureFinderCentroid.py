#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 13:43:47 2020

@author: eeko
"""
"""
CONVERT RAW TO MZML: FOR ONE FILE
"""
docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/20200723_NBC_UMETAB137_Blank_POS_006.raw --zlib --filter "peakPicking true [1 ,2]" --ignoreUnknownInstrumentError
docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/20200723_NBC_UMETAB137_Blank_POS_006.raw --mzML  --ignoreUnknownInstrumentError

"""
FOR THE WHOLE FOLDER
"""
docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/\*.raw --filter "peakPicking true 1-" --ignoreUnknownInstrumentError

"""Copy a file in the 10.75.1.39 shared machine:
scp /Users/eeko/Documents/raw_files/20200723_NBC_UMETAB137_Blank_POS_006.mzML eeko@10.75.1.39:.
"""
"""connect to the shared machine:
ssh eeko@10.75.1.39 
password"""
pip install pyopenms
pip install pandas
pip install numpy

import pandas as pd
import numpy as np
import pyopenms
from pyopenms import *

# Prepare data loading (save memory by only
# loading MS2 spectra into memory)
options = PeakFileOptions()
options.setMSLevels([2])
fh = MzMLFile()
fh.setOptions(options)

# Load data
exp = MSExperiment()
fh.load("20200723_NBC_UMETAB137_Blank_POS_006.mzML", exp)
exp.updateRanges()

ff = FeatureFinder()
ff.setLogType(LogType.CMD)


# Run the feature finder
name = "centroided"
features = FeatureMap()
seeds = FeatureMap()
params = FeatureFinder().getParameters(name)
ff.run(name, exp, features, params, seeds)

features.setUniqueIds()
fh = FeatureXMLFile()
fh.store("output.featureXML", features)
print("Found", features.size(), "features")

f0 = features[0]
for f in features:
    print (f.getRT(), f.getMZ())
