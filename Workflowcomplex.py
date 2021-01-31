
import numpy as np 
import pandas as pd
import pyopenms 
from pyopenms import *

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

MassTraceDetection().run(peak_map, mass_traces)
ElutionPeakDetection().detectPeaks(mass_traces, mass_traces_split)

ff = FeatureFindingMetabo()
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


deconv = MetaboliteFeatureDeconvolution()
f_out= FeatureMap()
cons_map0= ConsensusMap()
cons_map1= ConsensusMap()
print("start deconv")
deconvoluted= deconv.compute(feature_map, f_out, cons_map0, cons_map1)
print("deconv done")
search= AccurateMassSearchEngine()
print("start parsing files")
parsefiles= search.init() 
print("parsed mass files")
mztab= MzTabFile()
hits= search._run_0(deconvoluted, mztab) 
print("done: hits")


