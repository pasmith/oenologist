### Oenologist
> Oenologists evaluate the quality of wine and ensure it meets the desired outcome.

*Applying data science to evaluate wine quality*


**Patrick Smith**

---
#### Executive summary

In this project, we will apply natural language processing and use machine learning techniques to predict the quality of wines based on reviews written about those wines. Given that the tasters reviewing the wines are [Sommeliers](https://en.wikipedia.org/wiki/Sommelier) professionally trained in the art of wine tasting, we can expect a fair amount of consistency in the reviews. We expect different sommeliers reviewing similar wines awarding similar scores and providing similar descriptions explaining why the wines earned the points they did.

Part of what drives this consistency is that these wine reviews are blind. The tasters do not know the winery or winemaker, when they taste the wine. Depending on the task, they may know the varietal and general provenance and/or vintage (year) the wine was made. This methodology allows marketplaces like [WineEnthusiast](https://www.wineenthusiast.com/about-us/) to differentiate themselves as influencers in the wine consumer industry. To maintain that influence, the review process must be consistent, repeatable and objective, which is ideal for machine learning.

In fact, because of this consistency, we can expect the reviews to result in clustering similar to those shown in the infographic below to emerge from the reviews. 

<div>
  <p align='center'><img src="images/banner.png" alt="pinot noir" width="500"/></p>
  <p align="center">Fig 1: Most common words used in wine reviews</p>
</div>

An initial Logistic Regression model is used as a baseline model and achieved an accuracy of $51.8\%$. We will train and tune supervised learning classifiers, as well as neural network classifiers, and can expect that after tuning, the prediction accuracy will increase.

---

#### Rationale
The global wine market is expected to be nearly a $\$350$ billion industry in 2025. Gross margins for vineyards and wineries are on average 50%, while wine retailers and restaurants have profit margins of nearly $30\%$ and $70\%$ respectively. Factors that affect these profit margins include production volume, location, size of the winery, and market positioning. Wine reviews and quality assessments impact the reputation of the wine in the market, and in term impact both the demand for and the price that can be charged for a wine. As this testimonial attests, ratings can make the difference between being a successful business, or failing.

>Last year, slow sales at Domaine Clavel resulted in an unsold stockpile, putting the winery in a tough spot. Then, in July, Wine Enthusiast awarded its Côtes du Rhône Rouge a stunning $92$ points.
>
>“I was in disbelief. A $92$-point rating for a Côtes du Rhône—it felt unreal!” Clavel recalls. The score piqued interest from Costco, which ultimately ordered $100,000$ bottles. “It changed everything. For the first time this year, I felt confident about facing the bank.”
>
>—Claire Clavel – Owner of Domaine Clavel
source: [Wine Enthusiast Ratings Testimonials](https://www.wineenthusiast.com/submit-for-rating/?srsltid=AfmBOootA0Oo9WQahh1Nyo1JoBws2j7rwSIPEgs1YKwyJB6bfhF7TeVt#ratings-help-you)

Since the points ratings drive the demand and price of wines, it is vitally important that the reviews, and the associated ratings be fair and accurate. The reputation of the marketplace awarding the rating is critical to the marketplace.

Here are three business use cases that can benefit from this research:
- Wine producers are interested in ensuring their wines receive the highest ratings their wines can earn. As the testimonial mentioned above, this can make or break their business.

- Wine marketplaces need to protect the reputation and influence on the market their reviews have. To do this, they need to operationalize a distributed global corps of reviewers at scale to continuously taste new wine releases and offerings while maintaining the consistency and predictability that makes their ratings influential. Onboarding new wine reviewers in ways that don't jeopardize the reputation of the marketplace is a challenge. A new, unknown reviewer could do real harm if a review is published without review. However, duplicating reviews is costly. Statistical techniques, and machine learning techniques can minimize the costs involved in ramping and training new reviewers, all while preserving the standards and quality of the review process. AI can even provide coaching to help train and onboard reviewers.

- Wine distributors and restaurants can fine tune their inventories and increase profit margins by finding alternatives wine offerings that are equivalent in taste but cheaper. They might be able to achieve higher markup while offering the customer slightly cheaper alternatives.

---
#### Research Question
There are two research questions being investigated here.
1. Can the rating, be predicted from the wine review taster notes?

<p align="center">
<img src="images/points.png" alt="drawing" width="500"/>
<div  align="center"><i>from [WineEnthusiast](https://www.wineenthusiast.com/ratings/)</i></div>
</p>

#### Data Sources
The data source for this project is the WineEnthusiast [Wine Reviews](https://www.kaggle.com/datasets/zynicide/wine-reviews) data set on Kaggle. This dataset contains roughly 130k wine reviews commissioned by [WineEnthusiast](https://www.wineenthusiast.com/) between May and November 2017. 

The dataset contains thirteen (13) fields that describe:
- **what** wine is being reviewed: winery, designation, variety, vintage (in review title), price
- **where** the wine is from: country, province, region_1, region_2
- **who** reviewed the wine: taster_name, taster_twitter_handle
- the review and resulting **rating**: description, points

After data cleaning and extracting features from the wine review descriptions, the dataset consisted of $98,460$ samples each with $837$ features extracted from One Hot Encoders of categories, augmenting numerical data given relationships deiscovered during Exploratory Data Analysis, and converting reviews to sentence embeddings using the [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) pre-trained model that captures the semantic meaning of the review using a $768$ dimensional dense vector.

#### Methodology
There two distinct machine learning goals in this project.

1. After getting to know the data and deciding what features to use, how to handle duplicate and missing data, an exploratory data analysis will be performed to understand the distribution of target classes, and how features relate to the target and each other.
1. Then, since we are trying to extract features from the wine reviews, various natural language processing techniques will be assessed, including bag-of-words (BoW) and term frequency-inverse document frequency (TF-IDF) and compared to sentence embeddings to determine how to extract information from the reviews.
1. Then several popular supervised learning models will be trained on a subset of the data to determine which models to train the entire dataset on based on training time and relative performance.
1. And finally, a decision will be made on which target representation to use, points, or rating categories.
1. Once the features, models, and target have been selected, three supervised learning models will be trained and compared to a baseline result.
1. And a neural network will be trained and compared to the machine learning classifiers.

##### Evaluation Metric
Classification Accuracy is used as the primary evaluation metric providing the ratio of classes that are correctly predicted relative to the true value.

Since this is a multinomial classification problem, the prediction results can be compared to correct values using the confusion matrix. Not only does the confusion matrix provide insights about how often the classifier is correct, it can give insights about the kinds of classification errors the classifiers are making. Consider the confusion matrix comparing the results of the XGBoost classifier and the neural classifier shown below.

<p align="center">
<img src="images/xgboost-conf-matrix.png" width="45%">&nbsp;<img src="images/neural-conf-matrix.png" width="45%">
</p>

The classification errors made by the neural classifiers are close to the diagonal, indicating that the neural classifier generally understood the quality of the wine, but missed some nuances of wines in adjacent categories. In contrast, the XGBoost classifier made large errors far off the diagonal. For example, it $38\%$ of the wines labeled `acceptable` were in face `excellent` wines. Such a misclassification can be devastating, not just to the winemaker, but also the marketplace publishing the review.

#### Results
What did your research find?

1. The first interesting finding that surfaced during exploratory data analysis is that there is a correlation between the length of the review and the rating the wine receives. Generally, the longer the review the better the rating. We can speculate that reviewers have to explain the nuances that make high quality wines remarkable, and such explanations require more words to articulate.
    - High quality wines average $300$ words in length, while lower quality wines only average $150$ words.
    - Reviews longer than $200$ words indicate a superior quality wine.
1. The descriptions do contain a fair amount of structure, especially sentence embeddings.
1. The dataset is insufficient to predict the `points` solely from the wine reviews. There may be several reasons for that. First, the same wines are not reviewed frequently. This makes sense. It may be prohibitive for the marketplace to publish multiple reviews for the same product. Likely, they determine one review to publish, so that they can make space to review other wine releases. So the dataset is lacking completeness. Also, reviews are short in form. Perhaps, the full taster notes would contain more information about what the tasters observed in the wine being reviewed. That information could help the models better discern between scores.
    - As a result of this, the analysis is using the six (6) rating categories instead of points as the target to predict.
1. The baseline model using review length as the sole feature derived from the review is able to achieve an accuracy of $51.8\%$.
1. Several classifiers were trained and tuned including a multinomial Naive Bayes classifier, an ensemble classifier, and XGBoost. The Random Forest classifier was able to achieve an accuracy of $53.7\%$, while XGBoost was able to achieve an accuracy of $53.1\%$ much faster, in $\frac{1}{80}\text{th}$ of the time.
1. The neural classifier achieved even higher accuracy of $58.4\%$. Adding more hidden layers, or changing the shape of the dense layers did not appear to significantly improve the accuracy.
1. From this experiment, we can conclude the following.
    - Natural language processing of taster notes can be analyzed to predict the point rating a wine can, or should get. After all, the purpose of the reviews are to inform consumers to buy wines. High prices for superior wines have to be justified, and the reviews are one vehicle through which this is accomplished. For credibility and reputational reasons, these reviews need to be fair and repeatable.
    - To do this though, one needs access to all reviews collected, not just the subset published, from which this dataset is derived.
    - One should also get access to the full tasting notes since the reviews are edited in form to be concise. A lot of information is lost.

#### Next steps
  - Collecting more data, especially the full tasting notes from all tasters.
  - Create a Task Management System powered by this machine learning model that can onboard new wine reviewers while minimizing the cost required to maintain the accuracy and integrity of the review process.
  - Additional data augmentation. Given lat-lon coordinates of wineries, add soil and precipitation data during growing season. Use in climate prediction applications to predict quality of wines given changing soil conditions and weather patterns. Tasters know this about the wines when they taste it. They look for the effects of climate and location when tasting.
  - Cutting-edge systems like [eTaste](https://www.theguardian.com/science/2025/feb/28/scientists-create-e-taste-device-that-could-add-flavour-to-virtual-reality-experiences) can be used to measure and calibrate wine tasters.

#### Outline of project


1. [Understanding the data](data_understanding.ipynb), get to know the data.
1. [Data Cleaning](data_cleaning.ipynb), make decisions about missing values, duplicates, outliers, data formatting & interpretation.
1. [Exploratory Data Analysis](exploratory-data-analysis.ipynb), explore whether classes are balanced, distributions of values, and relationships between features, etc.
1. [Feature Selection](feature-selection.ipynb), determine which natural language processing technique to use to extract features from the review descriptions
1. [Model Selection](model-selection.ipynb), explore several popular classifier models on a subset of the data to determine which models to train and tune
1. [Target Selection](target-selection.ipynb), determine which target classes to use based on the features that can be extracted from reviews
1. [Model Training](model-training.ipynb), train and tune three ($3$) classifiers
1. [Neural Network Classifier](neural-classifier.ipynb), train two(2) neural network classifiers to compare to the supervised learning classifiers.
1. [Summary](summary.ipynb), discuss conclusions and next steps.


##### Contact and Further Information
For information about this project, please contact `tuque_smith` on Kaggle.



---
#### Criteria
**Project Organization**
- [x] README file with summary of findings and link to Jupyter Notebook(s)
- [x] Jupyter notebook(s) with headings and text appropriately formatted
- [ ] No unnecessary files
- [ ] Directories and files with appropriate names

**Syntax and Code Quality**
- [ ] Libraries imported and named correctly
- [ ] Code with no errors
- [ ] No long strings of code output
- [ ] Demonstrate competency with pandas
- [ ] Demonstration competence with viz libraries
- [ ] Appropriate use of comments
- [ ] Sensible variables

** Visualizations:
- [ ] Appropriate plots for categorical and continuous variables
- [ ] Plot with human-readable labels
- [ ] Plots with descriptive titles
- [ ] legible axes
- [ ] Appropriate use of subplots when necessary
- [ ] Plots that are scaled appropriately

** Modeling:
- [x] Multiple regression or classification models
- [x] Cross-validation of models
- [x] Grid Search hyperparameters
- [ ] Appropriate interpretation of models
- [x] Appropriate interpretation of evaluation metric
- [x] Clear identification of evaluation metric
- [x] Clear rationale for use of given evaluation metric

Findings:
- [ ] Clearly states business understanding of the problem
- [ ] Clean and organized notebook with data cleaning
- [ ] Correct and concise interpretation of descriptive and inferential statistics
- [ ] Clearly states findings in their own sections, with actionable items highlighted in appropriate language for a nontechnical audience
- [ ] Next steps and recommendations