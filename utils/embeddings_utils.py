import os
import pandas as pd

from sentence_transformers import SentenceTransformer
from utils.wine_review_utils import load_augmented_data
from utils.timer_utils import timeit


# compute the embeddings for the reviews
def compute_embeddings(corpus, model_name='all-MiniLM-L6-v2', trust_remote_code=False):
  """
  Compute the embeddings for the wine reviews using a pretrained sentence transformer model.
  :param corpus: The corpus of wine reviews
  :param model_name: The name of the pretrained model to use
  :param trust_remote_code: Whether to trust remote code
  :return: The embeddings as a numpy array
  """
  # timing helper
  __t = lambda purpose, func: timeit(model_name, purpose, func, len(corpus), 'reviews')

  # calculate embeddings using a pretrained sentence transformer model
  model = SentenceTransformer(model_name, trust_remote_code=trust_remote_code)
  return __t('compute embeddings', lambda: model.encode(corpus, normalize_embeddings=True, show_progress_bar=True, device='mps'))


# load the wine reviews dataset embeddings for the given model
def load_embeddings(dirname='data', model='all-MiniLM-L6-v2', filename='embeddings.parquet.gzip'):
  """
  Load the wine reviews dataset with embeddings.
  :param dirname: The directory where the dataset is stored
  :param model: The pretrained model to use to compute the embeddings
  :param filename: The name of the dataset file
  :return: The data as a pandas dataframe
  """ 
  datapath = os.path.join(dirname, f'{model}_{filename}')
  if os.path.exists(datapath):
    return pd.read_parquet(datapath)
  else:
    # load the augmented data
    reviews = load_augmented_data(dirname)
    # calculate the embeddings
    embeddings = pd.DataFrame(compute_embeddings(reviews.description.to_list(), model_name=model), index=reviews.index)
    # save the merged dataframe to a parquet file
    embeddings.to_parquet(datapath, compression='gzip')
    return embeddings