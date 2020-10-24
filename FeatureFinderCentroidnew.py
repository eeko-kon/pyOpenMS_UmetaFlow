from pyopenms import *

options = PeakFileOptions()
options.setMSLevels([1])
fh = MzMLFile()
fh.setOptions(options)

input_map = MSExperiment()
fh.load("raw_files/20200723_NBC_UMETAB137_Albus_O_acu_POS_009.mzML", input_map)
input_map.updateRanges()

ff = FeatureFinder()
ff.setLogType(LogType.CMD)

name = "centroided"
features = FeatureMap()
seeds = FeatureMap()
params = FeatureFinder().getParameters(name)
ff.run(name, input_map, features, params, seeds)

features.setUniqueIds()
fh = FeatureXMLFile()
fh.store("/py4e/store/hne.featureXML.featureXML", features)
print("Found", features.size(), "features")

retentions = []
mass = []
intensity = []
charges = []

for fe in features:
    retentions.append(fe.getRT())
    mass.append(fe.getMZ())
    intensity.append(fe.getIntensity())
    charges.append(fe.getCharge())

rimc = list(zip(retentions, intensity, mass, charges))
print(rimc[0])


def getKey(item):
    return item[0]
rimcSort = sorted(rimc, key=getKey)
print(rimcSort[0])

rt = [rimcSort[i][0] for i in range(0, len(rimcSort))]
ints = [rimcSort[i][1] for i in range(0, len(rimcSort))]

import pylab
plt.plot(rt, ints, '-')
pylab.xlabel('Retention (s)')
pylab.ylabel('Intensity')
pylab.show()