# GapLearn

GapLearn bridges gaps between other machine learning and deep learning tools. All models can be passed to the functions below regardless of the framework they were built upon (scikit-learn, tensorflow, xgboost, or even good ole numpy). 

My first package objective is to bring transparency to the often black-boxy model training process by making by making robust post-mortem analysis of the hyperparameter and feature selection processes possible. The functions below also further automate some processes while still giving the user full control of the results.

Many features are on their way. Unit tests and full documentation will be added shortly.

The source code is available on [GitHub](https://www.github.com/awhedon/gaplearn)

## Installation

```bash
pip install gaplearn
```

See the latest version on [PyPI](https://pypi.org/project/gaplearn/)

## Submodules

### cv

The `cv` submodule will have these classes (sfs has been released):

#### sfs
**Description:**
- This is a sequential feature selector that enables you to perform backwards elimination with any model (not just a linear regression).
- At each step, the feature that has the lowest permutation importance is selected for removal. The permutation importance is measured as the decrease in accuracy by default, but the user can pass any custom scoring function.

**Improvements on their way:**
- Add forward selection and all subsets testing
- Add more built-in scoring functions to for assessing feature permutation importance
- Create custom permutation scoring method to remove `eli5` as a dependency
- Enable a user to get the feature set that matches a certain criteria ("has n features", "has score > x")

##### Methods
**backwards_elimination(X, y, model = 'logit', params = {}, fit_function = None, predict_function = None, score_function = None, score_name = 'accuracy', cols = [], verbose = 0)**
- Run the backwards elimination
- **Params:**
	- X: (DataFrame or matrix) with independent variables
	- y: (iterable) dependent corresponding variable values
	- params: (dict) parameter set for model
	- model: (str or custom model type) if str ('logit' or 'rfc'), a corresponding sci-kit learn model will be used; if custom model type, the model you pass will be used
	- fit_function: (function) the function that will be used to train the model; the function must accept the parameters `model`, `X`, and `y`; if this value is not set, `backwards_elimination` will attempt to use your model's `fit` method
	- predict_function: (function) the function that will be used to make predictions with the model; the function must accept the parameters `model`, and `X`; if this value is not set, `backwards_elimination` will attempt to use your model's `predict` method
	- score_function: (function) the function that will be used to score the model and determine the feature permutation importance; the function must accept the parameters `y` and `preds`; if this value is not set, the accuracy will be used
	- score_name: (str) name of the score calculated by the `score_function`; 'accuracy' by default

**Example 1:**
```python
#### Perform a backwards elimination with sci-kit learn's random forest model ####

import pandas as pd
from gaplearn.cv import sfs

X = pd.read_csv('X_classification.csv')
y = pd.read_csv('y_classification.csv')

fs_rfc = sfs()

print('The backwards elimination has been run: {}'.format(fs_rfc.be_complete)) # prints False

# Run the backwards elimination
fs_rfc.backwards_elimination(X, y, model = 'rfc', params = {'n_jobs': -1})

# Get the step-by-step summary
summary_rfc = fs_rfc.get_summary_be() # Alternatively, `summary_rfc = fs_rfc.summary_be`

# Get the predictions and true values for each observation
results_rfc = fs_rfc.get_results_be() # Alternatively, `results_rfc = fs_rfc.results_be

# Get the features used in the analysis
features_rfc = fs_rfc.features_be # Alternatives, `sorted(list(results_rfc['feature to remove']))

# Identify which feature set can achieve at least 85% accuracy with the smallest number of features
at_least_85_rfc = fs_rfc.get_set_by_score_be(min_score = .85, num_steps = 1)

# Identify the best model with only 4 features
features_4_rfc = fs_rfc.get_set_by_features_be(num_features = 4)
```

**Example 2:**
```python
#### Perform a more complex backwards elimination with sci-kit learn's naive bayes model ####

import pandas as pd
from gaplearn.cv import sfs

from sklearn.linear_model import SGDRegressor

model_sgd = SGDRegressor(loss = 'modified_huber', penalty = 'elasticnet')

X = pd.read_csv('X_regression.csv')
y = pd.read_csv('y_regression.csv')

fs_nb = sfs()

# Define a score_function
def mse(y, preds):
	score = sum([(preds[i] - y[i]) ** 2 for i in range(y.shape[0])]) / y.shape[0]
	return score

# Define a predict_function
def arbitrary_prediction(model, X):
	preds = model.predict(X) + 1 # arbitrarily deciding to add 1 to the prediction (realistically, this would be a wrapper for model that don't have a `fit` method)
	return preds

# Run the backwards elimination
fs_nb.backwards_elimination(X, y, model = model_sgd, predict_function = arbitrary_prediction, score_function = mse)

# Get the step-by-step summary
summary_nb = fs_nb.get_summary_be() # Alternatively, `summary = fs_nb.summary_be`

# Get the predictions and true values for each observation
results_nb = fs_nb.get_results_be() # Alternatively, `results = fs_nb.results_be

# Get the features used in the analysis
features_nb = fs_nb.features_be # Alternatives, `sorted(list(results['feature to remove']))

# Identify which two feature sets can achieve at least 85% accuracy with the smallest number of features
at_least_85_nb = fs_nb.get_set_by_score_be(min_score = .85, num_steps = 2)

# Identify the best models with only 3-5 features
features_3_5_nb = fs_nb.get_set_by_features_be(num_features = 3, max_features = 5)
```

#### param_search_cluster (in development)
**Description:**
- This is a hyperparameter grid/random search for clustering algorithms
- Unlike other grid/random search algorithms, this one enables you to get the observation-by-observation results from each parameter set so that you can do deep post-mortem analysis of the grid/random search.

#### param_search (in development)
**Description:**
- This is a hyperparameter grid/random search for both regression algorithms and classification algorithms
- Unlike other grid/random search algorithms, this one enables you to get the observation-by-observation results from each parameter set so that you can do deep post-mortem analysis of the grid/random search.

### data_eng

The `data_eng` submodule will have these classes (sfs has been released):

#### distributed_sql (in development)
**Description:**
- This enables users to chunk multi-parameter sql queries and process them on multiple threads.