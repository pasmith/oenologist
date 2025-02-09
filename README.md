# oenologist
capstone project for UCB MLAI certificate: wine review



The research question you intend to answer (in one sentence, if possible)
I intend to answer how to predict the quality (and price) of a wine based on the review comments given by a taster.

Your expected data source(s) (as either a link to existing data or a sentence describing where you will source the data from)
The primary data source is from Kaggle: https://www.kaggle.com/datasets/zynicide/wine-reviews. It contains approximately 130k wine reviews collected from WineEnthusiast in 2017.

The techniques you expect to use in your analysis
I intend to augment the data set with geographic coordinates of the winery location, and use natural language processing techniques to extract categorical features from the descriptions, such as the flavor and texture the taster detected while reviewing the wine, that can be used to train several models to predict the quality of the wine based on its variety and the observations from the review.
Predicting the quality can be modeled as predicting between several categories of quality. For this reason, I intend to train algorithms like Multiclass Logistic Regression, Decision Trees, as well as One-vs-All (or One-vs-One), and neural networks to predict the wine quality from the comments.
To predict the price, I intend to train Linear, Decision Forest, and neural network models, depending on what models we learn in the course.

The expected results
When evaluating wines by wine variety, there are traits that are more desirable for different types of wines. The description tends to be similar. For example, good Cabernet Sauvignon wines tend to be dry, not sweet. As long as the natural language processing can extract features that capture the basic meaning with some amount of consistency, then it should be reasonable to expect the prediction to be somewhat effective. After all, humans make wine purchasing decisions based on these reviews. There is informational content in the review for the algorithm to use.

Why this question is important
Being able to predict what to expect from a wine is important in several ways.
For wine lovers, they can understand what wines are similar to wines they normally enjoy. Being an agricultural product, there are new wine releases every year, and every year, the quality changes. Being able to determine whether the wine will be what they expect based on the review can help individuals make informed decisions when purchasing wine. These types of algorithms can be personalized. Instead of matching only against what a professional reviewer might recommend, an algorithm like this could be trained on quality scores that individuals assign. This could be very useful in helping wine consumers discover new wines that match their preferences.
Wine stores, distributors and restaurants, can use reviews and quality insights derived from the reviews to fine tune their inventory. They can look for wines that match what their customers buy, especially if the model predicts larger margins between the wholesale price for the wine, and what the model predicts customers would be willing to pay for that wine.
Wineries and wine producers can benefit from this type of analysis by gaining an understanding of how the market will perceive the quality of their product. That information can be used by these organizations to fine tune their strategy for bringing their product to market. For example, they may change how much volume they release under a specific label or blend in order to increase the returns on a well reviewed wine predicted to be perceived as high quality. It may also help business understand when such techniques may not work and find alternate strategies to sell their stock.



### Code Quality
- unittest: testing framework
- coverage: test code coverage instumentation
- Pylint: One of the most widely used linters, Pylint checks for errors, style violations, and adherence to PEP 8 (Python's style guide).
- Flake8: A wrapper around PyFlakes (checks for errors), pycodestyle (checks for style violations), and McCabe (checks for code complexity).
- Ruff: An extremely fast Python linter written in Rust. see [ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit)
- Mypy: A static type checker that helps catch type-related errors.
- [balck](https://medium.com/@dineshsuthar03/mastering-python-code-quality-pep-8-pylint-and-black-69b71d945e7d): code formatter





