### pyOpenMS_untargeted_metabolomics

##### This is the progress of a pyOpenMS workflow in a Jupyter notebook for untargeted metabolomics data preprocessing and analysis tailored by [Eftychia Eva Kontou](https://github.com/eeko-kon) using OpenMS and pyOpenMS which are python bindings to the cpp OpenMS alogithms. 

## Workflow overview
![dag](/images/pyOpenMS_workflows.svg)

The pipeline consists of three separate workflows that are interconnected, and one last data analysis notebook:

1) Pre-processing: converting raw data to a feature table with a series of algorithms 
![dag](/images/1_Preprocessing+SIRIUS_CSI_FingerID.svg)
2) GNPSexport: generate all the files necessary to create a FBMN job at GNPS. (see https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking-with-openms/) 
![dag](/images/2_GNPSExport.svg)
3) Re-quantification: missing value imputation resulted by the pre-processing workflow.
![dag](/images/3_Re-quantification.svg)
4) Data analysis: Annotate the FeatureMatrix with GNPS metabolites, formula and structural predictions, and perform outlier analysis to find features detected less frequently in the matrix.
![dag](/images/4_Data_analysis.svg)


## Usage
### Step 1: Clone the workflow

[Clone](https://help.github.com/en/articles/cloning-a-repository) this repository to your local system, into the place where you want to perform the data analysis.

(Make sure to have the right access / SSH Key. If **not**, follow the steps:
Step 1: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Step 2: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)


    git clone https://github.com/eeko-kon/pyOpenMS_untargeted_metabolomics.git

### Step 2: Create a conda environment& install pyopenms

Installing pyOpenMS using [conda](https://github.com/conda) is advised:

    conda create --name pyopenms python=3.8
    conda activate pyopenms
    pip install pyopenms

For installation details and further documentation, see: [pyOpenMS documentation](https://pyopenms.readthedocs.io/en/latest/).

#### For Linux only 

Install mono with sudo (https://www.mono-project.com/download/stable/#download-lin):

    sudo apt install mono-devel

#### For iOS only 

Install homebrew and wget (for **iOS** only!):

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
Press enter (RETURN) to continue 
    
    brew install wget

### Step 3: Retrieve files (optional) and executables (not optional)

#### Get example data from zenodo (only for testing the workflow with the example dataset) or simply transfer your own data under the directory "data/raw/"

    (cd data && wget https://zenodo.org/record/5511115/files/raw.zip && unzip *.zip -d raw)

#### Get the necessary executables (ThermoRawFileParser, OpenMS & sirius):
    
    (cd resources/ThermoRawFileParser && wget https://github.com/compomics/ThermoRawFileParser/releases/download/v1.3.4/ThermoRawFileParser.zip && unzip ThermoRawFileParser.zip)

#### For Linux only 

    (cd resources/Sirius/ && wget https://github.com/boecker-lab/sirius/releases/download/v4.9.3/sirius-4.9.3-linux64-headless.zip  && unzip *.zip)
    
    (cd resources  && wget https://github.com/OpenMS/OpenMS/releases/download/Release2.7.0/OpenMS-2.7.0-Debian-Linux-x86_64.deb && unzip *.zip)
    
#### For iOS only  

    (cd resources/Sirius/ && wget https://github.com/boecker-lab/sirius/releases/download/v4.9.6/sirius-4.9.6-osx64-headless.zip  && unzip *.zip)
    
    (cd resources && wget https://github.com/OpenMS/OpenMS/releases/download/Release2.7.0/OpenMS-2.7.0-macOS.dmg && unzip *.zip)

### Step 5: Run all kernels and investigate the results

All the results are in a csv format and can be opened simply with excel or using pandas dataframes. 


### Citations

Röst, H.L., Sachsenberg, T., Aiche, S., Bielow, C., Weisser, H., Aicheler, F., Andreotti, S., Ehrlich, H.-C., Gutenbrunner, P., Kenar, E., Liang, X., Nahnsen, S., Nilse, L., Pfeuffer, J., Rosenberger, G., Rurik, M., Schmitt, U., Veit, J., Walzer, M., Wojnar, D., Wolski, W.E.,Schilling, O., Choudhary, J.S., Malmström, L., Aebersold, R., Reinert, K., Kohlbacher, O. OpenMS: A flexible open-source software platform for mass spectrometry data analysis. Nature Methods, vol. 13, 2016. doi:10.1038/nmeth.3959

Kai Dührkop, Markus Fleischauer, Marcus Ludwig, Alexander A. Aksenov, Alexey V. Melnik, Marvin Meusel, Pieter C. Dorrestein, Juho Rousu, and Sebastian Böcker, SIRIUS 4: Turning tandem mass spectra into metabolite structure information. Nature Methods 16, 299–302, 2019 doi:10.1038/s41592-019-0344-8

Kai Dührkop, Huibin Shen, Marvin Meusel, Juho Rousu, and Sebastian Böcker, Searching molecular structure databases with tandem mass spectra using CSI:FingerID, PNAS October 13, 2015 112 (41) 12580-12585, doi:10.1073/pnas.1509788112


### Test Data (only for testing the workflow with the example dataset)
* Current test data are built from known metabolite producer strains or standard samples that have been analysed with a Thermo IDX mass spectrometer. The presence of the metabolites and their fragmentation patterns has been manually confirmed using TOPPView.


