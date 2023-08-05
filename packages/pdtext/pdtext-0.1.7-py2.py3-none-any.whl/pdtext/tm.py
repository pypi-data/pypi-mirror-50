import pandas as pd

def extract_features(w):
    features = w.feats
    fd = {}
    if '|' not in features:
        return fd
    else:
        for f in features.split('|'):
            fs = f.split('=')
            fd[fs[0]] = fs[1]
    return fd


def extract_word(w, properties):
    l = {p:getattr(w,p) for p in properties}
    l.update(extract_features(w))
    return l

def extract_sentence(doc_s, properties):
    l = [extract_word(w, properties) for w in doc_s.words]
    df = pd.DataFrame(l)
    df.rename(columns = {'index' : 'sent_index'}, inplace=True)
    return df


def doc_2_df(nlp_doc):
    properties = ['index', 'text', 'lemma', 'pos', 'governor',  'upos', 'xpos']

    dfs = []
    for i,s in enumerate(nlp_doc.sentences):
        sdf = extract_sentence(s, properties)
        sdf['sentence'] = i
        dfs.append(sdf)

    df = pd.concat(dfs, sort=False)

    keys = df.keys()
    bonus = ['sentence', 'sent_index']
    extra = [k for k in keys if k not in properties + bonus]
    new_keys = bonus + properties[1:] + extra

    return df[new_keys].reset_index(drop=True)


def nlp_col_2_df(series):
    s = series.apply(doc_2_df)
    dfs = []
    for index, value in s.items():
        value['col_index'] = index
        dfs.append(value)

    df = pd.concat(dfs , sort=False)
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('col_index')))
    df = df.reindex(columns= cols)
    return df

def lemmatize(text):
    doc = nlp(text)

    lemma_text = []
    for s in doc.sentences:
        ns = ' '.join([w.lemma for w in s.words if w.upos != 'PUNCT'])
        lemma_text.append(ns.lower())


    return ' '.join(lemma_text)
