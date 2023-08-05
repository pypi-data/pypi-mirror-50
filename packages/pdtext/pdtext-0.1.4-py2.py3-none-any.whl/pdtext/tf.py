#!/usr/bin/env python
# coding: utf-8

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd
from string import punctuation

def word_count(text, include_numbers = True):

    '''Count number of words in a string.
    text = string to count.
    include_numbers = Boolean on whether to include numbers as words.
    '''

    if include_numbers == True:
        return sum([len(w.strip(punctuation))>0 for w in text.split()])
    else:
        return sum([w.strip(punctuation).isalpha() for w in text.split()])



def make_wf_df(text_column, summary=False, melt=False, tfidf = False, **kwargs):
    if tfidf == True:
        vectorizer = TfidfVectorizer(**kwargs, token_pattern=r"(?u)\b\w+\b")
    else:
        vectorizer = CountVectorizer(**kwargs, token_pattern=r"(?u)\b\w+\b")

    wf = vectorizer.fit_transform(text_column)

    if type(text_column) == pd.core.series.Series:
        index_column = text_column.index
    else:
        index_column = range(0,len(text_column))

    word_freq_df = pd.DataFrame(
        wf.toarray(), columns=vectorizer.get_feature_names(), index = index_column
    )

    if summary == True:
         word_freq_df.sum().sort_values(ascending=False)


    if melt == true:
        return pd.melt(word_freq_df)

    return word_freq_df


# In[ ]:
