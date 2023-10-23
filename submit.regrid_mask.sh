#!/bin/bash
#SBATCH --mem=200000
#SBATCH --ntasks=4
#SBATCH --time=60

#Extract args from command line
mask_file=$1
tb_file=$2

# Print the tracks file
echo "$mask_file"
echo "$tb_file"

# Run the unique_cells.py script
python regrid_mask.py ${mask_file} ${tb_file}