import pandas as pd
import numpy as np


def topic_pred(lda_model, tf, vectorizer):

    """returns a dataframe with topic predictions."""

    # Column names based on top three topics
    # source: https://stackoverflow.com/questions/44208501/getting-topic-word-distribution-from-lda-in-scikit-learn
    vocab = vectorizer.get_feature_names()
    feature_names = []
    for topic, comp in enumerate(lda_model.components_):
        word_idx = np.argsort(comp)[::-1][:3]
        name = "_".join([vocab[i] for i in word_idx])
        feature_names.append(name)

    lda_predictions = lda_model.transform(tf)
    df = pd.DataFrame(lda_predictions, columns=feature_names)

    return df


def topic_words(lda_model, vectorizer, ntokens=10):
    """Generate  a pandas dataframe of words associated with a scikit-learn topic model.
    Keyword arguments:
    lda_model  -- fitted lda model
    vectorizer -- fitted scikit-learn vectorizer used to construct word frequencies used in the topic model.
    """

    # source: https://stackoverflow.com/questions/44208501/getting-topic-word-distribution-from-lda-in-scikit-learn
    vocab = vectorizer.get_feature_names()

    # Get most common words for each topic and store in df column
    df = pd.DataFrame()
    for topic, comp in enumerate(lda_model.components_):
        column_name = "Topic %s" % (topic + 1)

        word_idx = np.argsort(comp)[::-1][:ntokens]
        topic_words = [vocab[i] for i in word_idx]
        df[column_name] = topic_words

    # reindex so first word has a rank of 1 and return tranposed for readability
    df.index += 1
    df = df.T

    return df
