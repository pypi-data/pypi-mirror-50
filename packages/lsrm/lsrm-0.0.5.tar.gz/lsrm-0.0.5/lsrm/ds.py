# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 09:04:41 2019

@author: michaelek
"""
import numpy as np
from pdsql import mssql
from gistools import vector
from hydrointerp import Interp
from pyproj import Proj, CRS, Transformer
import os
import pandas as pd
import geopandas as gpd
import xarray as xr
from lsrm.utils import ds_AET, base_dir
try:
    import plotly.offline as py
    import plotly.graph_objs as go
except:
    print('install plotly for plot functions to work')


#######################################
### Class


class LSRM(object):
    """
    Class to perform a land surface recharge calculation according to the model developed by David Scott 2013. The three main methods include (in the order of operations)  soils_import, input_processing, and lsrm.

    Nothing needs to be passed at initialisation.
    """

    def __init__(self):
        """

        """
        pass


    def soils_import(self, irr_type_dict=None, paw_dict=None, paw_ratio=0.67, irr_file='AQUALINC_NZTM_IRRIGATED_AREA_20160629.pkl.xz', paw_file='LAND_NZTM_NEWZEALANDFUNDAMENTALSOILS.pkl.xz'):
        """
        Function to import polygon input data. At the moment, these include irrigation type and PAW. Inputs are dictionaries that reference either an MSSQL table with a geometry column or a shapefile. If the dictionary references an sql table then the keys should be 'server', 'database', 'table', and 'column'. If the dictionary references a shapefile, then the keys should be 'shp' and 'column'. All values should be strings.
        """

        if not any([isinstance(irr_type_dict, dict), isinstance(paw_dict, dict)]):
            irr1 = pd.read_pickle(os.path.join(base_dir, 'datasets', irr_file))
            paw1 = pd.read_pickle(os.path.join(base_dir, 'datasets', paw_file))
        else:

            if 'column' in irr_type_dict.keys():
                if not isinstance(irr_type_dict['column'], str):
                    raise TypeError("The key 'column' must be a string.")
            else:
                raise TypeError("The key 'column' must be in the dictionaries.")

            if 'shp' in irr_type_dict.keys():
                if not isinstance(irr_type_dict['shp'], str):
                    raise TypeError("If 'shp' is in the dict, then it must be a string path to a shapefile.")
                irr1 = gpd.read_file(irr_type_dict['shp'])[[irr_type_dict['column'], 'geometry']]
            elif isinstance(irr_type_dict, dict):
                irr1 = mssql.rd_sql(irr_type_dict['server'], irr_type_dict['database'], irr_type_dict['table'], [irr_type_dict['column']], geo_col=True)
            irr1.rename(columns={irr_type_dict['column']: 'irr_type'}, inplace=True)

            if 'shp' in paw_dict.keys():
                if not isinstance(paw_dict['shp'], str):
                    raise TypeError("If 'shp' is in the dict, then it must be a string path to a shapefile.")
                paw1 = gpd.read_file(paw_dict['shp'])[[paw_dict['column'], 'geometry']]
            elif isinstance(paw_dict, dict):
                paw1 = mssql.rd_sql(paw_dict['server'], paw_dict['database'], paw_dict['table'], [paw_dict['column']], geo_col=True)
            paw1.rename(columns={paw_dict['column']: 'paw'}, inplace=True)

        paw1.loc[:, 'paw'] = paw1.loc[:, 'paw'] * paw_ratio

        setattr(self, 'irr', irr1)
        setattr(self, 'paw', paw1)

        return irr1, paw1


    def input_processing(self, bound_shp, grid_res, buffer_dis, interp_fun, agg_ts_fun, time_agg, precip_et=r'\\fileservices02\ManagedShares\Data\VirtualClimate\vcsn_precip_et_2016-06-06.nc', time_name='time', x_name='longitude', y_name='latitude', rain_name='rain', pet_name='pe', crs=4326, irr_eff_dict={'Drip/micro': 1, 'Unknown': 0.8, 'Gun': 0.8, 'Pivot': 0.8, 'K-line/Long lateral': 0.8, 'Rotorainer': 0.8, 'Solid-set': 0.8, 'Borderdyke': 0.5, 'Linear boom': 0.8, 'Unknown': 0.8, 'Lateral': 0.8, 'Wild flooding': 0.5, 'Side Roll': 0.8}, irr_trig_dict={'Drip/micro': 0.7, 'Unknown': 0.5, 'Gun': 0.5, 'Pivot': 0.5, 'K-line/Long lateral': 0.5, 'Rotorainer': 0.5, 'Solid-set': 0.5, 'Borderdyke': 0.5, 'Linear boom': 0.5, 'Unknown': 0.5, 'Lateral': 0.5, 'Wild flooding': 0.5, 'Side Roll': 0.5}, min_irr_area_ratio=0.01, irr_mons=[10, 11, 12, 1, 2, 3, 4], precip_correction=1.1):
        """
        Function to process the input data for the lsrm. Outputs a DataFrame of the variables for the lsrm.
        """
        np.seterr(invalid='ignore')

        ## Load and resample precip and et
        bound = gpd.read_file(bound_shp)

        ## mins and maxes
        minx, miny, maxx, maxy = bound.geometry.bounds.iloc[0]

        buff_minx = minx - buffer_dis
        buff_miny = miny - buffer_dis
        buff_maxx = maxx + buffer_dis
        buff_maxy = maxy + buffer_dis

        from_crs1 = Proj(CRS.from_user_input(bound.crs))
        to_crs1 = Proj(CRS.from_user_input(crs))
        trans1 = Transformer.from_proj(from_crs1, to_crs1)
        xy_new = np.array(trans1.transform([buff_minx, buff_maxx], [buff_miny, buff_maxy]))
        out_y_min, out_x_min = xy_new.min(1)
        out_y_max, out_x_max = xy_new.max(1)

        ## Precip
        if isinstance(precip_et, str):
            with xr.open_dataset(precip_et) as p:
                precip_et1 = p.load().copy()
        elif isinstance(precip_et, xr.Dataset):
            precip_et1 = precip_et.load().copy()
        else:
            raise TypeError('precip_et must either be a path to a netcdf file or an xarray Dataset')

        # Select data within bounds
#            precip_et2 = precip_et1.where((precip_et1[x_name] > out_x_min) & (precip_et1[x_name] < out_x_max) & (precip_et1[y_name] > out_y_min) & (precip_et1[y_name] < out_y_max), drop=True).load().copy()

        # Agg ts
        precip_et3 = precip_et1.resample(time=time_agg).sum()

        # grid to grid
        p1 = Interp(precip_et3, time_name, x_name, y_name, rain_name, crs)
        new_rain = p1.grid_to_grid(grid_res, 2193, (buff_minx, buff_maxx, buff_miny, buff_maxy), 2) # Need to update to be able to take in bound.crs
        new_rain1 = new_rain.precip.to_series()

        e1 = Interp(precip_et3, time_name, x_name, y_name, pet_name, crs)
        new_et = e1.grid_to_grid(grid_res, 2193, (buff_minx, buff_maxx, buff_miny, buff_maxy), 2) # Need to update to be able to take in bound.crs
        new_et1 = new_et.precip.to_series()
        new_et1.name = 'pet'

        new_rain_et = pd.concat([new_rain1, new_et1], axis=1)

        ## convert new point locations to geopandas
        time1 = new_rain_et.index.levels[0][0]
        grid1 = new_rain_et.loc[time1].reset_index()[['x', 'y']]
        grid2 = vector.xy_to_gpd(grid1.index, 'x', 'y', grid1, bound.crs)
        grid2.columns = ['site', 'geometry']

        all_times = new_rain_et.index.levels[0]
        new_rain_et.loc[:, 'site'] = np.tile(grid1.index, len(all_times))

        ## Convert points to polygons
        sites_poly = vector.points_grid_to_poly(grid2, 'site')

        ## process polygon data
        # Select polgons within boundary

        sites_poly_union = sites_poly.unary_union
        irr2 = self.irr[self.irr.intersects(sites_poly_union)]
        irr3 = irr2[irr2.irr_type.notnull()]
        paw2 = self.paw[self.paw.intersects(sites_poly_union)]
        paw3 = paw2[paw2.paw.notnull()]

        # Overlay intersection
        sites_poly1 = gpd.overlay(sites_poly, bound, how='intersection')[['site', 'geometry']]
        sites_poly2 = sites_poly1.dissolve('site')
        sites_poly2.crs = sites_poly.crs
        sites_poly_area = sites_poly2.area.round(2)
        sites_poly3 = sites_poly2.reset_index()

        irr4 = gpd.overlay(irr3, sites_poly3, how='intersection')
        paw4 = gpd.overlay(paw3, sites_poly3, how='intersection')

        irr4['area'] = irr4.geometry.area.round()
        irr5 = irr4[irr4.area >= 1].copy()

        paw4['area'] = paw4.geometry.area.round()
        paw5 = paw4.loc[(paw4.area >= 1)].copy()
        paw5.loc[paw5.paw <= 0, 'paw'] = 1

        # Add in missing PAW values - Change later to something more useful if needed
        mis_sites_index = ~sites_poly3.site.isin(paw5.site)
        sites_poly3['area'] = sites_poly3.area.round()

        paw6 = pd.concat([paw5, sites_poly3[mis_sites_index]], sort=False)
        paw6.loc[paw6.paw.isnull(), 'paw'] = 1

        # Aggregate by site weighted by area to estimate a volume
        paw_area1 = paw6[['paw', 'site', 'area']].copy()
        paw_area1.loc[:, 'paw_vol'] = paw_area1['paw'] * paw_area1['area']
        paw7 = ((paw_area1.groupby('site')['paw_vol'].sum() / paw_area1.groupby('site')['area'].sum()) * sites_poly_area * 0.001).round(2)

        site_irr_area = irr5.groupby('site')['area'].sum()
        irr_eff1 = irr5.replace({'irr_type': irr_eff_dict})
        irr_eff1.loc[:, 'irr_eff'] = pd.to_numeric(irr_eff1['irr_type']) * irr_eff1['area']
        irr_eff2 = (irr_eff1.groupby('site')['irr_eff'].sum() / site_irr_area).round(3)

        irr_trig1 = irr5.replace({'irr_type': irr_trig_dict})
        irr_trig1.loc[:, 'irr_trig'] = pd.to_numeric(irr_trig1['irr_type']) * irr_trig1['area']
        irr_trig2 = (irr_trig1.groupby('site')['irr_trig'].sum() / site_irr_area).round(3)

        irr_area_ratio1 = (site_irr_area/sites_poly_area).round(3)

        poly_data1 = pd.concat([paw7, sites_poly_area, irr_eff2, irr_trig2, irr_area_ratio1], axis=1)
        poly_data1.columns = ['paw', 'site_area', 'irr_eff', 'irr_trig', 'irr_area_ratio']
        poly_data1.loc[poly_data1['irr_area_ratio'] < min_irr_area_ratio, ['irr_eff', 'irr_trig', 'irr_area_ratio']] = np.nan

        ## Combine time series with polygon data
        new_rain_et1 = new_rain_et[new_rain_et['site'].isin(sites_poly2.index)]

        input1 = pd.merge(new_rain_et1.reset_index(), poly_data1.reset_index(), on='site', how='left')

        ## Convert precip and et to volumes
        input1.loc[:, ['precip', 'pet']] = (input1.loc[:, ['precip', 'pet']].mul(input1.loc[:, 'site_area'], axis=0) * 0.001).round(2)

        ## Remove irrigation parameters during non-irrigation times
        input1.loc[~input1.time.dt.month.isin(irr_mons), ['irr_eff', 'irr_trig']] = np.nan

        ## Run checks on the input data

    #    print('Running checks on the prepared input data')

        null_time = input1.loc[input1.time.isnull(), 'time']
        null_x = input1.loc[input1.x.isnull(), 'x']
        null_y = input1.loc[input1.y.isnull(), 'y']
        null_pet = input1.loc[input1['pet'].isnull(), 'pet']
        null_rain = input1.loc[input1['precip'].isnull(), 'precip']
        null_paw = input1.loc[input1.paw.isnull(), 'paw']
        not_null_irr_eff = input1.loc[input1.irr_eff.notnull(), 'irr_eff']

        if not null_time.empty:
            raise ValueError('Null values in the time variable')
        if not null_x.empty:
            raise ValueError('Null values in the x variable')
        if not null_y.empty:
            raise ValueError('Null values in the y variable')
        if not null_pet.empty:
            raise ValueError('Null values in the pet variable')
        if not null_rain.empty:
            raise ValueError('Null values in the rain variable')
        if not null_paw.empty:
            raise ValueError('Null values in the paw variable')
        if not_null_irr_eff.empty:
            raise ValueError('No values for irrigation variables')

        if input1['time'].dtype.name != 'datetime64[ns]':
            raise ValueError('time variable must be a datetime64[ns] dtype')
        if input1['x'].dtype != float:
            raise ValueError('x variable must be a float dtype')
        if input1['y'].dtype != float:
            raise ValueError('y variable must be a float dtype')
        if input1['pet'].dtype != float:
            raise ValueError('pet variable must be a float dtype')
        if input1['precip'].dtype != float:
            raise ValueError('precip variable must be a float dtype')
        if input1['paw'].dtype != float:
            raise ValueError('paw variable must be a float dtype')
        if input1['irr_eff'].dtype != float:
            raise ValueError('irr_eff variable must be a float dtype')
        if input1['irr_trig'].dtype != float:
            raise ValueError('irr_trig variable must be a float dtype')
        if input1['irr_area_ratio'].dtype != float:
            raise ValueError('irr_area_ratio variable must be a float dtype')

        ## Return dict
        setattr(self, 'model_var', input1)
        setattr(self, 'sites_poly', sites_poly2)

        return input1, sites_poly2


    def lsrm(self, A=6, include_irr=True):
        """
        The lsrm.
        """
        np.seterr(invalid='ignore')

        ## Make initial variables
        all_times = self.model_var['time'].unique()
        sites = self.model_var['site'].unique()

        ## Prepare individual variables
        # Input variables
        paw_val = self.model_var['paw'].values
        irr_area_ratio_val = self.model_var['irr_area_ratio'].copy()
        irr_area_ratio_val[irr_area_ratio_val.isnull()] = 0

        irr_paw_val = paw_val * irr_area_ratio_val.values
        non_irr_paw_val = paw_val - irr_paw_val
        irr_paw_val[irr_paw_val <= 0 ] = np.nan
        non_irr_paw_val[non_irr_paw_val <= 0 ] = np.nan

        irr_rain_val = self.model_var['precip'].values * irr_area_ratio_val.values
        non_irr_rain_val = self.model_var['precip'].values - irr_rain_val

        irr_pet_val = self.model_var['pet'].values * irr_area_ratio_val.values
        non_irr_pet_val = self.model_var['pet'].values - irr_pet_val

        irr_eff_val = self.model_var['irr_eff'].values
        irr_trig_val = self.model_var['irr_trig'].values

        time_index = np.arange(len(self.model_var)).reshape(len(all_times), len(sites))

        # Initial conditions
        w_irr = irr_paw_val[time_index[0]].copy()
        w_non_irr = non_irr_paw_val[time_index[0]].copy()

        # Output variables
        out_w_irr = np.full(len(irr_eff_val), np.nan)
        out_irr_demand = out_w_irr.copy()
        out_w_non_irr = out_w_irr.copy()
        out_irr_aet = out_w_irr.copy()
        out_non_irr_aet = out_w_irr.copy()

        out_irr_drainage = out_w_irr.copy()
        out_non_irr_drainage = out_w_irr.copy()

        ## Run the model
        for i in time_index:

            if include_irr:
                ### Irrigation bucket
                i_irr_paw = irr_paw_val[i]

                ## Calc AET and perform the initial water balance
                irr_aet_val = ds_AET(irr_pet_val[i], A, w_irr, i_irr_paw)
                out_irr_aet[i] = irr_aet_val.copy()
                w_irr = w_irr + irr_rain_val[i] - irr_aet_val

                ## Check and calc the GW drainage from excessive precip
                irr_drainge_bool = w_irr > i_irr_paw
                if any(irr_drainge_bool):
                    temp_irr_draiange = w_irr[irr_drainge_bool] - i_irr_paw[irr_drainge_bool]
                    out_irr_drainage[i[irr_drainge_bool]] = temp_irr_draiange
                    w_irr[irr_drainge_bool] = i_irr_paw[irr_drainge_bool]
                out_w_irr[i] = w_irr.copy()

                ## Check and calc drainage from irrigation if w is below trigger
                irr_paw_ratio = w_irr/i_irr_paw
                irr_trig_bool = irr_paw_ratio <= irr_trig_val[i]
                if any(irr_trig_bool):
                    diff_paw = i_irr_paw[irr_trig_bool] - w_irr[irr_trig_bool]
                    out_irr_demand[i[irr_trig_bool]] = diff_paw.copy()
                    irr_drainage = diff_paw/irr_eff_val[i][irr_trig_bool] - diff_paw
                    out_irr_drainage[i[irr_trig_bool]] = irr_drainage.copy()
                    w_irr[irr_trig_bool] = i_irr_paw[irr_trig_bool].copy()

                out_w_irr[i] = w_irr.copy()

            ### Non-irrigation bucket
            i_non_irr_paw = non_irr_paw_val[i]

            ## Calc AET and perform the initial water balance
            non_irr_aet_val = ds_AET(non_irr_pet_val[i], A, w_non_irr, i_non_irr_paw)
            out_non_irr_aet[i] = non_irr_aet_val.copy()
            w_non_irr = w_non_irr + non_irr_rain_val[i] - non_irr_aet_val
            w_non_irr[w_non_irr < 0] = 0

            ## Check and calc the GW drainage from excessive precip
            non_irr_drainge_bool = w_non_irr > i_non_irr_paw
            if any(non_irr_drainge_bool):
                temp_non_irr_draiange = w_non_irr[non_irr_drainge_bool] - i_non_irr_paw[non_irr_drainge_bool]
                out_non_irr_drainage[i[non_irr_drainge_bool]] = temp_non_irr_draiange.copy()
                w_non_irr[non_irr_drainge_bool] = i_non_irr_paw[non_irr_drainge_bool]
            out_w_non_irr[i] = w_non_irr.copy()

        ### Put results into dataframe

        output1 = self.model_var.copy()
        output1.loc[:, 'non_irr_aet'] = out_non_irr_aet.round(2)
        if include_irr:
            output1.loc[:, 'irr_aet'] = out_irr_aet.round(2)
            output1.loc[:, 'irr_paw'] = irr_paw_val.round(2)
            output1.loc[:, 'w_irr'] = out_w_irr.round(2)
            output1.loc[:, 'irr_drainage'] = out_irr_drainage.round(2)
            output1.loc[:, 'irr_demand'] = out_irr_demand.round(2)
        else:
            output1.drop(['irr_eff', 'irr_trig', 'irr_area_ratio'], axis=1, inplace=True)
        output1.loc[:, 'non_irr_paw'] = non_irr_paw_val.round(2)
        output1.loc[:, 'w_non_irr'] = out_w_non_irr.round(2)
        output1.loc[:, 'non_irr_drainage'] = out_non_irr_drainage.round(2)

        ### Return output dataframe
        setattr(self, 'results', output1)

        return output1



