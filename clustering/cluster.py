#!/usr/bin/env python3


from __future__ import print_function

import os
from sklearn.datasets import load_files
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
# parse commandline arguments
op = OptionParser()
op.add_option("--data-source",
                      dest="source_directory", default="~/pdn_data/by_major",
                                    help="Directory containing documents to load.")
op.add_option("--lsa",
                      dest="n_components", type="int",
                                    help="Preprocess documents with latent semantic analysis.")
op.add_option("--no-minibatch",
                      action="store_false", dest="minibatch", default=True,
                                    help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
                      action="store_false", dest="use_idf", default=True,
                                    help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
                      action="store_true", default=False,
                                    help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
                      help="Maximum number of features (dimensions)"
                                         " to extract from text.")
op.add_option("--verbose",
                      action="store_true", dest="verbose", default=False,
                                    help="Print progress reports inside k-means algorithm.")

#print(__doc__)
#op.print_help()

argv = sys.argv[1:]

(opts, args) = op.parse_args(argv)

categories = [
    '11-0000',
    '13-0000',
    '15-0000',
    '17-0000',
    '19-0000',
    '21-0000',
    '25-0000',
    '27-0000',
    '29-0000',
    '31-0000',
    '33-0000',
    '35-0000',
    '37-0000',
    '47-0000',
    '39-0000',
    '49-0000',
    '23-0000',
    '41-0000',
    '43-0000',
    '45-0000',
    '51-0000',
    '53-0000'
]

bunch = load_files(os.path.expanduser(opts.source_directory), load_content=False, random_state=10, encoding="utf8")
print(bunch)
