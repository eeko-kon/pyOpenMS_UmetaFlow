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
 
search= AccurateMassSearchEngine()
parsefiles= search.init() 
mztab= MzTab()
hits= search._run_0(deconvoluted, mztab) 
mztab.store("Masshits.mztab", mztab)
print(hits)


