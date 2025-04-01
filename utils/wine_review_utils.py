# data structures and data handling
import pandas as pd

# data loading
import os
import kagglehub

# data manipulation
import re


#
# Constants
#

# helper to extract year from review title
TITLE_PATTERN = re.compile(r'\D(19[0-9]{2}|20[0-9]{2})')

# definition of ratings
RATINGS = [('acceptable',range(80, 83)), ('good',range(83, 87)), ('very good',range(87, 90)), ('excellent',range(90, 94)), ('superb',range(94, 98)), ('classic',range(98, 101))]

# defaut cutoffs
DEFAULT_CUTOFFS = {'year': 2003, 'variety': 50, 'country': 200}

# Data Columns
FEATURES = ['winery', 'variety', 'year', 'country', 'price', 'taster_name', 'description', 'points']



#
# Helper functions
#

# Download the dataset if not already downloaded
def load_original_data(dirname='data', filename='reviews.parquet.gzip'):
  """
  Load the original wine reviews dataset.
  :param dirname: The directory where the dataset is stored
  :param filename: The name of the dataset file
  :return: The original data as a pandas dataframe
  """
  datapath = os.path.join(dirname, filename)
  if os.path.exists(datapath):
    return pd.read_parquet(datapath)
  else:
    os.makedirs(dirname, exist_ok=True)
    path = kagglehub.dataset_download("christopheiv/winemagdata130k")
    fname = 'winemag-data-130k-v2.csv'
    reviews = pd.read_csv(os.path.join(path, fname), index_col=0)
    reviews.to_parquet(datapath, compression='gzip')
    return reviews


# helper function to extract the vintage from the title
def vintage(title):
  """
  Extract the vintage from the title of the wine review.
  :param title: The title of the wine review
  :return: The vintage as an integer, or None if not found
  """
  m = TITLE_PATTERN.findall(title)
  if len(m) > 0:
    m.sort()
    return int(m[-1])
  return None


# data cleaning helper
def clean(original: pd.DataFrame, cutoffs: list[tuple[str,int]] = DEFAULT_CUTOFFS) -> pd.DataFrame:
  """
  Clean the wine reviews dataset.
  :param df: The original dataframe
  :param cutoffs: A list of tuples containing the column name and the cutoff value
  :return: The cleaned dataframe
  """
  df = original.copy(deep=True)
  
  # extract the year from the title
  df['year'] = df.title.apply(lambda x: TITLE_PATTERN.findall(x)[-1] if TITLE_PATTERN.findall(x) else None)
  df.dropna(subset=['year'], inplace=True)
  df.year = df.year.astype(int)
  # only keep reviews from 2004 and later
  cutoff = cutoffs.get('year', 2003)
  df = df.query('year > @cutoff').copy(deep=True)

  # drop duplicate descriptions
  df.drop_duplicates(subset=['description'], keep='last', inplace=True)

  # determine the countries with more than 200 reviews
  min_reviews = cutoffs.get('country', 200)
  top_countries = df.country.value_counts().reset_index().query('count > @min_reviews').set_index('country').index
  # determine the top 50 varieties with the most reviews
  top_n_varieties = cutoffs.get('variety', 50)
  varieties_with_many_reviews = df.variety.value_counts().head(top_n_varieties)

  # filter the dataframe to keep only the top countries and varieties
  mask = df.country.isin(top_countries)
  mask &= df.variety.isin(varieties_with_many_reviews.head(top_n_varieties).index)

  df = df[mask][FEATURES].copy(deep=True)

  # set the taster name to 'Unknown' if it is missing
  df.loc[df.taster_name.isna(), 'taster_name'] = 'Unknown'

  return df[mask][FEATURES].copy(deep=True)


# Clean the data if not already cleaned
def load_clean_data(dirname='data', filename='reviews-cleaned.parquet.gzip'):
  """
  Load the cleaned wine reviews dataset.
  :param dirname: The directory where the cleaned dataset is stored
  :param filename: The name of the cleaned dataset file
  :return: The cleaned data as a pandas dataframe
  """
  datapath = os.path.join(dirname, filename)
  if os.path.exists(datapath):
    return pd.read_parquet(datapath)
  else:
    reviews = load_original_data(dirname)
    cleaned = clean(reviews)
    cleaned.to_parquet(datapath, compression='gzip')
    return cleaned


# augment the review dataset with description length and rating columns
def load_augmented_data(dirname='data', filename='reviews-augmented.parquet.gzip'):
  """
  Load the augmented wine reviews dataset.
  :param dirname: The directory where the augmented dataset is stored
  :param filename: The name of the augmented dataset file
  :return: The augmented data as a pandas dataframe
  """
  datapath = os.path.join(dirname, filename)
  if os.path.exists(datapath):
    return pd.read_parquet(datapath)
  else:
    # define a mapping for wine ratings
    ratings_map = {points: rating for rating, points_range in RATINGS for points in points_range}
    # load the cleaned data
    reviews = load_clean_data(dirname)
    # add a new column for the rating
    reviews['rating'] = reviews.points.map(ratings_map)
    # add a new column for the length of the description
    reviews['description_length'] = reviews.description.str.len()
    # save the augmented data to a parquet file
    reviews.to_parquet(datapath, compression='gzip')
    return reviews
