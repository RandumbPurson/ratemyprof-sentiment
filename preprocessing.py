import numpy as np
import string
import collections

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk

def stem_comments(text):
    stemmer = PorterStemmer()
    stemmed_words = []

    for comment in text:
        words = word_tokenize(str(comment))
        
        for word in words:
            if word in string.punctuation:
                continue
            stemmed_words.append(stemmer.stem(word)) 

    return np.array(stemmed_words)

def top_n_stem_words(text, n):
    stem_words = stem_comments(text)
    freq = collections.Counter(stem_words)
    
    return freq.most_common(n)