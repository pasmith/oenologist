import re
import nltk
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize


# We need to download stopwords first
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# List of stopwords
nl_stopwords = stopwords.words('english')
nl_stopwords = set(nl_stopwords)

# Add custom words
nl_stopwords.update(["drink", "now", "wine", "flavor",
                     'flavors', 'finish', 'palate', 'show',
                     'nose', 'note', 'taste', 'notes',
                     'also', 'still', 'yet',
                     'feels', 'feel', 'give', 'gives', 'shows',
                     'come', 'comes', 'need', 'needs',
                     'seems', 'seem', 'ro'
                     'one', 'two'])


# Define a function to remove numbers and punctuations
def remove_num_punc(words):
  '''
  Remove all numbers and punctuations from given words
  '''
  # remove all numbers and punctuations
  pattern = r"('(?:\w+))|\\r\\n|\\n|\\r|[^a-zA-Z]"
  clean_words = re.sub(pattern,' ',str(words), flags=re.S)

  # turn words into lower case and split them into array
  words_arr = clean_words.lower().split()

  # join words with white space between each words
  join_words = ' '.join(words_arr)

  return join_words


def remove_stop_words(words, stop_words=nl_stopwords):
  '''
  Remove stop words from words
  Pre-set stopwords included words related to wine
  '''
  # Split string into words
  word_arr = words.split()

  # Ignore words in stop words list
  filter_words = [word for word in word_arr if word not in stop_words]
  join_words = ' '.join(filter_words)

  return join_words



def get_wordnet_pos(treebank_tag):
  '''
  Treebank tag
  https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
  '''
  if treebank_tag.startswith('J'):
        return wordnet.ADJ
  elif treebank_tag.startswith('V'):
      return wordnet.VERB
  elif treebank_tag.startswith('N'):
      return wordnet.NOUN
  elif treebank_tag.startswith('R'):
      return wordnet.ADV
  elif treebank_tag.startswith('VBZ'):
      return wordnet.ADJ_SAT
  else:
      return ''

def lemmatize_words(words):
  '''
  Lemmatize words

  Return a lemmatized words
  '''
  # tokenize words
  tokenized_words = word_tokenize(words, language='english')

  # lemmatize words
  lemmatizer = WordNetLemmatizer()
  lemmatized_words = []

  # for word in tokenized_words:
  #   lemmatized_words.append(lemmatizer.lemmatize(word))

  # Pos
  for word, tag in pos_tag(tokenized_words):
    pos = get_wordnet_pos(tag)
    if pos == '':
      lemmatized_words.append(word)
    else:
      lemmatized_words.append(lemmatizer.lemmatize(word, pos=pos))

  # join words together
  final_sentence = ' '.join(lemmatized_words)
  return final_sentence