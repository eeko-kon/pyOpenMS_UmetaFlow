#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:04:24 2020

@author: eeko
"""
"""
CONVERT RAW TO MZML: FOR ONE FILE
"""
#docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/20200723_NBC_UMETAB137_Blank_POS_006.raw --mzML --ignoreUnknownInstrumentError
"""
FOR THE WHOLE FOLDER
"""
#docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Documents/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/\*.raw --mzML --ignoreUnknownInstrumentError

"""mzML CENTROID"""
#docker run -it --rm -e WINEDEBUG=-all -v /Users/eeko/Desktop/py4e/raw_files:/data chambm/pwiz-skyline-i-agree-to-the-vendor-licenses wine msconvert /data/\*.raw --zlib --filter "peakPicking true 1-" --ignoreUnknownInstrumentError

"""Copy a file in the 10.75.1.39 shared machine:
scp /Users/eeko/Documents/raw_files/20200723_NBC_UMETAB137_Blank_POS_006.mzML eeko@10.75.1.39:.
"""
"""connect to the shared machine:
ssh eeko@10.75.1.39 
password"""

"""FEATURE FINDER"""
import pyopenms as oms
from pyopenms import *

OPENMS_OBJ_TYPES = (
    oms.PeakMap,
    oms.FeatureMap,
    oms.MSExperiment,
    oms.ConsensusMap,
    )

feature_map = FeatureMap()
mass_traces = []
mass_traces_split = []
mass_traces_filtered  = []

exp = oms.MSExperiment()

MzMLFile().load("raw_files/20200723_NBC_UMETAB137_Blank_POS_006.mzML", exp)

options = oms.PeakFileOptions()
options.setMSLevels([1])
#help(PeakFileOptions)

fh = oms.MzXMLFile()
fh.setOptions(options)

# Peak map= MSExperiment()
peak_map = oms.PeakMap()

print('# Spectra:', len( exp.getSpectra() ))
print('# Chromatograms:', len( exp.getChromatograms() ) )

for chrom in exp.getChromatograms():
    peak_map.addChromatogram(chrom)
    
for spec in exp.getSpectra():
    peak_map.addSpectrum(spec)

mass_trace_detect = oms.MassTraceDetection()
mass_trace_detect.run(peak_map, mass_traces)

print('# Mass traces:', len(mass_traces) )

elution_peak_detection = oms.ElutionPeakDetection()
elution_peak_detection.detectPeaks(mass_traces, mass_traces_split)
print('# Mass traces split:', len(mass_traces_split) )

feature_finding_metabo = oms.FeatureFindingMetabo()
feature_finding_metabo.run(
            mass_traces_split,
            feature_map,
            mass_traces_filtered)

print('# Mass traces filtered:', len(mass_traces_filtered) )
print('# Features:', feature_map.size())

feature_map.setUniqueIds()
fh = FeatureXMLFile()
fh.store("/py4e/store/hne.featureXML", feature_map)
print("Found", feature_map.size(), "features")
oms.FeatureXMLFile().store('FeatureFindingMetabo.featureXML', feature_map)

for p in feature_map:
    print(p.getRT(), p.getIntensity(), p.getMZ())
    import pylab
    pylab.plot(p.getRT(), p.getIntensity(), '-')
    pylab.xlabel('Retention (s)')
    pylab.ylabel('Intensity')
    print(pylab.show())

MetaboliteAdductDecharger= oms.MetaboliteFeatureDeconvolution(feature_map)
"""
Another way to Extract m/z, retention, intensity, and charge information

retentions = []
mass = []
intensity = []
charges = []

for fe in feature_map:
    retentions.append(fe.getRT())
    mass.append(fe.getMZ())
    intensity.append(fe.getIntensity())
    charges.append(fe.getCharge())

#Create a tuple and sort based on retention time in ascending order

rimc = list(zip(retentions, intensity, mass, charges))
print(rimc[0])

def getKey(item):
    return item[0]
rimcSort = sorted(rimc, key=getKey)
print(rimcSort[0])

#Let's see what the entire chromatogram looks like

rt = [rimcSort[i][0] for i in range(0, len(rimcSort))]
ints = [rimcSort[i][1] for i in range(0, len(rimcSort))]

import pylab
pylab.plot(rt, ints, '-')
pylab.xlabel('Retention (s)')
pylab.ylabel('Intensity')
pylab.legend()
"""
""" 
ALIGNMENT
var = oms.MapAlignmentAlgorithmIdentification()
param = var.align(peak_map , feature_finding_metabo)
help(MapAlignmentAlgorithmIdentification)

# Execute OpenSwathWorkflow in docker
OpenSwathWorkflow --help
# Execute PyProphet in docker
pyprophet --help
# Execute TRIC in docker
feature_alignment.py --help


# Download OpenSWATH image (openswath/openswath:latest)
docker pull openswath/openswath:latest

# Generate tutorial container (osw_tutorial) and log in
docker run --name osw_tutorial --rm -v ~/Desktop/:/data -i -t openswath/openswath:latest
# Execute OpenSwathWorkflow in docker
OpenSwathWorkflow --help
# Execute PyProphet in docker
pyprophet --help
# Execute TRIC in docker
feature_alignment.py --help"""
"""

run FeatureFinderMetabo, MetaboliteAdductDecharger and AccurateMassSerach (CandidateID)

oms.MetaboliteAdductDecharger
"""
