"""

05-3_Feature_Selection.py
Reducing the number of features.

"""

import sklearn.datasets as ds
import sklearn.feature_selection as fs
import sklearn.neighbors as nb



##### Generate a synthetic data set with a lot of features (60)
X, y = ds.make_classification(n_samples=100, n_features=60, n_redundant=0, n_classes=2)

# Remember that the output of ds.make_classification() is an ndarray
type(X)

# We can check the number of rows and columns using the 'shape' method
X.shape



######## Apply the univariate approach with the filter method
#
# Remember:
#   - The filter method uses a quality measure Q that is independent of the learning algorithm.
#   - The univariate approach evaluates each feature individually using Q and selects the k features with highest Q.

# Use class 'SelectKBest()' from the sklearn module 'feature_selection'
#
#   To use it, we follow the "initialize-fit-transform" process.
#
#   1. Initialize
#       Create an instance of the SelectKBest() class by specifying the parameters:
#       - score_func = fs.f_classif (specify the quality metric)
#         'fs.f_classif' is the ANOVA F-value.It measures the strength of relationship between an individual feature and the target.
#       - k = 15 (To reduce from 60 to 15 features, we select the 15 individually best features)
kb = fs.SelectKBest(score_func=fs.f_classif, k=15)
#
#   2. Fit
#       Calculate the ANOVA F-vlaues.
#       Notice: To calculate the F-Value, both, X and y, ares necessary.
kb.fit(X, y)
#
#   3. Transform
#       Reduce the dataset X to the 15 selected features.
X_kb = kb.transform(X)

# Let's check the shape after feature selection:
X_kb.shape # 15 columns left




######## Apply the iterative approach with the wrapper method
#
# Remember:
# - The wrapper method uses the performance of a machine learning algorithm as a wrapper for Q.
#   In this example, we use the KNeighborsClassifier as a wrapper.
#   We use the recognition rate as a performance measure for the wrapper.
# - The iterative approach is smarter than the univariate approach.
#   It searches in the "space" of feature subsets for the best subset.
#   In this example, we use Sequential Foreward Search (sfs) as a search strategy.

# Wrapper: Use the class 'KNeighborsClassifier()' from the sklearn module 'neighbors'
# Search: Use the class 'SequentialFeatureSelector()' from the sklearn module 'feature_selection'
#
#   To use it, we follow the "initialize-fit-transform" process.
#
#   1. Initialize the wrapper
#       Create an instance of the KNeighborsClassifier() class by specifying the parameter:
#       - n_neighbors = 1 (use 1 neighbor for classification)
knn = nb.KNeighborsClassifier(n_neighbors=1)
#       This instance of KNeighborsClassifier() will be used by the search algorithm.
#
#      Initialize the search algorithm
#       Create an instance of the SequentialFeatureSelector() class by specifying the parameters:
#       - estimator = knn (use knn as a wrapper for quality estimation)
#       - direction = 'forward' (choose sequential _foreward_ search)
#       - n_features_to_select = 15 (search for the best feature set with 15 features)
sfs = fs.SequentialFeatureSelector(estimator=knn, direction='forward', n_features_to_select=15)
#
#   2. Fit
#       Evaluate the feature sets generated by sfs based on the performance of the knn classifier
#       Select the best feature set that contains 15 features
#       Notice: This step takes a while!
sfs.fit(X, y)
#
#   3. Transform
#       Reduce the dataset X to the 15 selected features.
X_sfs = sfs.transform(X)

# Let's check the shape after feature selection:
X_sfs.shape