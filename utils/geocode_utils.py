import os
import pandas as pd
import numpy as np
import kagglehub
from joblib import Memory
import requests
from collections import namedtuple
from pyproj import Transformer
from shapely.ops import transform
import quackosm as qosm
from ratelimit import limits, sleep_and_retry
from cachetools import cached
import swifter

# configure cache
cachedir = ".cache"
memory = Memory(cachedir, verbose=0)

@memory.cache
def load_country_code_lookup():
    # manual overrides to address data quality issues
    overrides = {
        "US": "US",
        "England": "GB",
        "Moldova": "MD",
        "Czech Republic": "CZ",
        "Macedonia": "MK",
        "nan": None,
    }
    # Download the country code dataset
    fname = "wikipedia-iso-country-codes.csv"
    path = kagglehub.dataset_download("juanumusic/countries-iso-codes")
    countries = pd.read_csv(os.path.join(path, fname)).rename(
        columns={"English short name lower case": "country", "Alpha-2 code": "code"}
    )[["country", "code"]]
    return dict(overrides, **countries.set_index("country").to_dict()["code"])

codes = load_country_code_lookup()

def get_country_code(name: str) -> str:
  code_for = lambda n: codes[n] if n in codes else None
  if "United States" in name:
    code = code_for("US")
  elif "Congo" in name:
    code = code_for("Democratic Republic of the Congo")
  elif "Bahamas" in name:
    code = code_for("Bahamas")
  elif "Timor" in name:
    code = code_for("Timor-Leste")
  elif "Tanzania" in name:
    code = code_for("Tanzania, the United Republic of")
  code = code_for(name)
  if code is None:
    print('no code found for', name)
    return None
  elif type(code) != str:
    print(type(name), name, type(code), code)
    return None
  return code.lower()

def ping(url):
    res = requests.get(url)
    return res.status_code == 200


LOCATION = namedtuple('LOCATION', ['lat', 'lon', 'address'], defaults = [None]*3)


# configure coordinate system transformer - from lat lon to m
__transformer = Transformer.from_crs(4326, 3857, always_xy=False)

# helper to calcualte area in m2 of geometric boundary
__calculate_area = lambda geo: transform(func=__transformer.transform, geom=geo).area

__notna = lambda v: v is not None

__not_found = []

# throttled variant of fast operation
@sleep_and_retry
@limits(calls=1, period=1)  
def __fetch_gemoetry(area: str):
  return qosm.geocode_to_geometry(area)

@memory.cache
def get_area(area: str):
  try:
    return __fetch_gemoetry(area)
  except:
    __not_found.append(area)
    return None

def __determine_search_boundary(row):
  country, province, region_1, region_2 = row.replace(np.nan, None).to_list()[1:]

  boundaries = []
  areas = []

  def get_geometry(loc: str):
    shape = get_area(loc)
    if shape is not None:
      try:
        areas.append(__calculate_area(shape))
        boundaries.append(shape)
      except:
        __not_found.append(loc)

  if __notna(country):
    get_geometry(country)

#   if __notna(province):
#     get_geometry(province)

#   if __notna(region_1):
#     get_geometry(region_1)

#   if __notna(region_1):
#     get_geometry(region_2)

  return boundaries[areas.index(min(areas))]


@memory.cache
def calculate_search_boundaries(df):
  return df.swifter.apply(__determine_search_boundary, axis=1)

