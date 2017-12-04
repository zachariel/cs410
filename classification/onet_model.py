#!/usr/bin/env python3

import pickle
import os

from sklearn.datasets import load_files
from nltk.stem.snowball import SnowballStemmer

from time import time
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

from sklearn.datasets import load_files

from .tokenizer import Tokenizer

__all__ = ['OnetModel']

class OnetModel():
    def __init__(self):
        self.tokenizer  = Tokenizer()
        self.data_train = None
        self.data_test  = None
        self.classifier = None
        self.outpath    = None
        self.model      = None
        self.model2     = None
        self.stemmer    = True

    @property
    def target_names(self):
        if not self.data_train: return []
        return self.data_train.target_names

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


    def identity(self, arg):
        return arg

    def run(self, data_train, data_test, classifier=None, stemmer=None):
        if not classifier:
            self.classifier = LinearSVC(penalty='l1', dual=False, tol=1e-3)

        self.data_train = data_train
        self.data_test  = data_test
        self.model = classifier
        self.stemmer = stemmer

        self.train()
        self.test()
        return self

    def train(self):
        print('=' * 80)
        print("Training: ")
        print('_' * 80)
        #vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
        #                             stop_words='english')
        #X_vectorized = vectorizer.fit_transform(X)

        print(self.model)
        t0 = time()
        self.model.fit(self.data_train.data, self.data_train.target)
        self.model.labels_ = self.data_train.target_names
        train_time = time() - t0
        print("train time: %0.3fs" % train_time)

        return self

    def test(self):
        t0 = time()
        y_pred = self.model.predict(self.data_test.data)
        test_time = time() - t0
        print("test time:  %0.3fs" % test_time)

        score = metrics.accuracy_score(self.data_test.target, y_pred)
        print("accuracy:   %0.3f" % score)

        if hasattr(self.model, 'coef_'):
            print("dimensionality: %d" % self.model.coef_.shape[1])
            print("density: %f" % density(self.model.coef_))

            print("top 10 keywords per class:")
            for i, label in enumerate(self.data_train.target_names):
                top10 = np.argsort(self.model.coef_[i])[-10:]
                print(trim("%s: %s" % (label, " ".join(feature_names[top10]))))

        print("classification report:")
        print(metrics.classification_report(self.data_test.target, y_pred,
                                            target_names=self.data_train.target_names))

        return self

    def persist(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
            print("Model written out to {}".format(path))

    def restore(self, path):
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        return self

    def predict(self, documents):
        if not self.model: return None

        results = []
        predictions = self.model.predict(documents)
        for prediction in predictions:
            results.append(self.target_names[prediction])

        return results

    @classmethod
    def load(cls, path):
        classifier = cls().restore(path)
        return classifier



##https://bbengfort.github.io/tutorials/2016/05/19/text-classification-nltk-sckit-learn.html
##https://gist.github.com/bbengfort/044682e76def583a12e6c09209c664a1

def identity(args):
    return args

def load_data():
    data_train = load_files('/Users/zachariel/pdn_data/onet_dataset/train', encoding="utf8")
    data_test  = load_files('/Users/zachariel/pdn_data/onet_dataset/test',  encoding="utf8")

    return (data_train, data_test)

def main():
    base_dir = os.path.dirname(__file__) + "/models/"

    data_train, data_test = load_data()

    snowball = SnowballStemmer("english")

    model = Pipeline([
        ('vectorize', Tokenizer(stemmer=snowball)),
        ('tfidf', TfidfVectorizer(
            tokenizer=identity, preprocessor=None, lowercase=False
        )),
        ('clf', classifier),
    ])


    classifier = LinearSVC(penalty='l1', dual=False, tol=1e-3)
    classifier = LinearSVC()
    svc = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english') ),
        ('clf', classifier),
    ])

    params = {'tfidf__ngram_range': [(1,1), (1,2)],
            'clf__loss': ['hinge', 'squared_hinge'],
            'clf__dual': [True, False],
            'clf__tol': [1e-2, 1e-3, 1e-4],
            }

    gs_svc = GridSearchCV(svc, params, n_jobs=-1)
    gs_svc = gs_svc.fit(data_train.data, data_train.target)

    pams2 = {'tfidf__ngram_range': [(1,1), (1,2)],
            'tfidf__norm': [None, 'l1', 'l2'],
            'clf__alpha': (1e-2, 1e-3),
            }

    # model2 == model3
    #model3 = Pipeline([('vect', CountVectorizer(stop_words='english')),
    #                    ('tfidf', TfidfTransformer()),
    #                    ('clf', MultinomialNB())
    #])

    m = OnetModel()
    m.run(data_train, data_test, classifier=model)
    #file_name= os.path.join(base_dir, str(id(m)) + ".model")
    #m.persist(file_name)

    m2 = OnetModel()
    m2.run(data_train, data_test, classifier=model2)
    #file_name= os.path.join(base_dir, str(id(m)) + ".model")
    #m.persist(file_name)

    m3 = OnetModel()
    m2.run(data_train, data_test, classifier=model3)


if __name__ == '__main__' : main()
