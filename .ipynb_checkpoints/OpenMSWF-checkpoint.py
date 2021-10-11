"""
#convert files from ThermoRawFileParser 
cd 
mono ThermoRawFileParser.exe -d=/Users/eeko/Desktop/py4e/rawdata/mgf/ -f=0 -g 
mono ThermoRawFileParser.exe -d=/Users/eeko/Desktop/py4e/rawdata/mzML/ 

this command will automatically convert the files to centroid mzML
"""
#import numpy as np 
#import pandas as pd
from pyopenms import *
input_mzML = "./rawdata/mzML/CollinusKirromycin.mzML"

exp = MSExperiment()
print("Loading")
MzMLFile().load(input_mzML, exp)
print("Loaded")
print(exp.getSourceFiles()[0].getNativeIDTypeAccession())
print(exp.getSourceFiles()[0].getNativeIDType())

# sorty my m/z
exp.sortSpectra(True)

delta_mzs= []
mzs = []
rts= []
PrecursorCorrection.correctToHighestIntensityMS1Peak(exp, 100.0, True, delta_mzs, mzs, rts)

# Run mass trace detection
mass_traces = []
mtd = MassTraceDetection()
mtd_par = mtd.getDefaults()
# set addition parameters values
mtd_par.setValue("mass_error_ppm", 10.0) # example set ppm error
mtd_par.setValue("noise_threshold_int", 1.0e04)
mtd.setParameters(mtd_par)
print(mtd_par.getValue("mass_error_ppm")) # example check a specific value
mtd.run(exp, mass_traces, 0)  # 0 is default and does not restrict found mass traces

# Run elution peak detection
mass_traces_split = []
mass_traces_final = []
epd = ElutionPeakDetection()
epd_par = epd.getDefaults()
# set additional parameter values
epd_par.setValue("width_filtering", "fixed")
epd.setParameters(epd_par)
epd.detectPeaks(mass_traces, mass_traces_split)

if (epd.getParameters().getValue("width_filtering") == "auto"):
    epd.filterByPeakWidth(mass_traces_split, mass_traces_final)
else:
    mass_traces_final = mass_traces_split

# Run feature detection
feature_map_FFM = FeatureMap()
feat_chrom = []
ffm = FeatureFindingMetabo()
ffm_par = ffm.getDefaults() 
# set additional parameter values
ffm_par.setValue("isotope_filtering_model", "none")
ffm_par.setValue("remove_single_traces", "false")
ffm_par.setValue("mz_scoring_by_elements", "false")
ffm.setParameters(ffm_par)
ffm.run(mass_traces_final, feature_map_FFM, feat_chrom)

print('# Mass traces filtered:', len(mass_traces_final))

feature_map_FFM.setUniqueIds()
fh = FeatureXMLFile()
print("Found", feature_map_FFM.size(), "features")
fh.store('./pyOpenMS_results/FeatureFindingMetaboKirr.featureXML', feature_map_FFM)

# Run metabolite adduct decharging detection
# With SIRIUS you are only able to use singly charged adducts
mfd = MetaboliteFeatureDeconvolution()
mdf_par = mfd.getDefaults()
# set additional parameter values
mdf_par.setValue("potential_adducts",  [b"H:+:0.6",b"Na:+:0.2",b"NH4:+:0.1", b"H2O:-:0.1"])
mdf_par.setValue("charge_min", 1, "Minimal possible charge")
mdf_par.setValue("charge_max", 1, "Maximal possible charge")
mdf_par.setValue("charge_span_max", 1)
mdf_par.setValue("max_neutrals", 1)
print(mdf_par.getValue("potential_adducts")) # test if adducts have been set correctly
mfd.setParameters(mdf_par)

feature_map_DEC = FeatureMap()
cons_map0 = ConsensusMap()
cons_map1 = ConsensusMap()
mfd.compute(feature_map_FFM, feature_map_DEC, cons_map0, cons_map1)
fmdec= FeatureXMLFile()
fmdec.store("./pyOpenMS_results/deconvolutedKirr.featureXML", feature_map_DEC)

# Precursor corrector

PrecursorCorrection.correctToNearestFeature(feature_map_DEC, exp, 0.0, 100.0, True, False, False, False, 3, 0)

