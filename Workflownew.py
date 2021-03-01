import numpy as np 
import pandas as pd
import pyopenms 
from pyopenms import *

exp = MSExperiment()

import sys
print("Loading")
MzMLFile().load("./wf_testing/GermicidinAstandard.mzML", exp)
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
fh.store('./wf_testing/FeatureFindingMetabo.featureXML', feature_map)

for p in feature_map:
    print(p.getRT(), p.getIntensity(), p.getMZ())

deconv = MetaboliteFeatureDeconvolution()
f_out = FeatureMap()
cons_map0 = ConsensusMap()
cons_map1 = ConsensusMap()
deconvoluted = deconv.compute(feature_map, f_out, cons_map0, cons_map1)
deconvol = FeatureXMLFile()
deconvol.store("./wf_testing/devoncoluted.featureXML", feature_map)

# create temporary filesystem objects
debug_level = 10
sirius_tmp = SiriusTemporaryFileSystemObjects(debug_level)

# TODO: Add preprocessing here! To use the featureMapping! 
# https://github.com/OpenMS/OpenMS/blob/develop/src/utils/SiriusAdapter.cpp#L193

# TODO: Check feature and/or spectra number
# https://github.com/OpenMS/OpenMS/blob/develop/src/utils/SiriusAdapter.cpp#L201

# construct sirius ms file object
msfile = SiriusMSFile()

# fill variables, which are used in the function
# TODO: need to construct the feature mapping 
feature_mapping = FeatureMapping_FeatureToMs2Indices() 
feature_only = True #SiriusAdapterAlgorithm.getFeatureOnly()==True
isotope_pattern_iterations = 3
no_mt_info = False
compound_info = [] #SiriusMSFile_CompoundInfo()

#this is a parameter, which is called "feature_only" 
#It is a boolean value (true/false) and if it is true you are using the  the feature information 
#from in_featureinfo to reduce the search space to MS2 associated with a feature.
#this is recommended when working with featureXML input, if you do NOT use it 
#sirius will use every individual MS2 spectrum for estimation (and it will take ages)
#bool feature_only = (sirius_algo.getFeatureOnly() == "true") ? true : false;
#SiriusAdapterAlgorithm.getNoMasstraceInfoIsotopePattern() == False

msfile.store(exp, 
             String(sirius_tmp.getTmpDir()), # has to be converted to an "OpenMS::String"
             feature_mapping, 
             feature_only,
             isotope_pattern_iterations, 
             no_mt_info, 
             compound_info)

#Cython signature: void store
#(MSExperiment & spectra, String & msfile,
# FeatureMapping_FeatureToMs2Indices & feature_ms2_spectra_map, bool & feature_only, 
# int & isotope_pattern_iterations, bool no_mt_info, 
# libcpp_vector[SiriusMSFile_CompoundInfo] v_cmpinfo)


