# -*- coding: utf-8 -*-
"""

"""
import os
import pandas as pd
from pdsql import mssql
import yaml
from hydrointerp import Interp

pd.options.display.max_columns = 10
pd.options.display.max_rows = 20
run_time_start = pd.Timestamp.today()

###########################################
#### Parameters

base_dir = os.path.realpath(os.path.dirname(__file__))

with open(os.path.join(base_dir, 'parameters.yml')) as param:
    param = yaml.safe_load(param)

to_date = run_time_start.floor('H')
from_date = (to_date - pd.DateOffset(days=7)).round('D')

#########################################
### util Functions


def grp_ts_agg(df, grp_col, ts_col, freq_code, discrete=False, **kwargs):
    """
    Simple function to aggregate time series with dataframes with a single column of sites and a column of times.

    Parameters
    ----------
    df : DataFrame
        Dataframe with a datetime column.
    grp_col : str or list of str
        Column name that contains the sites.
    ts_col : str
        The column name of the datetime column.
    freq_code : str
        The pandas frequency code for the aggregation (e.g. 'M', 'A-JUN').
    discrete : bool
        Is the data discrete? Will use proper resampling using linear interpolation.

    Returns
    -------
    Pandas resample object
    """

    df1 = df.copy()
    if type(df[ts_col].iloc[0]) is pd.Timestamp:
        df1.set_index(ts_col, inplace=True)
        if isinstance(grp_col, str):
            grp_col = [grp_col]
        else:
            grp_col = grp_col[:]
        if discrete:
            val_cols = [c for c in df1.columns if c not in grp_col]
            df1[val_cols] = (df1[val_cols] + df1[val_cols].shift(-1))/2
        grp_col.extend([pd.Grouper(freq=freq_code, **kwargs)])
        df_grp = df1.groupby(grp_col)
        return (df_grp)
    else:
        print('Make one column a timeseries!')


###########################################
### Main function


