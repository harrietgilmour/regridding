# Python script for to regrid segmentation.nc files from initial tracking output to 10km IMERG grid.
# This script also adds latitude and longitude (projection x and y) dimensions to the .nc files as they are missing, adds bounds, and adds a coordinate system
#
# <USAGE> python regrid_mask.py <MASK_FILE> <TB_FILE>
#
# <EXAMPLE> python regrid_mask.py /data/users/hgilmour/initial_tracks/tobac_initial_tracks/segmentation/segmentation_yearly_2005.nc /data/users/hgilmour/tb/2005/tb_2005.nc
#

# Import local packages
import os
import sys
import glob

# Import third party packages
import iris
import numpy as np
import pandas as pd
import cdo
from cdo import *
import xarray as xr

# Import and set up warnings
import warnings
warnings.filterwarnings('ignore')


# Function that will check the number of arguements passed
def check_no_args(args):
    """ Check the number of arguements passed"""
    if len(args) != 2:
        print("Incorrect number of arguements")
        print("Usage: python regrid_tb.py <TB_FILE>")
        print("Example: python feature_detection.py /data/users/hgilmour/tb/2005/tb_2005.nc")
        sys.exit(1)


# Write a function which loads the file
def open_datasets(tb_file):
    """ Load specified files"""

    #tb = iris.load_cube(tb_file)
    tb = iris.load(tb_file) # load all the cubes in the input file
    tb = tb[1]

    return tb


# Write a function which creates bounds and a coordinate system for a cube (for projection x and y named cubes)
def guesslatlonbounds_projection(cube):
    cube.coord('projection_x_coordinate').circular = True

    cs = iris.coord_systems.GeogCS(6371229)
    for coord in ['projection_y_coordinate','projection_x_coordinate']:
        if cube.coord(coord).bounds is None:
            cube.coord(coord).guess_bounds()
        if cube.coord(coord).coord_system is None:
            cube.coord(coord).coord_system = cs
            
    return cube

# Write a function which creates bounds and a coordinate system for a cube (for lat lon named cubes)
def guesslatlonbounds_latlon(cube):
    cube.coord('longitude').circular = True

    cs = iris.coord_systems.GeogCS(6371229)
    for coord in ['latitude','longitude']:
        if cube.coord(coord).bounds is None:
            cube.coord(coord).guess_bounds()
        if cube.coord(coord).coord_system is None:
            cube.coord(coord).coord_system = cs
            
    return cube


# Write a function which regrids the mask file to the 10km IMERG grid
def regrid(tb_coords, subset_imerg_coords):
    scheme = iris.analysis.AreaWeighted()

    regridded_tb =tb_coords.regrid(subset_imerg_coords, scheme)

    return regridded_tb



def main():
    #First extract the arguments:
    tb_file = str(sys.argv[1])

    # We want to extract the month and year from the tb_file path
    # An example of the path is:
    # /data/users/hgilmour/tb/2005/tb_merge_01_2005.nc
    # Extract the filename first
    filename = os.path.basename(tb_file)
    print("Type of filename:", type(filename))
    print("Filename:", filename)
    filename_without_extension = os.path.splitext(filename)
    #print("Type of filename_without_extension:", type(filename_without_extension))
    #print(filename_without_extension)
    filename = filename.replace(".", "_")
    segments = filename.split("_")
    print(segments)
    #segments = segments.split("_")
    #print(segments)
    year = segments[1]

    # Print the year
    print("year", year)

    # check the number of arguements:
    check_no_args(sys.argv)

              
    # Open the dataset
    tb = open_datasets(tb_file)
    print('datasets opened')

    # Create bounds and a coord system for the cube
    tb_coords = guesslatlonbounds_projection(tb)

    # Load imerg file (this reference file stays the same for each time this script is run)
    imerg_file = '/scratch/hgilmour/obs/precip/precip_2001.nc'

    imerg = iris.load(imerg_file)

    imerg = imerg[0]

    ## Take a small subset of imerg for testing ##

    imerg_subset = imerg[0:1,:,:]

    # Create bounds and a coord system for the IMERG dataset
    subset_imerg_coords = guesslatlonbounds_latlon(imerg_subset)

    # Regrid the mask file to the IMERG 10km grid
    regridded_tb = regrid(tb_coords, subset_imerg_coords)
    print('Re-gridding complete')

    # Save the file
    savefile = '/data/users/hgilmour/tb/regridded/regridded_tb_{}.nc'.format(year)

    iris.save(regridded_tb, savefile)
    print('File saved')

#Run the main function
if __name__ == "__main__":
    main()












