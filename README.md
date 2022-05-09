### pyOpenMS_untargeted_metabolomics

##### This is the progress of a pyOpenMS workflow in a Jupyter notebook for untargeted metabolomics data preprocessing and analysis tailored by [Eftychia Eva Kontou](https://github.com/eeko-kon) and [Axel Walter](https://github.com/axelwalter) using OpenMS and pyOpenMS which are python bindings to the cpp OpenMS alogithms. 

## Workflow overview

The pipeline consists of five interconnected steps:

1) [File conversion](1_FileConversion.ipynb) (optional): Simply add your Thermo raw files in data/raw/ and they will be converted to centroid mzML files. If you have Agilent or Bruker files, skip that step (write "FALSE" for rule fileconversion in the config.yaml file - see more under "Configure workflow") and convert them independently using proteowizard (see https://proteowizard.sourceforge.io/) and add them to the data/mzML/ directory.

2) [Pre-processing](2_Preprocessing_requant.ipynb): converting raw data to a feature table with a series of algorithms & re-quantification: Re-quantify all raw files to avoid missing values resulted by the pre-processing workflow for statistical analysis and data exploration.

3) Structural and formula predictions with [SIRIUS and CSI:FingeID](3_SIRIUS_CSI.ipynb)

4) [GNPSexport](4_GNPSExport.ipynb): generate all the files necessary to create a FBMN job at GNPS. (see https://ccms-ucsd.github.io/GNPSDocumentation/featurebasedmolecularnetworking-with-openms/) 

5) [Annotation](5_Annotation.ipynb): annotate the feature tables with #1 ranked SIRIUS and CSI:FingerID predictions, as well as GNPS MSMS library matching annotations.

![dag](/images/MetabolomicsFlow.svg)


## Usage
### Step 1: Clone the workflow

[Clone](https://help.github.com/en/articles/cloning-a-repository) this repository to your local system, into the place where you want to perform the data analysis.

(Make sure to have the right access / SSH Key. If **not**, follow the steps:
Step 1: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Step 2: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)


    git clone https://github.com/eeko-kon/pyOpenMS_untargeted_metabolomics.git

### Step 2: Create a conda environment& install pyopenms
    
Installing pyOpenMS using [conda](https://github.com/conda) is advised:
First, get the latest wheels:

    MY_OS="Linux" # or "macOS" or "Windows" (case-sensitive)
    wget https://nightly.link/OpenMS/OpenMS/workflows/pyopenms-wheels/nightly/${MY_OS}-wheels.zip\?status\=completed
    mv ${MY_OS}-wheels.zip\?status=completed ${MY_OS}-wheels.zip
    unzip *.zip

    conda create --name pyopenms python=3.10
    conda activate pyopenms
    pip install *.whl

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

#### Get the necessary executables (ThermoRawFileParser & Sirius):
    
    (cd resources/ThermoRawFileParser && wget https://github.com/compomics/ThermoRawFileParser/releases/download/v1.3.4/ThermoRawFileParser.zip && unzip ThermoRawFileParser.zip)
    
    conda install -c bioconda sirius-csifingerid

    pip install pyteomics

    pip install --upgrade nbformat

    pip install matplotlib
### Step 5: Run all kernels and investigate the results

All the results are in a csv format and can be opened simply with excel or using pandas dataframes. 


### Citations

Röst, H.L., Sachsenberg, T., Aiche, S., Bielow, C., Weisser, H., Aicheler, F., Andreotti, S., Ehrlich, H.-C., Gutenbrunner, P., Kenar, E., Liang, X., Nahnsen, S., Nilse, L., Pfeuffer, J., Rosenberger, G., Rurik, M., Schmitt, U., Veit, J., Walzer, M., Wojnar, D., Wolski, W.E.,Schilling, O., Choudhary, J.S., Malmström, L., Aebersold, R., Reinert, K., Kohlbacher, O. OpenMS: A flexible open-source software platform for mass spectrometry data analysis. Nature Methods, vol. 13, 2016. doi:10.1038/nmeth.3959

Kai Dührkop, Markus Fleischauer, Marcus Ludwig, Alexander A. Aksenov, Alexey V. Melnik, Marvin Meusel, Pieter C. Dorrestein, Juho Rousu, and Sebastian Böcker, SIRIUS 4: Turning tandem mass spectra into metabolite structure information. Nature Methods 16, 299–302, 2019 doi:10.1038/s41592-019-0344-8

Kai Dührkop, Huibin Shen, Marvin Meusel, Juho Rousu, and Sebastian Böcker, Searching molecular structure databases with tandem mass spectra using CSI:FingerID, PNAS October 13, 2015 112 (41) 12580-12585, doi:10.1073/pnas.1509788112


### Test Data (only for testing the workflow with the example dataset)
* Current test data are built from known metabolite producer strains or standard samples that have been analysed with a Thermo IDX mass spectrometer. The presence of the metabolites and their fragmentation patterns has been manually confirmed using TOPPView.


