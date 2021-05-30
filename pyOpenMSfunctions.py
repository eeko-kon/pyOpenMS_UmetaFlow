from pyopenms import *
import glob
import pandas as pd
import os

def prepare_output_directory(name: str, filename: str) -> None:
    input_prefix = os.path.basename(filename(input_file, "", get_config()))
    if not name:
        name = os.path.abspath(input_prefix)
        update_config({"pyOpenMS_results": name})

    if os.path.exists(name):
        if not os.path.isdir(name):
            raise RuntimeError("Output directory %s exists and is not a directory" % name)
        # not empty (apart from a possible input dir), and not reusing its results
        if not input_file.endswith(".mzML") and \
                list(filter(_ignore_patterns, glob.glob(os.path.join(name, "*")))):
            raise RuntimeError("Output directory contains other files, aborting for safety")


def FFM(filename):
    exp = MSExperiment()
    input_mzML= filename
    MzMLFile().load(input_mzML, exp)
    exp.sortSpectra(True) # Sort the data points by retention time.
    mass_traces = []
    mtd = MassTraceDetection()
    mtd_par = mtd.getDefaults()
    mtd_par.setValue("mass_error_ppm", 10.0) 
    mtd_par.setValue("noise_threshold_int", 1.0e04)
    mtd.setParameters(mtd_par)
    mtd.run(exp, mass_traces, 0)  # 0 is default and does not restrict found mass traces
    mass_traces_split = []
    mass_traces_final = []
    epd = ElutionPeakDetection()
    epd_par = epd.getDefaults()
    epd_par.setValue("width_filtering", "fixed")
    epd.setParameters(epd_par)
    epd.detectPeaks(mass_traces, mass_traces_split)
    if (epd.getParameters().getValue("width_filtering") == "auto"):
        epd.filterByPeakWidth(mass_traces_split, mass_traces_final)
    else:
        mass_traces_final = mass_traces_split
    feature_map_FFM = FeatureMap()
    feat_chrom = []
    ffm = FeatureFindingMetabo()
    ffm_par = ffm.getDefaults() 
    ffm_par.setValue("isotope_filtering_model", "none")
    ffm_par.setValue("remove_single_traces", "true")
    ffm_par.setValue("mz_scoring_by_elements", "true")
    ffm.setParameters(ffm_par)
    ffm.run(mass_traces_final, feature_map_FFM, feat_chrom)
    feature_map_FFM.setUniqueIds()
    fh = FeatureXMLFile()
    fh.store('./pyOpenMS_results/FFM.featureXML', feature_map_FFM)
    return 

def MFD(filename):
    mfd = MetaboliteFeatureDeconvolution()
    mdf_par = mfd.getDefaults()
    mdf_par.setValue("potential_adducts",  [b"H:+:0.6",b"Na:+:0.2",b"NH4:+:0.1", b"H2O:-:0.1"])
    mdf_par.setValue("charge_min", 1, "Minimal possible charge")
    mdf_par.setValue("charge_max", 1, "Maximal possible charge")
    mdf_par.setValue("charge_span_max", 1)
    mdf_par.setValue("max_neutrals", 1)
    mfd.setParameters(mdf_par)
    feature_map_DEC = FeatureMap()
    cons_map0 = ConsensusMap()
    cons_map1 = ConsensusMap()
    mfd.compute(feature_map_FFM, feature_map_DEC, cons_map0, cons_map1)
    fxml = FeatureXMLFile()
    fxml.store("./pyOpenMS_results/MFD.featureXML", feature_map_DEC)
    return

def PC(filename):
    delta_mzs= []
    mzs = []
    rts= []
    PrecursorCorrection.correctToHighestIntensityMS1Peak(exp, 100.0, True, delta_mzs, mzs, rts)
    return

def SIRIUS(filename):
    sirius_algo = SiriusAdapterAlgorithm()
    sirius_algo_par = sirius_algo.getDefaults()
    sirius_algo_par.setValue("preprocessing:filter_by_num_masstraces", 2) 
    sirius_algo_par.setValue("preprocessing:precursor_mz_tolerance", 10.0)
    sirius_algo_par.setValue("preprocessing:precursor_mz_tolerance_unit", "ppm")
    sirius_algo_par.setValue("preprocessing:precursor_rt_tolerance", 5.0)
    sirius_algo_par.setValue("preprocessing:feature_only", "true")
    sirius_algo_par.setValue("sirius:profile", "orbitrap")
    sirius_algo_par.setValue("sirius:db", "all")
    sirius_algo_par.setValue("sirius:ions_considered", "[M+H]+, [M-H2O+H]+, [M+Na]+, [M+NH4]+")
    sirius_algo_par.setValue("sirius:candidates", 5)
    sirius_algo_par.setValue("sirius:elements_enforced", "CHNOP") 
    sirius_algo_par.setValue("project:processors", 2)
    sirius_algo.setParameters(sirius_algo_par)
    featureinfo = "./pyOpenMS_results/MFD.featureXML"
    fm_info = FeatureMapping_FeatureMappingInfo()
    feature_mapping = FeatureMapping_FeatureToMs2Indices() 
    sirius_algo.preprocessingSirius(featureinfo,
                                    exp,
                                    fm_info,
                                    feature_mapping)
    sirius_algo.logFeatureSpectraNumber(featureinfo, 
                                        feature_mapping,
                                        exp)
    msfile = SiriusMSFile()
    debug_level = 10
    sirius_tmp = SiriusTemporaryFileSystemObjects(debug_level)
    siriusstring= String(sirius_tmp.getTmpMsFile())
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
    out_csifingerid = "./pyOpenMS_results/csifingerID.mzTab" # empty string " " : when no file is specified, no CSIFingerId Output will be generated
    subdirs = sirius_algo.callSiriusQProcess(String(sirius_tmp.getTmpMsFile()),
                                             String(sirius_tmp.getTmpOutDir()),
                                             String(SIRIUS_EXECUTABLE_PATH),
                                             String(out_csifingerid),
                                             False)
    
    candidates = sirius_algo.getNumberOfSiriusCandidates()
    sirius_result = MzTab()
    siriusfile = MzTabFile()
    SiriusMzTabWriter.read(subdirs,
                            filename,
                            candidates,
                            sirius_result)
    siriusfile.store("./pyOpenMS_results/out_sirius_test.mzTab", sirius_result)
    top_hits= 5
    csi_result=MzTab()
    csi_file=MzTabFile()
    CsiFingerIdMzTabWriter.read(subdirs,
                        filename,
                        top_hits,
                        csi_result)

    csi_file.store("./pyOpenMS_results/csifingerID.mzTab", csi_result)
    return print(String(sirius_tmp.getTmpMsFile()))