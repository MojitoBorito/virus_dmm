#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --output /nfs/home/students/m.patil/ba/logs/nextflow_%j.out
#SBATCH --error /nfs/home/students/m.patil/ba/logs/nextflow_%j.err
#SBATCH --partition=exbio-cpu
#SBATCH --job-name=cat_hsv
#SBATCH --cpus-per-task=2
#SBATCH --mem=24G
#SBATCH --time=32:00:00

mkdir -p /nfs/home/students/m.patil/ba/logs
mkdir -p /nfs/home/students/m.patil/ba/apptainer_cache
mkdir -p /nfs/scratch/singularity_tmp/m.patil

source /opt/mambaforge/etc/profile.d/conda.sh
conda activate daisy-env

export TMPDIR=/nfs/scratch/singularity_tmp/m.patil
export NXF_SINGULARITY_CACHEDIR=/nfs/home/students/m.patil/ba/apptainer_cache
export SINGULARITY_TMPDIR=/nfs/scratch/singularity_tmp/m.patil
export SINGULARITY_LOCALCACHEDIR=/nfs/scratch/singularity_tmp/m.patil

echo "=========================================="
echo "Starting hsv run -- $(date)"
echo "=========================================="
nextflow run ../diseasemodulediscovery/. \
    -profile daisybio,apptainer,keep_work \
    --skip_annotation \
    --skip_digest \
    --input input_sheets/hsv_samplesheet_subcategories.csv \
    --id_space uniprot \
    --outdir subcategories_outputs/hsv \
    --publish_dir_mode symlink
echo "hsv done -- $(date)"