#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 13:43:47 2020

@author: eeko
"""

import numpy as np
import pyopenms
import pyopenms as oms
import os
import sys
import imp
import re
import copy
import collections

exp = MSExperiment()
MzMLFile().load("20200723_NBC_UMETAB137_WGS14_standard_POS_005.mzML", exp)

OPENMS_OBJ_TYPES = (
     oms.PeakMap,
     oms.FeatureMap,
     oms.MSExperiment,
     oms.ConsensusMap,
     )
fmap = oms.FeatureMap()
mass_traces = []
mass_traces_split = []
mass_traces_filtered  = []
options = oms.PeakFileOptions()
options.setMSLevels([1])
fh = oms.MzXMLFile()
fh.setOptions(options)
peak_map = oms.PeakMap()

print('# Spectra:', len(exp.getSpectra() ))
print('# Chromatograms:', len(exp.getChromatograms() ) )

mass_trace_detect = oms.MassTraceDetection()
mass_trace_detect.run(peak_map, mass_traces)

