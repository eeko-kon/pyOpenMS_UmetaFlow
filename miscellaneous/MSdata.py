import numpy as np
import pandas as pd
import io 

colnames = ["Time(min)", "Relative Abundance"]
data = pd.read_csv("/Users/eeko/Desktop/20191218_NBC_UMETAB106_Salbus_711J_DCM_NEG_HIGHMASS_35.csv", "w", delimiter= ",", skiprows=lambda x: x in [0,1,2], header = 0, engine = "python")
print(data)

df = pd.DataFrame(data, columns = ["Time(min)", "Relative Abundance"])
Highest_Intensity = df["Relative Abundance"].max()
Lowest_Intensity = df["Relative Abundance"].min()
Sum_intensity = df["Relative Abundance"].sum()

print(Highest_Intensity)
print(Lowest_Intensity)
print(Sum_intensity)

row_count = len(data)
print(row_count)

Mean = (Sum_intensity/row_count)
print(Mean)

for MSdata in df["Relative Abundance"]:
    if MSdata > Mean:
        print(MSdata)

print(type(MSdata))
