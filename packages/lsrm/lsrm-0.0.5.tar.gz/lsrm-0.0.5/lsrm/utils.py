# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:12:19 2019

@author: michaelek
"""
import os
import numpy as np
import pandas as pd
import geopandas as gpd
from pdsql import mssql

###################################################
### Parameters

base_dir = os.path.realpath(os.path.dirname(__file__))

#with open(os.path.join(base_dir, 'parameters.yml')) as param:
#    param = yaml.safe_load(param)


###################################################
### Functions


def ds_AET(pet, A, paw_now, paw_max):
    """
    Minhas et al. (1974) function used by David Scott to estimate 'actual ET' from PET and PAW. All inputs must be as floats.
    """

    aet = pet * ((1 - np.exp(-A*paw_now/paw_max))/(1 - 2*np.exp(-A) + np.exp(-A*paw_now/paw_max)))
    return aet
















