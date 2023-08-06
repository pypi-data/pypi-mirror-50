#!/usr/bin/env python

# importing important and also basic libraries for data processing

import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from termcolor import colored
from sklearn.model_selection import cross_val_score

# Pre-processing

encode = preprocessing.LabelEncoder()

# Metrics of interest to see which one performs better

metrics = {'Accuracy': 'accuracy_score', 'Precision': 'precision_score',
           'Jaccard Score': 'jaccard_similarity_score', 'F1_Score': 'f1_score', 'R Value': 'matthews_corrcoef',
           'ROC AUC': 'roc_auc_score', 'MSE': 'mean_squared_error', 'Log Loss': 'log_loss'}

class basicanalysis:

    def __init__(self, df, pred=None, resp=None, tsts=0.25, seed=1):
        self.df = df
        self.pred = pred if pred is not None else [i for i in range(len(df.columns) - 1)]
        self.resp = resp if resp is not None else [len(df.columns) - 1]
        self.tsts = tsts
        self.seed = seed

        predictors = df.iloc[:, self.pred]
        predictions = df.iloc[:, self.resp]

        x_train, x_test, y_train, y_test = train_test_split(predictors,
                                                            predictions,
                                                            test_size=self.tsts,
                                                            random_state=self.seed)

        x_train = x_train.apply(encode.fit_transform)
        y_train = y_train.apply(encode.fit_transform)

        x_test = x_test.apply(encode.fit_transform)
        y_test = y_test.apply(encode.fit_transform)

        # Just looking

        for idx, col in enumerate(predictions.columns):
            print('Train data distribution:')
            td = pd.concat([predictions[col].value_counts(),
                            round(predictions[col].value_counts(normalize=True) * 100, 2)], axis=1)
            td.columns = ['Counts', 'Percentage']
            print(td)

        # Defining the models

        models = pd.DataFrame(data={'Model': ['Decision Trees', 'Logistic Regression', 'Naive-Bayes', 'SVM',
                                              'Neural Netwoks', 'K-NN', 'Random Forest', 'Adaboost'],
                                    'attr': ['tree', 'linear_model', 'naive_bayes', 'svm', 'neural_network',
                                             'neighbors', 'ensemble', 'ensemble'],
                                    'class': ['DecisionTreeClassifier', 'LogisticRegression', 'GaussianNB',
                                              'SVC', 'MLPClassifier', 'KNeighborsClassifier',
                                              'RandomForestClassifier', 'AdaBoostClassifier']})

        score = pd.DataFrame(columns=models['Model'], index=list(metrics.keys()))

        for i in range(len(models)):

            # Importing models

            __import__("sklearn." + models['attr'][i])
            attr = getattr(__import__("sklearn"), models['attr'][i])
            model = getattr(attr, models['class'][i])

            # Assigning the model and getting the metrics

            try:
                model = model()
            except ValueError:
                pass
            y_pred = model.fit(x_train, y_train.values.ravel()).predict(x_test)

            for j, each in enumerate(metrics):
                # Importing metrics

                __import__("sklearn.metrics")
                attr = getattr(__import__("sklearn"), 'metrics')
                metric = getattr(attr, metrics[each])

                score.loc[each, models['Model'][i]] = round(metric(y_test, y_pred), 2)

        self.output = score

    def __repr__(self):
        return str(self.output)


