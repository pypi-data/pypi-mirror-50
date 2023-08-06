Performance Overview of Supervised Learning methods 
====================================================

Do not know which supervised learning method is good for your dataset?
Would you like to know it in just few seconds?

:Congratulations:
  You are about to learn about a package which gives you the solution to all above problems!

This small package of merely few bytes and code written in less than 100 lines, provide you the overview of all fundamental metrics measured for almost all supervised learning method.


+---------------------------------------------+---------------------------------------------+
|               Models evaluated:             |             Metrics considered:             |
+=====================+=======================+========================+====================+
|    Decision Trees   |  Logistic Regression  |        Accuracy        |      Precision     |
+---------------------+-----------------------+------------------------+--------------------+
|     Naive Bayes     |          SVM          |       Jaccard Score    |      F1_Score      |
+---------------------+-----------------------+------------------------+--------------------+
|   Neural Networks   |          K-NN         |      R (Corr. Coeff.)  |      ROC AUC       |
+---------------------+-----------------------+------------------------+--------------------+
|    Random Forest    |        Adaboost       |           MSE          |      Log Loss      |
+---------------------+-----------------------+------------------------+--------------------+


-------------------------------------------------------------------------------------------------------------------------

:Mandatory inputs required:
  A Pandas DataFrame

:Optional inputs in the given order:
  - Column numbers for the predictors in the form of a LIST 
      Default: It will take all columns except the last one.
  - Column number for the response in the form of a LIST
      Default: It will take the last column.
  - Test size in Float Ex. 0.3 for 30% Test Size.
      Default: 0.25 (25% Test size) will be assumed.


-------------------------------------------------------------------------------------------------------------------------

:How to install:
  Type ``pip install basicanalysis`` in command line to install the package
  
  To call the module from this package, type ``from basicanalysis.basicanalysis import basicanalysis``
  
*Note : To import other modules, use the following command.*
  ``from basicanalysis.basicanalysis import knn``
  ``from basicanalysis.basicanalysis import knn_10fold``
  ``from basicanalysis.basicanalysis import *``

-------


Neat! Isn't it?
===============


MAJOR UPDATE: 0.0.3 -> 0.1.0, BasicAnalysis -> basicanalysis
============================================================

* Added class knn to run K-NN method to compare with multiple inputs
* Added class knn_10fold to run K-nn method on training data with 10-fold cross validation, comparing multiple inputs.

------

README file for the task

Written in reStructuredText or .rst file, and used to generate the project page on PyPI. Images coming soon...
