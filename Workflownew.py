import numpy as np 
import pandas as pd
import pyopenms 
from pyopenms import *

exp = MSExperiment()

print("Loading")
MzMLFile().load("data Thermo Orbitrap ID-X/FileFiltered Std/ThermocentroidpentamycinFileFilter.mzML", exp)
print("Loaded")
#print(exp.getSourceFiles()[0].getNativeIDTypeAccession())
#print(exp.getSourceFiles()[0].getNativeIDType())

feature_map_FFM = FeatureMap()
mass_traces = []
mass_traces_split = []
mass_traces_filtered = []

peak_map = PeakMap()
for chrom in exp.getChromatograms():
    peak_map.addChromatogram(chrom)

for spec in exp.getSpectra():
    peak_map.addSpectrum(spec)

# Run mass trace detection
mtd = MassTraceDetection()
mtd_par = mtd.getDefaults()
# set addition parameters values
mtd_par.setValue("mass_error_ppm", 10.0) # example set ppm error
mtd_par.setValue("noise_threshold_int", 10.0)

mtd.setParameters(mtd_par)
print(mtd_par.getValue("mass_error_ppm")) # example check a specific value
mtd.run(peak_map, mass_traces, 1000)

# Run elution peak detection
epd = ElutionPeakDetection()
epd_par = epd.getDefaults()
# set additional parameter values
epd_par.setValue("width_filtering", "fixed")
epd.setParameters(epd_par)
epd.detectPeaks(mass_traces, mass_traces_split)

print(len(mass_traces_split))


ffm = FeatureFindingMetabo()
ffm_par = ffm.getDefaults() 
# set additional parameter values
ffm_par.setValue("isotope_filtering_model", "none")
#
ffm.setParameters(ffm_par)
ffm.run(mass_traces_split,
    feature_map_FFM,
    mass_traces_filtered)

print('# Mass traces filtered:', len(mass_traces_filtered))
print('# Features:', feature_map_FFM.size())

feature_map_FFM.setUniqueIds()
fh = FeatureXMLFile()
print("Found", feature_map_FFM.size(), "features")
fh.store('./wf_testing/FeatureFindingMetabo.featureXML', feature_map_FFM)

# output all traces in the feature map
# for p in feature_map_FFM:
#     print(p.getRT(), p.getIntensity(), p.getMZ())

# Run metabolite adduct decharging detection
# With SIRIUS you are only able to use singly charged adducts
mfd = MetaboliteFeatureDeconvolution()
mdf_par = mfd.getDefaults()
# set additional parameter values
potential_adducts = [b"H:+:0.6",b"Na:+:0.2",b"K:+:0.2"]
mdf_par.setValue("potential_adducts", potential_adducts)
print(mdf_par.getValue("potential_adducts")) # test if adducts have been set correctly
mfd.setParameters(mdf_par)

feature_map_DEC = FeatureMap()
cons_map0 = ConsensusMap()
cons_map1 = ConsensusMap()
mfd.compute(feature_map_FFM, feature_map_DEC, cons_map0, cons_map1)
fxml = FeatureXMLFile()
fxml.store("./wf_testing/devoncoluted.featureXML", feature_map_DEC)


# Prepare sirius parameters
sirius_algo = SiriusAdapterAlgorithm()
#sirius_algo_par = SiriusAdapterAlgorithm().getDefaults()
#sirius_algo_par.setValue("preprocessing:filter_by_num_masstraces", 3) # need at least 3 mass traces (for testing)
#sirius_algo_par.setValue("preprocessing:precursor_mz_tolerance", 10.0)
#sirius_algo_par.setValue("preprocessing:precursor_mz_tolerance_unit", "ppm")
#sirius_algo.setParameters(sirius_algo_par)


# TODO: Add preprocessing here! To use the featureMapping! 
#    run masstrace filter and feature mapping
#    vector<FeatureMap> v_fp; // copy FeatureMap via push_back
#   KDTreeFeatureMaps fp_map_kd; // reference to *basefeature in vector<FeatureMap>
#  FeatureMapping::FeatureToMs2Indices feature_mapping; // reference to *basefeature in vector<FeatureMap>
# https://github.com/OpenMS/OpenMS/blob/develop/src/utils/SiriusAdapter.cpp#L193
featureinfo= "./wf_testing/devoncoluted.featureXML"
spectra= exp
v_fp= []
fp_map_kd= KDTreeFeatureMaps()
feature_mapping = FeatureMapping_FeatureToMs2Indices() 
sirius_algo.preprocessingSirius(featureinfo,
                                spectra,
                                v_fp,
                                fp_map_kd,
                                sirius_algo,
                                feature_mapping)

print("preprocessed")
# TODO: Check feature and/or spectra number
# https://github.com/OpenMS/OpenMS/blob/develop/src/utils/SiriusAdapter.cpp#L201
sirius_algo.checkFeatureSpectraNumber(featureinfo,
                                    feature_mapping,
                                    spectra,
                                    sirius_algo)
print("checked")
# construct sirius ms file object
msfile = SiriusMSFile()
# create temporary filesystem objects
debug_level = 10
sirius_tmp = SiriusTemporaryFileSystemObjects(debug_level)
siriusstring= String(sirius_tmp.getTmpMsFile())

# fill variables, which are used in the function
# TODO: need to construct the feature mapping 
#feature_mapping = FeatureMapping_FeatureToMs2Indices() 
feature_only = True #SiriusAdapterAlgorithm.getFeatureOnly()==True
#this is a parameter, which is called "feature_only" 
#It is a boolean value (true/false) and if it is true you are using the  the feature information 
#from in_featureinfo to reduce the search space to MS2 associated with a feature.
#this is recommended when working with featureXML input, if you do NOT use it 
#sirius will use every individual MS2 spectrum for estimation (and it will take ages)
#bool feature_only = (sirius_algo.getFeatureOnly() == "true") ? true : false;
isotope_pattern_iterations = 3
no_mt_info = False #SiriusAdapterAlgorithm.getNoMasstraceInfoIsotopePattern() == False
compound_info = [] #SiriusMSFile_CompoundInfo()

msfile.store(spectra, 
             siriusstring, # has to be converted to an "OpenMS::String"
             feature_mapping, 
             feature_only,
             isotope_pattern_iterations, 
             no_mt_info, 
             compound_info)

print("stored")
#next step:call siriusQprocess
out_csi= CsiFingerIdMzTabWriter()
out_csifingerid= String(out_csi)
executable= "Users/eeko/Applications/sirius"
subdirs= sirius_algo.callSiriusQProcess(String(sirius_tmp.getTmpMsFile()),
                                String(sirius_tmp.getTmpOutDir()),
                                executable,
                                out_csifingerid,
                                sirius_algo)
print("SIRIUSQprocess")
#SiriusMZtabwriter for storage
candidates = sirius_algo.getCandidates()
sirius_result= MzTab()
siriusfile= MzTabFile()

input = "data Thermo Orbitrap ID-X/FileFiltered Std/ThermocentroidpentamycinFileFilter.mzML"
SiriusMzTabWriter.read(subdirs,
                        input,
                        candidates,
                        sirius_result)
print("storing..")
siriusfile.store("./wf_testing/out_sirius", sirius_result)
print("stored")

#CSI:FingerID
