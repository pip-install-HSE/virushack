import word2vec
from config import *
word2vec.word2phrase(filename_start, filename_phrases, verbose=True)
word2vec.word2vec(filename_phrases, filename_bin, size=100, verbose=True)
word2vec.word2clusters(filename_start, filename_clusters, 100, verbose=True)
