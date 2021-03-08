import numpy as np 
import pandas as pd
import pyopenms 
from pyopenms import *

exp = MSExperiment()

print("Loading")
MzMLFile().load("Standards/ThermocentroidGermicidinAstandard.mzML", exp)
print("Loaded")

feature_map_FFM = FeatureMap()
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
print(len(mass_traces_split))

ff = FeatureFindingMetabo()
ff.run(mass_traces_split,
    feature_map_FFM,
    mass_traces_filtered)

print('# Mass traces filtered:', len(mass_traces_filtered))
print('# Features:', feature_map_FFM.size())

feature_map_FFM.setUniqueIds()
fh = FeatureXMLFile()
print("Found", feature_map_FFM.size(), "features")
fh.store('./wf_testing/FeatureFindingMetabo.featureXML', feature_map_FFM)

for p in feature_map_FFM:
    print(p.getRT(), p.getIntensity(), p.getMZ())

deconv = MetaboliteFeatureDeconvolution()
feature_map_DEC = FeatureMap()
cons_map0 = ConsensusMap()
cons_map1 = ConsensusMap()
deconvoluted = deconv.compute(feature_map_FFM, feature_map_DEC, cons_map0, cons_map1)
deconvol = FeatureXMLFile()
deconvol.store("./wf_testing/devoncoluted.featureXML", feature_map_DEC)

featureinfo= "./wf_testing/devoncoluted.featureXML"
spectra= exp
v_fp= []
fp_map_kd= KDTreeFeatureMaps()
sirius_algo= SiriusAdapterAlgorithm()
feature_mapping = FeatureMapping_FeatureToMs2Indices() 
sirius_algo.preprocessingSirius(featureinfo,
                                spectra,
                                v_fp,
                                fp_map_kd,
                                sirius_algo,
                                feature_mapping)

print("preprocessed")

sirius_algo.checkFeatureSpectraNumber(featureinfo,
                                    feature_mapping,
                                    spectra,
                                    sirius_algo)
print("checked")

msfile = SiriusMSFile()
debug_level = 10
sirius_tmp = SiriusTemporaryFileSystemObjects(debug_level)
siriusstring= String(sirius_tmp.getTmpMsFile())

feature_only = True 
isotope_pattern_iterations = 3
no_mt_info = False 
compound_info = []

msfile.store(spectra, 
             siriusstring, 
             feature_mapping, 
             feature_only,
             isotope_pattern_iterations, 
             no_mt_info, 
             compound_info)
print("stored")
out_csi= CsiFingerIdMzTabWriter()
out_csifingerid= String(out_csi)
executable= "Users/eeko/Applications/sirius"
subdirs= sirius_algo.callSiriusQProcess(String(sirius_tmp.getTmpMsFile()),
                                String(sirius_tmp.getTmpOutDir()),
                                executable,
                                out_csifingerid,
                                sirius_algo)
print("SIRIUSQprocess")
candidates = sirius_algo.getCandidates()
sirius_result= MzTab()
siriusfile= MzTabFile()
input = "Standards/ThermocentroidGermicidinAstandard.mzML"
SiriusMzTabWriter.read(subdirs,
                        input,
                        candidates,
                        sirius_result)
print("storing..")
siriusfile.store("./wf_testing/out_sirius", sirius_result)
print("stored")
