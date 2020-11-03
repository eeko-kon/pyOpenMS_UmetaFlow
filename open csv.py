import numpy as np
import pandas as pd
import io 
"""
with open ("/Users/eeko/Desktop/20191218_NBC_UMETAB106_Salbus_711J_DCM_NEG_HIGHMASS_35.csv", "r") as MSdata:
    for line in MSdata:
        line = line.strip().split(",")
        if len(line) < 2:
            continue
        Time = line[0]
        Rel_abundance = line[1]
        print (Time + "\t" + Rel_abundance + "\n")    

"""
colnames = ["Time(min)", "Relative Abundance"]
data = pd.read_csv("/Users/eeko/Desktop/20191218_NBC_UMETAB106_Salbus_711J_DCM_NEG_HIGHMASS_35.csv", "w", delimiter= ",", skiprows=lambda x: x in [0,1,2], header = 0, engine = "python", usecols= ["Relative Abundance"])
print(data)

df = pd.DataFrame(data, columns = ["Time(min)", "Relative Abundance"])
Highest_Intensity = df["Relative Abundance"].max()
Lowest_Intensity = df["Relative Abundance"].min()
Sum_intensity = df["Relative Abundance"].sum()

print(Highest_Intensity)
print(Lowest_Intensity)
print(Sum_intensity)

#Rel_Abundance= df[df.columns[1:]]
#print(Rel_Abundance)
#print(type(Rel_Abundance))

#Intensity = df.Rel_Abundance.tolist()
#print(Rel_Abundance)
