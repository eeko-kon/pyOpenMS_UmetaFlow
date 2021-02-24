import numpy as np 
import pandas as pd
import pyopenms 
from pyopenms import *

exp = MSExperiment()

import sys
print("Loading")
MzMLFile().load("GermicidinAstandard.mzML", exp)
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

MassTraceDetection().run(peak_map, mass_traces, 1000)
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
deconvoluted= deconv.compute(feature_map, f_out, cons_map0, cons_map1)
deconvol = FeatureXMLFile()
deconvol.store("devoncoluted.featureXML", feature_map)
Sirius= SiriusMSFile()
sirius= MSExperiment()
feature_only= FeatureXMLFile() #?
#bool no_mt_info??
compoundinfo= SiriusMSFile()
Sirius.store(exp, sirius, feature_map, feature_only, 10, #noideahere, compoundinfo)

#Cython signature: void store(MSExperiment & spectra, String & msfile,
#FeatureMapping_FeatureToMs2Indices & feature_ms2_spectra_map, bool & feature_only, 
#int & isotope_pattern_iterations, bool no_mt_info, 
#libcpp_vector[SiriusMSFile_CompoundInfo] v_cmpinfo)