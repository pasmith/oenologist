# libraries
import numpy as np
import pandas as pd
from functools import cache
from cachetools import cached, LRUCache

# import geopandas as gpd
import os
import json
from collections import namedtuple

def __load_wineries():
  # helper to extract region and country information from raw dataset
  def extract_region(k: str) -> tuple[str]:
    parts = k.split(', ')
    if len(parts) == 2:
      return parts
    elif len(parts) == 3:
      return {parts[0], parts[2]}
    elif len(parts) < 2:
      if parts[0] == 'Unknown':
        return [None] * 2
      print(len(parts), parts)    
      return [parts[0], None]
    else:
      print(len(parts), parts)
      return [parts[0], parts[1]]

  # data model
  vineyard_cols = ['name', 'lat', 'lon', 'region', 'country', 'color', 'url']
  Vineyard = namedtuple('Vineyard', vineyard_cols, defaults = [None]*len(vineyard_cols))

  # Open and read the JSON file
  with open(os.path.join('../winerymap', 'vineyards.json'), 'r') as file:
    data = json.load(file)
    file.close()

  # Print the data
  return pd.DataFrame(
      [
        Vineyard(vineyard[2], vineyard[0], vineyard[1], *extract_region(key), data[key]['color'], vineyard[3])
        for key in data
        for vineyard in data[key]['vineyards']
    ]
  )

wineries = __load_wineries()

def __create_indexes(df = wineries):
  # group by helper
  by_ = lambda cols, df=wineries: df.groupby(cols).count()[['lat']].rename(columns={'lat':'count'}).sort_values('count', ascending=False)


  # index of wineries witn only one location
  by_name = by_('name')
  known_wineries = np.unique(by_name.index)
  single_site_wineries = np.unique(by_name.query('count == 1').index)

  # index of wineries witn only one location per country
  by_country = by_(['name', 'country'], df=wineries[~wineries.name.isin(single_site_wineries)])
  single_site_by_country_wineries = np.unique(by_country.query('count == 1').index)

  # index of wineries witn only one location per region
  by_region = by_(
    ['name', 'country', 'region'],
    df=wineries[
      (~wineries.name.isin(single_site_wineries))
      &(~wineries.set_index(['name', 'country']).index.isin(single_site_by_country_wineries))
    ]
  )
  single_site_by_region_wineries = np.unique(by_region.query('count == 1').index)

  # index of wineries witn multiple locations per region
  multisite_wineries = by_(
    ['name', 'country', 'region'],
    df=wineries[
      (~wineries.name.isin(single_site_wineries))
      &(~wineries.name.isin(single_site_by_country_wineries))
      &(~wineries.set_index(['name', 'country']).index.isin(single_site_by_country_wineries))
      &(~wineries.set_index(['name', 'country', 'region']).index.isin(single_site_by_region_wineries))
    ]
  )
  multisite_wineries = np.unique(multisite_wineries.index)

  return known_wineries, single_site_wineries, single_site_by_country_wineries, single_site_by_region_wineries, multisite_wineries

__known_wineries, __single_site_wineries, __single_site_by_country_wineries, __single_site_by_region_wineries, __multisite_wineries = __create_indexes()

__review_location_cols = ['winery', 'country', 'province', 'region_1', 'region_2']
__geocode_cols = ['lat', 'lon', 'region', 'country', 'url']

UNKNOWN_WINERY = namedtuple('UNKNOWN_WINERY', __review_location_cols, defaults=[None]*len(__review_location_cols))
RESOLVED_WINERY = namedtuple('RESOLVED_WINERY', __geocode_cols, defaults=[None]*len(__geocode_cols))

__to_resolved_winery = lambda result: RESOLVED_WINERY(*next(result.itertuples(index=False)))

@cached({}, info=True)
def __calculate(query: str):
  print('calculating', query)
  return __to_resolved_winery(wineries.query(query)[__geocode_cols].groupby(['region', 'country', 'url']).mean().reset_index()[__geocode_cols])


@cached({}, info=True)
def __lookup(query: str):
  return __to_resolved_winery(wineries.query(query)[__geocode_cols])

def geocode(row):
  
  # fail fast for unrecognized winery names
  if not row.winery in __known_wineries:
    return RESOLVED_WINERY() # UNKNOWN_WINERY(row.winery, row.country, row.province, row.region_1, row.region_2)
  
  query_terms = [
    f'name == "{row.winery}"',
    f'country == "{row.country}"',
    f'region == "{row.province}"',
  ]

  q = None
  if row.winery in __single_site_wineries:
    q = query_terms[:1]
  elif (row.winery, row.country) in map(lambda k: tuple(k), __single_site_by_country_wineries):
    q = query_terms[:2]
  elif (row.winery, row.country, row.province) in map(lambda k: tuple(k), __single_site_by_region_wineries):
    q = query_terms[:3]
  elif (row.winery, row.country, row.province) in map(lambda k: tuple(k), __multisite_wineries):
    # TODO take centroid of lat-lon points
    # print('multisite winery', query_terms[:3])
    q = query_terms[:3]
    return __calculate(' and '.join(q))
  
  if q is None:
    # print('***', row)
    return RESOLVED_WINERY()

  return __lookup(' and '.join(q))

