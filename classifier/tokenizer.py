#!/usr/bin/env python3

import string

import Stemmer
from nltk.corpus import stopwords as sw
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag
from nltk import wordpunct_tokenize
from nltk.corpus import wordnet as wn

from sklearn.base import BaseEstimator, TransformerMixin

class MyStemmer(Stemmer.Stemmer):
    def __init__(self, language):
        super().__init__(language)

    def stem(self, word):
        return self.stemWord(word)

class Tokenizer(BaseEstimator, TransformerMixin):
    """Tokenizer for text document

    Tokenizer used to preprocess documents, it will lowercase, remove stopwords
    and puctuation characters, also will steam.

    Parameters
    -----------
    stopwords : list, optional
        List of stop words to be used, defaults to nltk english stopwords.
    punct : list, optional
        List of punctuation characters, defaults to nltk punct chars.
    lower : boolean, optional
        If True, will lowercase all characters in document.
    stemmer : Stemmer, optional
        If provided will stem tokens with it.
    strip : boolean, optional
        If True, will strip tokens.
    """
    def __init__(self, stopwords=None, punct=None, lower=True, strip=True, stemmer= None):
        self.lower      = lower
        self.strip      = strip
        self.stopwords  = stopwords or set(sw.words('english'))
        self.punct      = punct or set(string.punctuation)
        self.stemmer    = stemmer
        self.lemmatizer = WordNetLemmatizer()

    def tokenize(self, document):
        # Break document into sentences
        for sentence in sent_tokenize(document):
            # Break sentence into part of speech tagged tokens
            for token, tag in pos_tag( wordpunct_tokenize(sentence) ):
                # Preprocess token
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token

                # Ignore stopwords
                if token in self.stopwords:
                    continue

                # Skip punctuations
                if all(char in self.punct for char in token):
                    continue

                # Steam token
                token = self.stemmer.stem(token) if self.stemmer else token

                # Lemmatize token and yield
                lemma = self.lemmatize(token, tag)
                yield lemma

    def lemmatize(self, token, tag):
        tag = {
                'N': wn.NOUN,
                'V': wn.VERB,
                'R': wn.ADV,
                'J': wn.ADJ
        }.get(tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)

    def fit(self, X, y=None):
        """ Transformer interface method implementation """
        return self

    def inverse_transform(self, X):
        """ Transformer interface method implementation """
        return [" ".join(doc) for doc in X]

    def transform(self, X):
        """ Transformer interface method implementation. Takes a list of documents (X)
            and returns a new list of tokenized documents, where each document is
            transformed into list of ordered tokens.

        Parameters
        ----------
        X : list
            List of documents to transforma.

        Returns
        -------
        params : array of tokens per document
        """
        return [
            list(self.tokenize(doc)) for doc in X
        ]
    pass

def main():
    from sklearn.datasets import load_files
    data_train = load_files('/Users/zachariel/pdn_data/onet_dataset/train', encoding="utf8")
    tokenizer = Tokenizer()
    document = data_train.data[0]
    print(tokenizer.transform([document]))

#if __name__ == "__main__" : main()
