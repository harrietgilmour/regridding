#!/bin/bash
#SBATCH --mem=200000
#SBATCH --ntasks=4
#SBATCH --time=60

#Extract args from command line
tb_file=$1

# Print the tracks file
echo "$tb_file"

# Run the unique_cells.py script
python regrid_tb.py ${tb_file}