class knn():

    def __init__(self, df, pred=None, resp=None, tsts=0.25, seed=1, n_neighbors=5, algorithm='auto', leaf_size=30,
                 n_jobs=None):
        self.df = df
        self.pred = pred if pred is not None else [i for i in range(len(df.columns) - 1)]
        self.resp = resp if resp is not None else [len(df.columns) - 1]
        self.tsts = tsts
        self.seed = seed

        self.n_neighbors = [n_neighbors] if isinstance(n_neighbors, int) else n_neighbors
        self.algorithm = [algorithm] if isinstance(algorithm, str) else algorithm
        self.leaf_size = [leaf_size] if isinstance(leaf_size, int) else leaf_size
        self.n_jobs = n_jobs if n_jobs is not None else n_jobs

        predictors = df.iloc[:, self.pred]
        predictions = df.iloc[:, self.resp]

        x_train, x_test, y_train, y_test = train_test_split(predictors, predictions, test_size=self.tsts,
                                                            random_state=self.seed)

        x_train = x_train.apply(encode.fit_transform)
        y_train = y_train.apply(encode.fit_transform)

        x_test = x_test.apply(encode.fit_transform)
        y_test = y_test.apply(encode.fit_transform)

        # Just looking

        for idx, col in enumerate(predictions.columns):
            print('Train data distribution:')
            td = pd.concat([predictions[col].value_counts(),
                            round(predictions[col].value_counts(normalize=True) * 100, 2)], axis=1)
            td.columns = ['Counts', 'Percentage']
            print(td)

        # K-NN magic starts here

        knn_score = pd.DataFrame(index=list(metrics.keys()))

        from sklearn.neighbors import KNeighborsClassifier

        algo_err = set()
        leaf_err = set()
        err_dict = {}
        bad_algo = {}
        if isinstance(self.n_neighbors, list):
            for i in range(len(self.n_neighbors)):
                if isinstance(self.n_neighbors[i], int):
                    if isinstance(self.algorithm, list):
                        for j in range(len(self.algorithm)):
                            if isinstance(self.algorithm[j], str):
                                if not bad_algo or (bad_algo['i'] != i and bad_algo['j'] != j):
                                    if self.algorithm[j] not in ['auto', 'ball_tree', 'kd_tree', 'brute']:
                                        print(colored('\n \033[1m "' + self.algorithm[j] +
                                                      '" is not a proper input in algorithm!', 'red'))
                                        print('\n -> Please enter one of [‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’]')
                                        bad_algo['i'] = i
                                        bad_algo['j'] = j
                                        print(' -> Currently moving on by using "auto" instead')
                                        self.algorithm[j] = 'auto'
                                    else:
                                        pass
                                if isinstance(self.leaf_size, list):
                                    for k in range(len(self.leaf_size)):
                                        if isinstance(self.leaf_size[k], int):

                                            try:
                                                model = KNeighborsClassifier(n_neighbors=self.n_neighbors[i],
                                                                             algorithm=self.algorithm[j],
                                                                             leaf_size=self.leaf_size[k],
                                                                             n_jobs=n_jobs)
                                                col = 'n=' + str(self.n_neighbors[i]) + ' ' + self.algorithm[j] + \
                                                      ' leaf=' + str(self.leaf_size[k])

                                            except ValueError:
                                                if not err_dict or \
                                                        (err_dict['i'] != i and err_dict['j'] != j and err_dict[
                                                            'k'] != k):
                                                    print(colored('\n \033[1m Yo!! There is an error occured '+
                                                                  'while building the model. Check!', 'red'))
                                                    err_dict['i'] = i
                                                    err_dict['j'] = j
                                                    err_dict['k'] = k
                                                pass

                                            y_pred = model.fit(x_train, y_train.values.ravel()).predict(x_test)

                                            for num, each in enumerate(metrics):

                                                # Importing metrics

                                                __import__("sklearn.metrics")
                                                attr = getattr(__import__("sklearn"), 'metrics')
                                                metric = getattr(attr, metrics[each])

                                                try:
                                                    entry = round(metric(y_test, y_pred), 2)
                                                except:
                                                    entry = np.nan
                                                knn_score.loc[each, col] = entry

                                        else:
                                            if not leaf_err or k not in leaf_err:
                                                print(colored('\n \033[1m An inappropriate non-integer element in ' +
                                                              'leaf_size list at location ' + str(
                                                    k) + '! PLEASE CHECK!!!', 'red'))
                                                leaf_err.add(k)
                                            pass
                                else:
                                    print(colored('\n \033[1m Inappropriate integer or a list of integers' +
                                                  'entered for leaf_size!', 'red'))
                                    print('Taking leaf_size as 30 and moving on...')
                            else:
                                if not algo_err or j not in algo_err:
                                    print(colored('\n \033[1m An inappropriate non-string element in algorithm ' +
                                                  'list at location ' + str(j) + '! PLEASE CHECK!!!', 'red'))
                                    algo_err.add(j)
                                pass
                    else:
                        print(
                            colored('\n \033[1m Inappropriate string value or a list of strings entered for algorithm!',
                                    'red'))
                        print('Taking algorithm as "auto" and moving on...')
                else:
                    print(colored('\n \033[1m An inappropriate non-integer element in n_neighbors list at location ' +
                                  str(i) + '! PLEASE CHECK!!!', 'red'))
                    pass

        else:
            print(colored('\n \033[1m Inappropriate integer or a list of integers entered for n_neighbors!', 'red'))
            print('Taking n_neighbors as 5 and moving on...')

        self.output = knn_score

    def __repr__(self):
        return str(self.output)



