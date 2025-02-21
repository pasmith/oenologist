### Oenologist

**Patrick Smith**

#### Executive summary
```Oenologists evaluate the quality of wine and ensure it meets the desired outcome.```

This project aims to use data science, specifically machine learning, to assess whether wines achieve desired outcomes based on qualitative wine reviews obtained experienced wine industry tasters. Desirable traits differ based on the types of wines. For example, certain wines are considered higher quality if they are dry, acidic, and aged in barrels, which imparts flavor and texture characteristics wine reviewers may note in their descriptions. Other wines are expected less dry and more fruity. This infographic describes what flavors and characteristics are expressed by different types of wine.

**Wine Classifying Wines**

Since each wine should have been expertly described by someone trained in the art of wine tasting, I thought I could use the data to:

- Classify wines based on description
- Recreate the proper red-white groupings from descriptors

<img src="images/Different-Types-of-Wine-v2.jpg" alt="pinot noir" width="500"/>

This project trains classification algorithms on roughly 130k descriptions of wines reviewed by [WineEnthusiast](https://www.wineenthusiast.com/) between May and November 2017. Natural language processing is used to extract features from the descriptions and train the algorithm to predict the quality of the wine given the description, type of wine, and other data about the winemaker.

Once successfully trained, this algorithm would be able to predict whether a wine is considered high quality, or has achieved the outcome expected for that wine, based on the descriptions obtained from industry tasters.

#### Rationale
The global wine market is expected to be nearly a $350 billion industry in 2025. Gross margins for vineyards and wineries are on average 50%, while wine retailers and restaurants have profit margins of nearly 30% and 70% respectively. Factors that affect these profit margins include production volume, location, size of the winery, and market positioning. Wine reviews and quality assessments impact the reputation of the wine in the market, and in term impact how the wine is positioned in the market.

- Vineyards and wineries can use predictions of the quality of their wines to influence their go-to-market strategies.

- Retailers and restaurants can make educated purchasing decisions to fine tune their inventories and maximize their profit margins.

- The general wine loving public is always interested in finding great quality wines from lesser known wine producers. A qualitative review of such wines can help such buyers discover wines they might enjoy despite not knowing the producer.

#### Research Question
The main research question investigated here is assessing the quality of a wine by the type of wine it is, given the review description it received. The basic premise is that wines are expected to exhibit certain traits. The reviews should describe the traits of the wine. By using natural language processing, we expect to be able to extract these descriptions as features and train a model to predict the quality of a wine based on those features.

We also expect to predict the corresponding price of the wine to help producers, retailers, and restaurants estimate what the public would be willing to pay for the wine given the review it has received.

- **Text Classification**: Assigning categories or labels to text documents based on their content. Examples include spam detection, topic classification, and sentiment analysis.
- **Sentiment Analysis**: Determining the sentiment (positive, negative, neutral) expressed in a piece of text, which is useful for analyzing customer feedback, social media posts, and reviews.


#### Data Sources
WineEnthusiast [Wine Reviews](https://www.kaggle.com/datasets/zynicide/wine-reviews) data set on Kaggle.

#### Methodology
The CRISP-DM methodology is applied to solving this data science problem.
- Given the business objective defined above, the data will be explored and cleaned up.
- After that, natural language processing techniques including stemming and lemmatization will be used to extract features from textual descriptions included in reviews of wines.
- Then, several models will be trained to try to classify the wine based on its descriptions. Both individual multiclass classification algorithms, as well as ensemble methods will be used, and compared the performance to neural networks.
- For example: we may want to one-hot encode the categorical features and tfidfvectorize the text features.

1. set aside test data
1. remainder is training data
1. Preprocessing corrects flaws in the data
1. build features for the model
1. train the model to minimize loss function
1. repeated for different regularization and hyper parameters, and even differnet models

data: Corpus - text reviews, consisting of documents.
1. split corpus into test and trainng data sets
1. preprocess the documents in the training corpus
  - tokenization - split the grammatical units, tokens
  - normalization - reduce tokens to core set that captures important information
1. feature extraction - converts text based document into numerical representation
  - bag of words
  - TF-IDF
1. train model, minimizing loss function
1. repeat for other models, hyper parameters, and regularization

NLTK - NLP specific preproseccing and feature extraction

Choosing Stem since this task is similar to sentiment analysis

**Preprocessing**
The various text preprocessing steps are:

Tokenization
Lower casing
Stop words removal
Stemming
Lemmatization

Depending on the performance of the various models, a recommendation will be made, including its performance characteristics.

#### Results
What did your research find?

**WIP**

#### Next steps
Wine experts have information about soil characteristics, weather, temperature, and precipitation during the growing season of where the wine is grown. Given the geolocation of the winery that produced the wines, it would be interesting to augment this data set with data from 
- XXXXX
- XXXXX


#### Outline of project

- [initial data exploration](wine_review-initial_data_exploration.ipynb)
- [data cleaning](wine_review-data_cleaning.ipynb)
- [exploratory data analysis](wine_review-eda.ipynb)
- [preprocess](wine_review-preprocess.ipynb)
- [feature extraction](wine_review-feature_extraction.ipynb)
- [train initial model](wine_review-baseline_model.ipynb)


##### Contact and Further Information
For information about this project, please contact `tuque_smith` on Kaggle.
