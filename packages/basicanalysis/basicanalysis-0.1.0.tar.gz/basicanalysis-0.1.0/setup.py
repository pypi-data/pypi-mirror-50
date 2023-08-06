#!/usr/bin/env python

from setuptools import setup

setup(
    name='basicanalysis',
    version='0.1.0',
    description='A quick way to see the best supervised learning method for your dataset or best configuration for the chosen method.',
    license='MIT',
    packages=['basicanalysis'],
    author=['Niral J Shah'],
    author_email='niraljshah@outlook.com',
    long_description=open('README.RST').read(),
    long_description_content_type='text/x-rst',
    keywords=['Basic', 'Analysis', 'Supervised', 'Learning', 'Metrics', 'KNN', 'Adaboost', 'SVM', 'Naive-Bayes',
              'Naive', 'Bayes', 'Logistic Regression', 'Logistic', 'Regression', 'Linear', 'Neural Network',
              'Cross-validation', 'validation', 'k-fold', 'n-fold', '10-fold', 'k-fold validation'],
    url='https://github.com/niraljshah/SupervisedLearningOverview'
)

