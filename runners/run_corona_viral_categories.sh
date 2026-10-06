#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --output /nfs/home/students/m.patil/ba/logs/nextflow_%j.out
#SBATCH --error /nfs/home/students/m.patil/ba/logs/nextflow_%j.err
#SBATCH --partition=exbio-cpu
#SBATCH --job-name=vir_corona
#SBATCH --cpus-per-task=2
#SBATCH --mem=24G
#SBATCH --time=32:00:00

#mkdir -p /nfs/home/students/m.patil/ba/logs
#mkdir -p /nfs/home/students/m.patil/ba/apptainer_cache
#mkdir -p /nfs/scratch/singularity_tmp/m.patil

source /opt/mambaforge/etc/profile.d/conda.sh
conda activate daisy-env

export TMPDIR=/nfs/scratch/singularity_tmp/m.patil
export NXF_SINGULARITY_CACHEDIR=/nfs/home/students/m.patil/ba/apptainer_cache
export SINGULARITY_TMPDIR=/nfs/scratch/singularity_tmp/m.patil
export SINGULARITY_LOCALCACHEDIR=/nfs/scratch/singularity_tmp/m.patil

echo "=========================================="
echo "Starting Corona run -- $(date)"
echo "=========================================="
nextflow run ../diseasemodulediscovery/. \
    -profile daisybio,singularity,keep_work \
    --skip_annotation \
    --skip_digest \
    --input input_sheets/corona_viral_comparisons.csv \
    --id_space uniprot \
    --outdir viral_categories/corona \
    --publish_dir_mode symlink
echo "Corona done -- $(date)"