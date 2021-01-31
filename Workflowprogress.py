import numpy as np 
import pandas as pd
import pyopenms 
from pyopenms import *

#Tue: save file temporarily -analyse-delete
exp = MSExperiment()

import sys
print("Loading")
MzMLFile().load(sys.argv[1], exp)
print("Loaded")

feature_map = FeatureMap()
mass_traces = []
mass_traces_split = []
mass_traces_filtered = []

peak_map = PeakMap()
for chrom in exp.getChromatograms():
    peak_map.addChromatogram(chrom)

for spec in exp.getSpectra():
    peak_map.addSpectrum(spec)

MassTraceDetection().run(peak_map, mass_traces) #Mass Trace Detection default parameters
ElutionPeakDetection().detectPeaks(mass_traces, mass_traces_split)  #to separate isobaric Mass Traces by elution time

ff = FeatureFindingMetabo() #assembling mass traces to charged features
ff.run(mass_traces_split,
    feature_map,
    mass_traces_filtered)

print('# Mass traces filtered:', len(mass_traces_filtered))
print('# Features:', feature_map.size())

feature_map.setUniqueIds()
fh = FeatureXMLFile()
print("Found", feature_map.size(), "features")
fh.store('FeatureFindingMetabo.featureXML', feature_map)

for p in feature_map:
    print(p.getRT(), p.getIntensity(), p.getMZ())

search= AccurateMassSearchEngine() #specify libraries? 
print("start parsing files")
#try except 
parsefiles= search.init() 
print("parsed mass files")
mztab= MzTabFile()
hits= search.run(feature_map, mztab) 
print("done: hits")


