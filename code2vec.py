#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import gensim, re, smart_open
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

def read_corpus(fname, tokens_only=False):
    """transforms a 'corpus' (one 'document' per line) as a sequence of tokens
    considering alphanumeric characters
    """
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            #tokens = gensim.utils.simple_preprocess(line)
            line = line.replace('\n',' ')
            tokens = re.compile(' +').split(line)
            tokens = [t for t in tokens if t!='']
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

def learnModel(corpus, vsize=20, cwindow=5, niter=200):
    """learn a 'doc2vec' model from a training 'corpus'
    """
    train_corpus = list(read_corpus(corpus))
    model = gensim.models.doc2vec.Doc2Vec(vector_size=vsize, min_count=2, epochs=niter, window=cwindow)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    return model

def inferVectors(model, corpus):
    """Infer new embedding vectors from a model given a 'test_corpus' with one test 'document' per line
    """
    test_corpus = list(read_corpus(corpus, tokens_only=True))
    res=[]
    for doc_id in range(len(test_corpus)):
        res.append(model.infer_vector(test_corpus[doc_id]))
    return res

def visuEmbedingstSNE(model, type = 'token', lab=None, title=''):
    """plot a 2D-visualization of the token/code embeddings with the t-SNE projection method
        Parameters are :
        - model : the trained code2vec model
        - type : 'token' to vosualize 'tokens' (default value) / 'code' to visualize programs
        - lab (optional) : list of labels
        - title : the title of the plot
    """
    if type=='token':
        Embed = model.wv.vectors
    elif type=='code':
        Embed = model.docvecs.vectors_docs
    else :
        Embed = model
    df = pd.DataFrame(Embed)
    df = StandardScaler().fit_transform(df)
    df=pd.DataFrame(df)
    tsne = TSNE(random_state=0)
    tsne_results = tsne.fit_transform(df)
    tsne_results=pd.DataFrame(tsne_results, columns=['tsne1', 'tsne2'])
    x,y=tsne_results['tsne1'],tsne_results['tsne2']
    plt.scatter(x, y, c=lab)
    plt.title(title)
    if type=='token':
        eps=(max(y)-min(y))*0.03
        vocab = model.wv.index2word
        for i in range(len(vocab)):
            plt.text(x[i],y[i]+eps,vocab[i],horizontalalignment='center',verticalalignment='center')
    plt.show()

