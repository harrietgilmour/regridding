#!/bin/bash
#SBATCH --mem=160000
#SBATCH --ntasks=4
#SBATCH --time=60

#Extract args from command line
precip_file=$1

# Print the tracks file
echo "$precip_file"

# Run the unique_cells.py script
python regrid_precip.py ${precip_file}