def calcmin(min_values=5, quantile=0.2, month=5, start_year='2001', where_in=None):
    """
    Function to calculate the specified groundwater level quantile for a specific month and interpolate those values across all other available wells.

    Parameters
    ----------
    min_values : int
        The minimum number of water levels to calculate the quantile. If you use two or less, this function will produce an electric shock to your brain!
    where_in : dict or None
        A dict filter for the ExternalSites table in the Hydro db.
    quantile : float
        The specified quantile.
    month : int
        The month to select the data from.
    start_year : str
        The year the data will start from.

    Returns
    -------
    DataFrame
    """
    ## Check for stupidity
    if min_values < 3:
        raise ValueError('Zap!!!')

    ## Get sites and summary data
    sites1 = mssql.rd_sql(param['input']['ts_server'], param['input']['ts_database'], param['input']['sites_table'], ['ExtSiteID', 'NZTMX', 'NZTMY', 'Altitude', 'CatchmentName', 'CatchmentGroupName', 'SwazName', 'SwazGroupName', 'GwazName', 'CwmsName'], where_in=where_in)
    sites2 = sites1[sites1.ExtSiteID.str.contains('[A-Z]+\d+/\d+')]

    summ1 = mssql.rd_sql(param['input']['ts_server'], param['input']['ts_database'], param['input']['ts_summ_table'], ['ExtSiteID', 'Min', 'Median', 'Mean', 'Max', 'Count', 'FromDate', 'ToDate'], where_in={'DatasetTypeID': [param['input']['ts_dataset']]})
    summ2 = summ1[summ1.Count >= min_values].copy()

    sites3 = sites2[sites2.ExtSiteID.isin(summ2.ExtSiteID)].copy()

    ## Get TS data
    tsdata1 = mssql.rd_sql(param['input']['ts_server'], param['input']['ts_database'], param['input']['ts_table'], ['ExtSiteID', 'DateTime', 'Value'], where_in={'ExtSiteID': sites3.ExtSiteID.tolist(), 'DatasetTypeID': [param['input']['ts_dataset']], 'QualityCode': param['input']['ts_quality_codes']}, from_date=start_year, date_col='DateTime')
    tsdata1.DateTime = pd.to_datetime(tsdata1.DateTime)

    ## Interpolate and extract
    agg1 = grp_ts_agg(tsdata1.dropna(), 'ExtSiteID', 'DateTime', 'D', True).Value.mean().dropna().unstack(0)
    agg2 = agg1.resample('D').mean()
    agg3 = agg2.dropna(how='all', axis=1)
    agg4 = agg3.interpolate('time', limit=40, limit_area='inside')
    ts1 = agg4.stack()
    ts1.name = 'Value'
    ts1 = ts1.reset_index()
    ts1['month'] = ts1.DateTime.dt.month
    ts1['day'] = ts1.DateTime.dt.day
    ts2 = ts1[(ts1.day == 15) & (ts1.month == month)].drop(['month', 'day'], axis=1).copy()

    # Summarise
    tsmon1 = ts2.groupby('ExtSiteID').Value.count()
    good_sites = tsmon1[tsmon1 >= min_values]
    tsdata3 = ts2.loc[ts2.ExtSiteID.isin(good_sites.index)]

    ## Calc percentiles
    quant1 = tsdata3.groupby('ExtSiteID')['Value'].quantile(quantile)
    quant1.name = 'GwlQuantile'

    ## Get additional well attributes
    attr1 = mssql.rd_sql(param['input']['ts_server'], param['input']['ts_database'], param['input']['site_feature_table'], ['ExtSiteID', 'Value'], where_in={'Parameter': ['WellDepth']})
    attr1['Value'] = pd.to_numeric(attr1.Value, errors='coerce')
    attr1.rename(columns={'Value': 'WellDepth'}, inplace=True)

    ## Categorise well depths
    attr1['DepthCat'] = pd.cut(attr1.WellDepth, bins=param['input']['well_depth_bins'], labels=[0, 15, 50, 100])
    attr1.dropna(inplace=True)

    ## Interpolate wells
    sites_xy = sites2[['ExtSiteID', 'NZTMX', 'NZTMY', 'Altitude']].dropna().copy()
    sites_xy.rename(columns={'NZTMX': 'x', 'NZTMY': 'y'}, inplace=True)
    sites_xy = pd.merge(sites_xy, attr1, on='ExtSiteID')
    quant4 = pd.merge(sites_xy, quant1, on='ExtSiteID')
    quant4['GwlQuantile'] = quant4['GwlQuantile'] + quant4['Altitude']
    sites_other = sites_xy[~sites_xy.ExtSiteID.isin(quant4.ExtSiteID.unique())].copy()

    quant5 = quant4.replace({'DepthCat': {0: '2000-01-01', 15: '2000-01-02', 50: '2000-01-03', 100: '2000-01-04'}})
    quant5 = quant5.groupby(['x', 'y', 'DepthCat'])['GwlQuantile'].mean().reset_index()
    interp1 = Interp(point_data=quant5, point_time_name='DepthCat', point_x_name='x', point_y_name='y', point_data_name='GwlQuantile', point_crs=2193)
    q_interp1 = interp1.points_to_points(sites_other.drop_duplicates(['x', 'y']), to_crs=2193)

    q_interp2 = q_interp1.reset_index()
    q_interp2['time'] = q_interp2['time'].astype(str)
    q_interp2.replace({'time': {'2000-01-01': 0, '2000-01-02': 15, '2000-01-03': 50, '2000-01-04': 100}}, inplace=True)
    q_interp2.rename(columns={'time': 'DepthCat', 'precip': 'GwlQuantile'}, inplace=True)

    q_other1 = pd.merge(sites_other, q_interp2, on=['x', 'y', 'DepthCat'])
    q_other1['Estimated'] = True

    ## Combine
    quant4['Estimated'] = False
    q_all1 = pd.concat([quant4, q_other1], sort=True)

    return q_all1







