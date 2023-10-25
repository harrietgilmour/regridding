#!/bin/sh -l
#
# This script submits the jobs to run the regrid_tb.py script
#
# Usage: submit_all.regrid_tb.bash <year>
#
# For example: bash submit_all.regrid_tb.bash 2005
#

# Check that the year has been provided
if [ $# -ne 1 ]; then
    echo "Usage: submit_all.regrid_tb.bash <year>"
    exit 1
fi

# extract the year from the command line
year=$1

# set up the extractor script
EXTRACTOR="/data/users/hgilmour/regridding/submit.regrid_tb.sh"

# base directory is the directory where the tb and mask files are stored
# in format tb_merge_mm_yyyy.nc

tb_base_dir="/data/users/hgilmour/tb"

# Set up the output directory
OUTPUT_DIR="/data/users/hgilmour/regridding/lotus_output/mask"
mkdir -p $OUTPUT_DIR

    
echo $year

# Find the mask and tb files for the year
tb_file="tb_${year}.nc"
# construct the full paths
tb_path=${tb_base_dir}/${tb_file}

# Set up the output files
OUTPUT_FILE="$OUTPUT_DIR/regrid_tb_cpm.$year.out"
ERROR_FILE="$OUTPUT_DIR/regrid_tb_cpm.$year.err"

# submit the batch job
sbatch --mem=200000 --ntasks=4 --time=60 --output=$OUTPUT_FILE --error=$ERROR_FILE $EXTRACTOR $tb_path