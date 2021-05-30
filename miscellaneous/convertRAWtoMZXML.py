#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 10:51:59 2020
This is the command to convert .raw data to mzxml
@author: eeko
"""
"""
CONVERT RAW TO MZML: FOR ONE FILE
"""
docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/20200723_NBC_UMETAB137_Blank_POS_006.raw --filter "peakPicking true 1-" --ignoreUnknownInstrumentError
"""
FOR THE WHOLE FOLDER
"""
docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/\*.raw --mzML --ignoreUnknownInstrumentError

"""Copy a file in the 10.75.1.39 shared machine:
scp /Users/eeko/Documents/raw_files/20200723_NBC_UMETAB137_Blank_POS_006.mzML eeko@10.75.1.39:.
"""
"""connect to the shared machine:
ssh eeko@10.75.1.39 
password"""

import pandas as pd
import numpy as np
import pyopenms
from pyopenms import *
exp = MSExperiment()
MzMLFile().load("20200723_NBC_UMETAB137_Blank_POS_006.mzML", exp)
#help(exp)
exp.getNrSpectra()
exp.getNrChromatograms()

"""iterate
"""
for spec in exp:
   print("MS Level:", spec.getMSLevel())
"""
take a look at the data:
"""
print ("MS Level:", exp[0].getMSLevel())
spec = exp[1]
mz, intensity = spec.get_peaks()
sum(intensity)

for peak in spec:
... print (peak.getIntensity())
"""
Calculates total ion chromatogram of an LC-MS/MS experiment
"""
def calcTIC(exp, mslevel):
    tic = 0
    # Iterate through all spectra of the experiment
    for spec in exp:
        # Only calculate TIC for matching (MS1) spectra
        if spec.getMSLevel() == mslevel:
            mz, i = spec.get_peaks()
            tic += sum(i)
    return tic

spectrum_data = exp.getSpectrum(0).get_peaks()
chromatogram_data = exp.getChromatogram(0).get_peaks()

"""
Script to read mzML data and filter out all MS1 spectra:
"""
from pyopenms import *
exp = MSExperiment()
MzMLFile().load("test.mzML", exp)

spec = []
for s in exp.getSpectra():
    if s.getMSLevel() != 1:
        spec.append(s)
exp.setSpectra(spec)

MzMLFile().store("filtered.mzML", exp)
