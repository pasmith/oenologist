# data structures and data handling
import pandas as pd
import numpy as np

# data loading
import os
import kagglehub

# data manipulation
import re
from functools import reduce


# helper to extract year from review title
TITLE_PATTERN = re.compile(r'\D(19[0-9]{2}|20[0-9]{2})')


# definition of ratings
RATINGS = [('acceptable',range(80, 83)), ('good',range(83, 87)), ('very good',range(87, 90)), ('excellent',range(90, 94)), ('superb',range(94, 98)), ('classic',range(98, 101))]


# defaut cutoffs
DEFAULT_CUTOFFS = [('year', 1000), ('variety', 500), ('country', 1000)]


def vintage(title):
  m = TITLE_PATTERN.findall(title)
  if len(m) > 0:
    m = TITLE_PATTERN.findall(title)
    m.sort()
    return int(m[-1])
  return None


def mask_reviews(df, cutoffs: list[tuple[str,int]] = DEFAULT_CUTOFFS) -> pd.DataFrame:
  if cutoffs is None:
    return df
  # define the masks for the specificed cutoff thresholds  
  masks = [df[col].isin(df[col].value_counts().to_frame().query(f'count > {threshold}').index) for col, threshold in cutoffs]
  # filter the dataframe keeping only the elements that match the mask
  return df[reduce(lambda r, m: r&m, masks, np.array([True]*df.shape[0]))].copy(deep=True)


def clean(df: pd.DataFrame, cutoffs: list[tuple[str,int]] = DEFAULT_CUTOFFS) -> pd.DataFrame:
  clean = df.copy(deep=True)
  
  # extract year from title
  clean['year'] = clean.title.apply(vintage)

  # extract review length
  clean['review_len'] = clean.description.str.len()

  # add rating
  clean['rating'] = clean.points.map({points: rating for rating, point_range in RATINGS for points in point_range})

  # drop columns that are not needed
  clean.drop(['price', 'taster_twitter_handle', 'province', 'region_1', 'region_2', 'designation', 'title', 'winery'], axis=1, inplace=True)

  # Impute missing tasters to 'Unknown'
  clean.loc[clean.taster_name.isna(), 'taster_name'] = 'Unknown'

  # drop rows with missing data that would be difficult to impute sensibly
  mask = clean.year.notna()
  mask &= clean.variety.notna()
  mask &= clean.country.notna()

  clean = clean[mask].copy(deep=True)
  clean.year = clean.year.astype(int)

  # drop duplicate descriptions
  clean.drop_duplicates('description', keep='first', inplace=True)

  return clean if cutoffs is None else mask_reviews(clean)


def load_data(dirname: str = '.', fname: str ='wine_reviews-clean.parquet.gzip', cutoffs: list[tuple[str,int]]=DEFAULT_CUTOFFS) -> pd.DataFrame:
  data_path = os.path.join(dirname, fname)

  if os.path.exists(data_path):
    df = pd.read_parquet(data_path)
  else:
    kaggle_path = kagglehub.dataset_download("christopheiv/winemagdata130k")
    kaggle_fname = 'winemag-data-130k-v2.csv'
    reviews = pd.read_csv(os.path.join(kaggle_path, kaggle_fname), index_col=0)
    df = clean(reviews, cutoffs)
    df.to_parquet(data_path, compression='gzip')
  
  return df



