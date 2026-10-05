#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --output /nfs/home/students/m.patil/ba/logs/nextflow_%j.out
#SBATCH --error /nfs/home/students/m.patil/ba/logs/nextflow_%j.err
#SBATCH --partition=exbio-cpu
#SBATCH --job-name=diseasemodulediscovery
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=24:00:00

mkdir -p /nfs/home/students/m.patil/ba/logs
mkdir -p /nfs/home/students/m.patil/ba/apptainer_cache

source /opt/mambaforge/etc/profile.d/conda.sh
conda activate daisy-env

export NXF_SINGULARITY_CACHEDIR=/nfs/home/students/m.patil/ba/apptainer_cache

echo "=========================================="
echo "Starting CORONA run -- $(date)"
echo "=========================================="
nextflow run ../diseasemodulediscovery/. \
    -profile daisybio,singularity \
    --skip_annotation \
    --skip_digest \
    --input input_sheets/corona_input.csv \
    --id_space uniprot \
    --outdir outputs/corona \
    --skip_gprofiler
echo "CORONA done -- $(date)"

echo "=========================================="
echo "Starting HIV run -- $(date)"
echo "=========================================="
nextflow run ../diseasemodulediscovery/. \
    -profile daisybio,singularity \
    --skip_annotation \
    --skip_digest \
    --input input_sheets/hiv_input.csv \
    --id_space uniprot \
    --outdir outputs/hiv \
    --skip_gprofiler
echo "HIV done -- $(date)"

echo "=========================================="
echo "Starting HSV run -- $(date)"
echo "=========================================="
nextflow run ../diseasemodulediscovery/. \
    -profile daisybio,singularity \
    --skip_annotation \
    --skip_digest \
    --input input_sheets/hsv_input.csv \
    --id_space uniprot \
    --outdir outputs/hsv \
    --skip_gprofiler
echo "HSV done -- $(date)"

echo "=========================================="
echo "All runs completed -- $(date)"
echo "=========================================="