class knn_10fold():

    def __init__(self, df, pred=None, resp=None, tsts=0.25, seed=1, n_neighbors=5, algorithm='auto', leaf_size=30,
                 n_jobs=None):
        self.df = df
        self.pred = pred if pred is not None else [i for i in range(len(df.columns) - 1)]
        self.resp = resp if resp is not None else [len(df.columns) - 1]
        self.tsts = tsts
        self.seed = seed

        self.n_neighbors = [n_neighbors] if isinstance(n_neighbors, int) else n_neighbors
        self.algorithm = [algorithm] if isinstance(algorithm, str) else algorithm
        self.leaf_size = [leaf_size] if isinstance(leaf_size, int) else leaf_size
        self.n_jobs = n_jobs if n_jobs is not None else n_jobs

        predictors = df.iloc[:, self.pred]
        predictions = df.iloc[:, self.resp]

        x_train, x_test, y_train, y_test = train_test_split(predictors, predictions, test_size=self.tsts,
                                                            random_state=self.seed)

        x_train = x_train.apply(encode.fit_transform)
        y_train = y_train.apply(encode.fit_transform)

        x_test = x_test.apply(encode.fit_transform)
        y_test = y_test.apply(encode.fit_transform)

        # Just looking

        for idx, col in enumerate(predictions.columns):
            print('Train data distribution:')
            td = pd.concat([predictions[col].value_counts(),
                            round(predictions[col].value_counts(normalize=True) * 100, 2)], axis=1)
            td.columns = ['Counts', 'Percentage']
            print(td)

        # K-NN magic starts here

        metrics = {'Accuracy': 'accuracy', 'Precision': 'average_precision', 'Jaccard Score': 'jaccard',
                   'F1_Score': 'f1_macro', 'R-squared': 'r2', 'ROC AUC': 'roc_auc',
                   'MSE': 'neg_mean_squared_error', 'Log Loss': 'neg_log_loss'}

        knn_score = pd.DataFrame(index=list(metrics.keys()))

        from sklearn.neighbors import KNeighborsClassifier

        algo_err = set()
        leaf_err = set()
        err_dict = {}
        bad_algo = {}
        if isinstance(self.n_neighbors, list):
            for i in range(len(self.n_neighbors)):
                if isinstance(self.n_neighbors[i], int):
                    if isinstance(self.algorithm, list):
                        for j in range(len(self.algorithm)):
                            if isinstance(self.algorithm[j], str):
                                if not bad_algo or (bad_algo['i'] != i and bad_algo['j'] != j):
                                    if self.algorithm[j] not in ['auto', 'ball_tree', 'kd_tree', 'brute']:
                                        print(colored('\n \033[1m "' + self.algorithm[j] +
                                                      '" is not a proper input in algorithm!', 'red'))
                                        print('\n -> Please enter one of [‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’]')
                                        bad_algo['i'] = i
                                        bad_algo['j'] = j
                                        print(' -> Currently moving on by using "auto" instead')
                                        self.algorithm[j] = 'auto'
                                    else:
                                        pass
                                if isinstance(self.leaf_size, list):
                                    for k in range(len(self.leaf_size)):
                                        if isinstance(self.leaf_size[k], int):

                                            try:
                                                model = KNeighborsClassifier(n_neighbors=self.n_neighbors[i],
                                                                             algorithm=self.algorithm[j],
                                                                             leaf_size=self.leaf_size[k],
                                                                             n_jobs=n_jobs)
                                                col = 'n=' + str(self.n_neighbors[i]) + ' ' + self.algorithm[j] +\
                                                      ' leaf=' + str(self.leaf_size[k])

                                            except ValueError:
                                                if not err_dict or \
                                                        (err_dict['i'] != i and err_dict['j'] != j and err_dict[
                                                            'k'] != k):
                                                    print(colored('\n \033[1m Yo!! There is an error occured '+
                                                                  'while building the model. Check!', 'red'))
                                                    err_dict['i'] = i
                                                    err_dict['j'] = j
                                                    err_dict['k'] = k
                                                pass

                                            scores = cross_val_score(model, x_train, y_train, cv=10, scoring='f1_macro')

                                            for num, each in enumerate(metrics):

                                                try:
                                                    scores = cross_val_score(model, x_train, y_train, cv=10,
                                                                             scoring=metrics[each])
                                                    entry = "%0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
                                                except:
                                                    entry = "NaN"
                                                knn_score.loc[each, col] = entry

                                        else:
                                            if not leaf_err or k not in leaf_err:
                                                print(colored('\n \033[1m An inappropriate non-integer element in ' +
                                                              'leaf_size list at location ' + str(k) +
                                                              '! PLEASE CHECK!!!', 'red'))
                                                leaf_err.add(k)
                                            pass
                                else:
                                    print(colored('\n \033[1m Inappropriate integer or a list of integers' +
                                                  'entered for leaf_size!', 'red'))
                                    print('Taking leaf_size as 30 and moving on...')
                            else:
                                if not algo_err or j not in algo_err:
                                    print(colored('\n \033[1m An inappropriate non-string element in algorithm ' +
                                                  'list at location ' + str(j) + '! PLEASE CHECK!!!', 'red'))
                                    algo_err.add(j)
                                pass
                    else:
                        print(
                            colored('\n \033[1m Inappropriate string value or a list of strings entered for algorithm!',
                                    'red'))
                        print('Taking algorithm as "auto" and moving on...')
                else:
                    print(colored('\n \033[1m An inappropriate non-integer element in n_neighbors list at location ' +
                                  str(i) + '! PLEASE CHECK!!!', 'red'))
                    pass

        else:
            print(colored('\n \033[1m Inappropriate integer or a list of integers entered for n_neighbors!', 'red'))
            print('Taking n_neighbors as 5 and moving on...')

        self.output = knn_score

    def __repr__(self):
        return str(self.output)
