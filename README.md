# py4e
## This is the progress of a pyOpenMS workflow to dereplicate untargeted metabo data 
#### Old file: Workflownew.py
#### Newest version: pyOpenMS functions.py where I split Workflownew.py into functions and
#### raw_data_processing.ipynb where I am trying to parse through a directory with glob (doesn't work because pyOpenMS works only with 1 file at a time, and glob with give a list of files)

## Link for the raw and converted data:
#### https://drive.google.com/drive/folders/1O0JmZa17oqyzObAjphbXxyHmE9LF6Tkf?usp=sharing

#### Agilent files cannot run right now in pyopenms 

#### raw data Thermo Orbitrap: *.raw files of standards Germicidins A (1 and 2 are the same - 1 is just higher concentration of the standard) and B. 

#### mzml convert: MS1 and MS2 converted to centroid

#### FileFiltered : all files have negative intensities (from Thermo) and had to be filtered through OpenMS to only keep positive ones.

#### KNIME test workflow also added
