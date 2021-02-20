import numpy as np
import pandas as pd
import pyopenms
from pyopenms import *
import sys

exp = MSExperiment()

print("loading")
MzMLFile().load("WGS14_standard_POS_005_noncentroid.mzML", exp)   #or MzMLFile().load(sys.argv[1].exp)
print("loaded")

feature_map = FeatureMap()
mass_traces = []
mass_traces_split = []
mass_traces_filtered = []

print('# Spectra:', len(exp.getSpectra()))
print('# Chromatograms:', len(exp.getChromatograms()))

peak_map = PeakMap()

for chrom in exp.getChromatograms():
    peak_map.addChromatogram(chrom)

for spec in exp.getSpectra():
    peak_map.addSpectrum(spec)

MassTraceDetection().run(peak_map, mass_traces)
print('# Mass traces:', len(mass_traces))
ElutionPeakDetection().detectPeaks(mass_traces, mass_traces_split)
print('# Mass traces split:', len(mass_traces_split))

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
deconcoluted= deconv.compute(feature_map, f_out, cons_map0, cons_map1)

search= AccurateMassSearchEngine()
parsefiles= search.init() 
output= MzTab()
hits= search._run_0(deconcoluted, output) 

#convert mzTab to mzML
#Add SIRIUS fragmentation trees with seed:accumasssearchengine
#and then MS2 database search

"""
SiriusAdapterHit(             SiriusAdapterRun(             SiriusMzTabWriter(
SiriusAdapterIdentification(  SiriusMSFile( 
"""