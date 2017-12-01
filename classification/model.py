#!/usr/bin/env python3

import pickle

import timeit
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

from tokenizer import Tokenizer

class Model():
    def __init__(self, data_train, data_test, classifier=SGDClassifier, outpath=None):
        self.data_train = data_train
        self.data_test  = data_test
        self.classifier = classifier
        self.model = None

    @property
    def y_train(self):
        return self.data_train.target
        y_train, y_test = data_train.target, data_test.target
        labels = LabelEncoder()
        y = labels.fit_transform(y)
        return y

    @property
    def y_test(self):
        return self.data_test.target
        labels = LabelEncoder()
        y = labels.fit_transform(y)
        return y


    def identity(self):
        pass

    def build(self, X, y):
        if isinstance(self.classifier, type):
            self.classifier = self.classifier()

        model = Pipeline([
            ('preprocessor', Tokenizer()),
            ('vectorize', TfidfVectorizer(
                tokenizer=self.identity, preprocessor=None, lowercase=False
            )),
            ('classifier', self.classifier),
        ])


        model.fit(X, y)
        return model

    def run(self):
        self.train()
        self.test()

    def train(self):
        self.model = self.build(self.data_train.data, self.data_train.target)
        y_pred = self.model.predict(self.data_test.data)
        print(y_pred)

        pass

    def test(self):
        return False
        train_model = self.build(self.data_test.data, self.data_test.target)
        pass

    def persist(self):
        if not self.outpath : return False

        with open(self.outpath, 'wb') as f:
            pickle.dump(self.model, f)
            print("Model written out to {}".format(self.outpath))

from sklearn.datasets import load_files

#https://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html
#https://gist.github.com/bbengfort/044682e76def583a12e6c09209c664a1
data_train = load_files('/Users/zachariel/pdn_data/onet_dataset/train', encoding="utf8")
data_test  = load_files('/Users/zachariel/pdn_data/onet_dataset/test',  encoding="utf8")
m = Model(data_train, data_test)
print(m.run())
