from pyopenms import *

def pyopenms_WF(filename):
    exp = MSExperiment()
    MzMLFile().load(filename, exp)
    exp.sortSpectra(True)
    
    mass_traces = []
    mtd = MassTraceDetection()
    mtd_par = mtd.getDefaults()
    mtd_par.setValue("mass_error_ppm", 10.0) 
    mtd_par.setValue("noise_threshold_int", 1.0e04)
    mtd.setParameters(mtd_par)
    mtd.run(exp, mass_traces, 0)
    
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
    fh.store('./mzML_files/wf_testing/FeatureFindingMetabo.featureXML', feature_map_FFM)
    
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
    fxml.store("./mzML_files/wf_testing/deconvoluted.featureXML", feature_map_DEC)
    
    out_mzml= "./mzML_files/wf_testing/PrecursorCorrected.mzML"
    features= FeatureMap()
    FeatureXMLFile().load("./mzML_files/wf_testing/deconvoluted.featureXML", features)
    PrecursorCorrection.correctToNearestFeature(features, exp, 0.0, 100.0, True, False, False, False, 3, 0)
    MzMLFile().store(out_mzml, exp)
    
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
    
    featureinfo = "./mzML_files/wf_testing/deconvoluted.featureXML"
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
    out_csifingerid = "./mzML_files/wf_testing/csifingerID.mzTab" 
    executable= "/Users/eeko/Desktop/software/Contents/MacOS/sirius"
    subdirs = sirius_algo.callSiriusQProcess(String(sirius_tmp.getTmpMsFile()),
                                             String(sirius_tmp.getTmpOutDir()),
                                             String(executable),
                                             String(out_csifingerid),
                                             False)
    candidates = sirius_algo.getNumberOfSiriusCandidates()
    sirius_result = MzTab()
    siriusfile = MzTabFile()
    SiriusMzTabWriter.read(subdirs,
                            filename,
                            candidates,
                            sirius_result)
    siriusfile.store("./mzML_files/wf_testing/out_sirius_test.mzTab", sirius_result)
    top_hits= 5
    csi_result=MzTab()
    csi_file=MzTabFile()
    CsiFingerIdMzTabWriter.read(subdirs,
                        filename,
                        top_hits,
                        csi_result)
    csi_file.store("./mzML_files/wf_testing/csifingerID.mzTab", csi_result)
    return "FINITO"