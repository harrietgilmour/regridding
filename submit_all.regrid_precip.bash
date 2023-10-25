#!/bin/sh -l
#
# This script submits the jobs to run the regrid_precip.py script
#
# Usage: submit_all.regrid_precip.bash <year>
#
# For example: bash submit_all.regrid_precip.bash 2005
#

# Check that the year has been provided
if [ $# -ne 1 ]; then
    echo "Usage: submit_all.regrid_precip.bash <year>"
    exit 1
fi

# extract the year from the command line
year=$1

# set up the extractor script
EXTRACTOR="/data/users/hgilmour/regridding/submit.regrid_precip.sh"

# base directory is the directory where the tb and mask files are stored
# in format tb_merge_mm_yyyy.nc

precip_base_dir="/scratch/hgilmour/total_precip/yearly_files"

# Set up the output directory
OUTPUT_DIR="/data/users/hgilmour/regridding/lotus_output/precip"
mkdir -p $OUTPUT_DIR

    
echo $year

# Find the mask and tb files for the year
precip_file="total_precip_${year}.nc"
# construct the full paths
precip_path=${precip_base_dir}/${precip_file}

# Set up the output files
OUTPUT_FILE="$OUTPUT_DIR/regrid_precip.$year.out"
ERROR_FILE="$OUTPUT_DIR/regrid_precip.$year.err"

# submit the batch job
sbatch --mem=160000 --ntasks=4 --time=60 --output=$OUTPUT_FILE --error=$ERROR_FILE $EXTRACTOR $precip_path