# Prepare sirius parameters
sirius_algo = SiriusAdapterAlgorithm()

sirius_algo_par = sirius_algo.getDefaults()

sirius_algo_par.setValue("preprocessing:filter_by_num_masstraces", 2) 
sirius_algo_par.setValue("preprocessing:precursor_mz_tolerance", 10.0) #default
sirius_algo_par.setValue("preprocessing:precursor_mz_tolerance_unit", "ppm")
sirius_algo_par.setValue("preprocessing:precursor_rt_tolerance", 5.0) #default
sirius_algo_par.setValue("preprocessing:feature_only", "true")
sirius_algo_par.setValue("sirius:profile", "orbitrap")
sirius_algo_par.setValue("sirius:db", "none")
sirius_algo_par.setValue("sirius:ions_considered", "[M+H]+, [M-H2O+H]+, [M+Na]+, [M+NH4]+")
sirius_algo_par.setValue("sirius:candidates", 10)
sirius_algo_par.setValue("sirius:elements_enforced", "CHNOS") 
sirius_algo_par.setValue("project:processors", 2)
sirius_algo_par.setValue("fingerid:db", "BIO")
sirius_algo.setParameters(sirius_algo_par)

featureinfo = "./pyOpenMS_results/deconvolutedKirr.featureXML"
fm_info = FeatureMapping_FeatureMappingInfo()
feature_mapping = FeatureMapping_FeatureToMs2Indices() 
sirius_algo.preprocessingSirius(featureinfo,
                                exp,
                                fm_info,
                                feature_mapping)

print("preprocessed")
# Check feature and/or spectra number
# https://github.com/OpenMS/OpenMS/blob/develop/src/utils/SiriusAdapter.cpp#L201
sirius_algo.logFeatureSpectraNumber(featureinfo, 
                                    feature_mapping,
                                    exp)

print("checked")

# construct sirius ms file object
msfile = SiriusMSFile()
# create temporary filesystem objects
debug_level = 3
sirius_tmp = SiriusTemporaryFileSystemObjects(debug_level)
siriusstring= String(sirius_tmp.getTmpMsFile())

# fill variables, which are used in the function
# this is a parameter, which is called "feature_only"
# It is a boolean value (true/false) and if it is true you are using the  the feature information
# from in_featureinfo to reduce the search space to MS2 associated with a feature.
# this is recommended when working with featureXML input, if you do NOT use it
# sirius will use every individual MS2 spectrum for estimation (and it will take ages)

feature_only = sirius_algo.isFeatureOnly()
isotope_pattern_iterations = sirius_algo.getIsotopePatternIterations()
no_mt_info = sirius_algo.isNoMasstraceInfoIsotopePattern()
compound_info = []

msfile.store(exp, 
             String(sirius_tmp.getTmpMsFile()),
             feature_mapping, 
             feature_only,
             isotope_pattern_iterations, 
             no_mt_info, 
             compound_info)
print(String(sirius_tmp.getTmpMsFile()))
print("stored")


#next step:call siriusQprocess
out_csifingerid = "./pyOpenMS_results/csifingerIDKirr.mzTab" # empty string, since no file was specified - no CSIFingerId Output will be generated
executable= "/Users/eeko/Desktop/software/Contents/MacOS/sirius"
subdirs = sirius_algo.callSiriusQProcess(String(sirius_tmp.getTmpMsFile()),
                                         String(sirius_tmp.getTmpOutDir()),
                                         String(executable),
                                         String(out_csifingerid),
                                         False) # debug option not yet implemented
print("SIRIUSQprocess")
#SiriusMZtabwriter for storage
candidates = sirius_algo.getNumberOfSiriusCandidates()
sirius_result = MzTab()
siriusfile = MzTabFile()
SiriusMzTabWriter.read(subdirs,
                        input_mzML,
                        candidates,
                        sirius_result)
print("storing..")
siriusfile.store("./pyOpenMS_results/out_sirius_testKirr.mzTab", sirius_result)
print("stored")

#CSI:FingerID
top_hits= 5
csi_result=MzTab()
csi_file=MzTabFile()
CsiFingerIdMzTabWriter.read(subdirs,
                    input_mzML,
                    top_hits,
                    csi_result)

csi_file.store("./pyOpenMS_results/csifingerIDKirr.mzTab", csi_result)
