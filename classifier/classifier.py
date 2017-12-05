#!/usr/bin/env python3

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import sys
from time import time

from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.utils.extmath import density
from sklearn import metrics

class Classifier():
    def __init__(self):
        print('__init__')


def main():
    data_train = load_files('/Users/zachariel/pdn_data/onet_dataset/train', encoding="utf8")
    data_test  = load_files('/Users/zachariel/pdn_data/onet_dataset/test', encoding="utf8")

    target_names = data_train.target_names

# split a training set and a test set
    y_train, y_test = data_train.target, data_test.target

    use_hashing = False

#if use_hashing:
#    vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False,
#                                   n_features=n_features)
#    X_train = vectorizer.transform(data_train.data)
#else:
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                 stop_words='english')
    X_train = vectorizer.fit_transform(data_train.data)

    X_test = vectorizer.transform(data_test.data)

# mapping from integer feature name to original token string
    if use_hashing:
        feature_names = None
    else:
        feature_names = vectorizer.get_feature_names()

    select_chi2 = None

    if select_chi2:
        print("Extracting %d best features by a chi-squared test" %
              select_chi2)
        t0 = time()
        ch2 = SelectKBest(chi2, k=select_chi2)
        X_train = ch2.fit_transform(X_train, y_train)
        X_test = ch2.transform(X_test)
        if feature_names:
            # keep selected feature names
            feature_names = [feature_names[i] for i
                             in ch2.get_support(indices=True)]
        print("done in %fs" % (time() - t0))
        print()

    if feature_names:
        feature_names = np.asarray(feature_names)
    def trim(s):
        """Trim string to fit on terminal (assuming 80-column display)"""
        return s if len(s) <= 80 else s[:77] + "..."

# #############################################################################
# Benchmark classifiers
    print_top10 = True
    print_report = True
    print_cm     = False
    def benchmark(clf):
        print('_' * 80)
        print("Training: ")
        print(clf)
        t0 = time()
        clf.fit(X_train, y_train)
        train_time = time() - t0
        print("train time: %0.3fs" % train_time)

        t0 = time()
        pred = clf.predict(X_test)
        test_time = time() - t0
        print("test time:  %0.3fs" % test_time)

        score = metrics.accuracy_score(y_test, pred)
        print("accuracy:   %0.3f" % score)

        if hasattr(clf, 'coef_'):
            print("dimensionality: %d" % clf.coef_.shape[1])
            print("density: %f" % density(clf.coef_))

            if print_top10 and feature_names is not None:
                print("top 10 keywords per class:")
                for i, label in enumerate(target_names):
                    top10 = np.argsort(clf.coef_[i])[-10:]
                    print(trim("%s: %s" % (label, " ".join(feature_names[top10]))))
            print()

        if print_report:
            print("classification report:")
            print(metrics.classification_report(y_test, pred,
                                                target_names=target_names))

        if print_cm:
            print("confusion matrix:")
            print(metrics.confusion_matrix(y_test, pred))

        print()
        clf_descr = str(clf).split('(')[0]
        return clf_descr, score, train_time, test_time


    penalty = 'l1'
    benchmark(LinearSVC(penalty=penalty, dual=False, tol=1e-3))
