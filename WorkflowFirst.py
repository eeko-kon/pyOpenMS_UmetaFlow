import numpy as np
import pandas as pd
import pyopenms
from pyopenms import *

options = PeakFileOptions()
options.setMSLevels([1])
fh = MzMLFile()
fh.setOptions(options)

exp = MSExperiment()
print("about load")
MzMLFile().load("raw_files/20200723_NBC_UMETAB137_Albus_O_acu_POS_009.mzML", exp)
print("successfully loaded")
feature_map = FeatureMap()
mass_traces = []
mass_traces_split = []
mass_traces_filtered = []

peak_map = PeakMap()

print('# Spectra:', len(exp.getSpectra()))
print('# Chromatograms:', len(exp.getChromatograms()))

for chrom in exp.getChromatograms():
    peak_map.addChromatogram(chrom)

for spec in exp.getSpectra():
    peak_map.addSpectrum(spec)

mass_trace_detect = MassTraceDetection()
mass_trace_detect.run(peak_map, mass_traces, 10000000000000)

print('# Mass traces:', len(mass_traces))

elution_peak_detection = ElutionPeakDetection()
elution_peak_detection.detectPeaks(mass_traces, mass_traces_split)
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
mztab= MzTab()
hits= search._run_0(deconcoluted, mztab) 
mztab.store("Masshits.mztab", hits)
print(hits)


