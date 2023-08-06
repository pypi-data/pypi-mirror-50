#!/usr/bin/env python3

import pkg_resources
from irisreader import sji_cube, raster_cube, observation

DATA_PATH = pkg_resources.resource_filename( 'irisreader', 'data/' )

def sample_sji( keep_null=False ):
    """
    Returns a sample SJI data cube.
    
    Parameters
    ----------
    keep_null : boolean
        whether to load images that are NULL (-200) everywhere

    Returns
    -------
    sji_cube
        sample SJI data
    """

    return sji_cube( DATA_PATH + "/IRIS_SJI_test.fits", keep_null=keep_null )

def sample_raster( line='Mg', keep_null=False ):
    """
    Returns a sample raster data cube.
    
    Parameters
    ----------
    line : str
        name or (unique) abbreviation of the desired line
    
    keep_null : boolean
        whether to load images that are NULL (-200) everywhere

    Returns
    -------
    raster_cube
        sample raster data
    
    """
    return raster_cube( [ DATA_PATH + "/IRIS_raster_test1.fits", DATA_PATH + "/IRIS_raster_test2.fits"], line=line, keep_null=keep_null )

def sample_observation( keep_null=False ):
    """
    Returns a sample IRIS observation.
    
    Parameters
    ----------
    keep_null : boolean
        whether to load images that are NULL (-200) everywhere

    Returns
    -------
    observation
        sample IRIS observation
    """
    
    return observation( DATA_PATH + "/20140518_151415_3820607204", keep_null=keep_null )
