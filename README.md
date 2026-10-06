# Evaluating Input Construction Strategies for Network-Based Disease Module Discovery in Viral Diseases

## Setup
To use the nf-core/diseasemodulediscovery pipeline with the blacklist integration, please use the version under https://github.com/MojitoBorito/diseasemodulediscovery. For the running scripts and sample sheets to work follow the following file structure:

```
.
├── virus_dmm (this repository)
└── diseasemodulediscovery (https://github.com/MojitoBorito/diseasemodulediscovery)
```

### Requirements
- R version 4.6.1 (newer versions should also be compatible)
    - R packages:
        - tidyverse
        - ggplot2
        - ggh4x
        - readr
        - ggVennDiagram
        - patchwork
        - RColorBrewer
        - ggrepel
        - GO.db
        - org.Hs.eg.db
        - AnnotationDbi
        - httr2
        - fs
        - biomaRt
- Python 3.12.9
    - Python packages:
        - pandas
- Nextflow 26.04.0

The whole environment can be created using requirements.yml

## Input Construction
The following files are required to construc the inputs:
- virfil.py (IntAct and HVIDB)
- intact_filter.py (IntAct)
- data_gen.Rmd (Open Targets (all))
- vhi_qc.Rmd (IntAct and HVIDB (metadata filtering))
- sub_categorization.Rmd (IntAct and HVIDB (protein categorization))

The shell scripts under create_inputs create the inputs for the following:
- create_data.sh: unfiltered data for HVIDB and IntAct
- test_interactions.sh: Top 50 and top 100 confidence score filtered interactions for IntAct
- test_top_human.sh: Top n (named same_n), top 50 and top 100 confidence score filtered seeds for IntAct applied on network extended by virus host, intraviral and intra-human interactions 
- test_top.sh: Top n (named same_n), top 50 and top 100 confidence score filtered seeds for IntAct applied on standard networks
- test_top_virus.sh: Top n (named same_n), top 50 and top 100 confidence score filtered seeds for IntAct applied on network extended by virus host and intraviral

## Pipeline Execution
The runners include the slurm scripts used to execute the Nextflow pipeline on the daisybio server, independantly for each virus. Please remove the daisybio and keep_work from the profile to execute locally. 
The run files run the following categories: 
- run_(virus).sh: unfiltered seeds
- *filtered.sh: top n, 50 and 100 confidence score filtered seeds
- *human.sh: top n, 50 and 100 confidence score filtered human seeds applied on network extended by virus host, intraviral and intra-human interactions
- *interaction_filter.sh: seeds from top 50 and 100 confidence score filtered interactions 
- *viral_categories.sh: viral seeds filtered by metadata and all viral seeds applied on network extended by virus host, intraviral and intra-human interactions
- *_categories.sh: human seeds filtered by metadata
- *_categories_sub.sh: seeds categorised by their role in viral process GO term

The input samplesheets for the corresponding runs can be found under input_sheets

## Plots
- vhi_qc.Rmd: code for seed set size plots for base seeds and other distributions
- sub_categorization.Rmd: code for seed size plots for seeds categorised by their role in viral process GO term
- topology_analysis.Rmd: code for module size plots
- pathway_analysis.Rmd: code for pathway analysis bar plots
- drugs.Rmd: code for drug profile plots and recall. 

