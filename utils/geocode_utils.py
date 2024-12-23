import os
import pandas as pd
import kagglehub
from joblib import Memory
import requests

# configure cache
cachedir = '.cache'
memory = Memory(cachedir, verbose=0)


@memory.cache
def get_country_code_lookup():
  # manual overrides to address data quality issues
  overrides = {
    'US': 'US',
    'England': 'GB',
    'Moldova': 'MD',
    'Czech Republic': 'CZ',
    'Macedonia': 'MK',
    'nan': None,
  }
  # Download the country code dataset
  fname = 'wikipedia-iso-country-codes.csv'
  path = kagglehub.dataset_download("juanumusic/countries-iso-codes")
  countries = pd.read_csv(os.path.join(path, fname)) \
                .rename(columns={'English short name lower case': 'country', 'Alpha-2 code': 'code'})[['country','code']]
  return dict(overrides, **countries.set_index('country').to_dict()['code'])

def ping(url):
    res = requests.get(url)
    return res.status_code == 200