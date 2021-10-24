### pyOpenMS_untargeted_metabolomics

#### This is the progress of a pyOpenMS workflow in a Jupyter notebook for untargeted metabolomics data preprocessing and analysis tailored by [Eftychia Eva Kontou](https://github.com/eeko-kon) using OpenMS and pyOpenMS which are python bindings to the cpp OpenMS alogithms.  

## Workflow overview
![dag](/images/pyOpenMS_workflow.svg)

View the workflow with interactive comments in lucid: https://lucid.app/lucidchart/4dc81d37-bca3-4b2d-8253-33341ac79ab4/edit?viewport_loc=-71%2C53%2C2422%2C1416%2C0_0&invitationId=inv_5c1c0383-052a-4905-8146-dd842ee528fb 

## Usage
### Step 1: Clone the workflow

[Clone](https://help.github.com/en/articles/cloning-a-repository) this repository to your local system, into the place where you want to perform the data analysis.

(Make sure to have the right access / SSH Key. If **not**, follow the steps:
Step 1: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Step 2: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)


    git clone git@github.com:NBChub/snakemake-metabolomics.git


**Suggestion: Always add the genome ID in the filename for easier connection later to BGC_analytics.**

`samples.tsv` example:

|  sample_name |       comment                |
|-------------:|-----------------------------:|
| NBC_00162    | pyracrimicin                 |
| MDNA_WGS_14  | epemicins_A_B                |


### Step 2: Create a conda environment& install pyopenms

Installing Snakemake using [Mamba](https://github.com/mamba-org/mamba) is advised. In case you don’t use [Mambaforge](https://github.com/conda-forge/miniforge#mambaforge) you can always install [Mamba](https://github.com/mamba-org/mamba) into any other Conda-based Python distribution with:

    conda install -n base -c conda-forge mamba

Then install Snakemake with:

    mamba create -c conda-forge -c bioconda -n snakemake snakemake

For installation details, see the [instructions in the Snakemake documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

### Step 3: Retreive files and executables

#### Get input data from zenodo (only for testing the workflow with the example dataset) or simply transfer your own data under the directory "data/raw/"

    (cd data && wget https://zenodo.org/record/5511115/files/raw.zip && unzip *.zip -d raw)

#### Get the necessary executables (ThermoRawFileParser & sirius):
    
    (cd resources/ThermoRawFileParser && wget https://github.com/compomics/ThermoRawFileParser/releases/download/v1.3.4/ThermoRawFileParser.zip && unzip ThermoRawFileParser.zip)
    
    (cd resources/Sirius/ && wget https://github.com/boecker-lab/sirius/releases/download/v4.9.3/sirius-4.9.3-linux64-headless.zip  && unzip *.zip)

### Step 5: Run all kernels and investigate the results
All the results are in a csv format and can be opened simply with excel or using pandas dataframes. 


### Citations

Röst, H.L., Sachsenberg, T., Aiche, S., Bielow, C., Weisser, H., Aicheler, F., Andreotti, S., Ehrlich, H.-C., Gutenbrunner, P., Kenar, E., Liang, X., Nahnsen, S., Nilse, L., Pfeuffer, J., Rosenberger, G., Rurik, M., Schmitt, U., Veit, J., Walzer, M., Wojnar, D., Wolski, W.E.,Schilling, O., Choudhary, J.S., Malmström, L., Aebersold, R., Reinert, K., Kohlbacher, O. OpenMS: A flexible open-source software platform for mass spectrometry data analysis. Nature Methods, vol. 13, 2016. doi:10.1038/nmeth.3959

Kai Dührkop, Markus Fleischauer, Marcus Ludwig, Alexander A. Aksenov, Alexey V. Melnik, Marvin Meusel, Pieter C. Dorrestein, Juho Rousu, and Sebastian Böcker, SIRIUS 4: Turning tandem mass spectra into metabolite structure information. Nature Methods 16, 299–302, 2019.

Citation: Kai Dührkop, Huibin Shen, Marvin Meusel, Juho Rousu, and Sebastian Böcker, Searching molecular structure databases with tandem mass spectra using CSI:FingerID, PNAS October 13, 2015 112 (41) 12580-12585, https://doi.org/10.1073/pnas.1509788112


### Test Data (only for testing the workflow with the example dataset)
* Current test data are built from real runs of known metabolite producer strains or standard samples that have been already alanysed with the GUI Software Freestyle and confirmed the presence of fragmentation patterns for the specific metabolites.


