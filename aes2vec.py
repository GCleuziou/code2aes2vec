#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import gensim, re, smart_open

def data2cor(data,outputfile,selectionfield='eval_set',selectionsets=['training'],valuefield='aes2'):
    """build a corpus of descriptions (typically AES) from the full or a selected part of the dataset
    - data           : the dataset containing learners' attempts
    - outputfile     : the .cor file to generate
    - selectionfield : (default 'eval_set') a field (key) in data to serve as filter
    - selectionsets  : (default ['training']) values to consider in the filter
    - valuefield     : (default 'aes2') the filed (key) that contains the attempt's desription to report in the corpus        
    """
    with open(outputfile,'w') as f:
        for att in data:
            if att[selectionfield] in selectionsets :
                f.write(att[valuefield]+'\n')

def read_corpus(fname, tokens_only=False):
    """transforms a 'corpus' (one 'document' per line) as a sequence of tokens
    considering alphanumeric characters
    """
    with smart_open.open(fname, encoding="iso-8859-1") as f:
        for i, line in enumerate(f):
            line = line.replace('\n',' ')
            tokens = re.compile(' +').split(line)
            tokens = [t for t in tokens if t!='']
            if tokens_only:
                yield tokens
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

# Final functions =================================================================================

def learnModel(data, selectionfield='eval_set', selectionsets=['training'], valuefield='aes2', vsize=100, cwindow=5, niter=500):
    """learn an 'aes2vec' model from the full or a selected part of the dataset
    - data           : the dataset containing learners' attempts
    - selectionfield : (default 'eval_set') a field (key) in data to serve as filter
    - selectionsets  : (default ['training']) values to consider in the filter
    - valuefield     : (default 'aes2') the filed (key) that contains the attempt's desription to report in the corpus        
    - vsize          : (default 100) dimension of expected embeddings
    - cwindow        : (default 5) size of the context window : nb tokens before/after the token to predict
    - niter          : (default 500) nb. epochs for the learning process
    The resulting model is in Doc2Vec form. 
    """
    corpus = 'utils/train.cor'
    data2cor(data,corpus,selectionfield,selectionsets,valuefield)
    train_corpus = list(read_corpus(corpus))
    model = gensim.models.doc2vec.Doc2Vec(vector_size=vsize, min_count=2, epochs=niter, window=cwindow)
    model.build_vocab(train_corpus)
    model.train(train_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    return model

def inferVectors(model, data, selectionfield='eval_set', selectionsets=['test'], valuefield='aes2'):
    """Infer new embedding vectors of full or a selected part of the dataset given a pre-trained model
    - model          : the pre-trained model (typically obtaind by learnModel())
    - data           : the dataset containing learners' attempts
    - selectionfield : (default 'eval_set') a field (key) in data to serve as filter
    - selectionsets  : (default ['test']) values to consider in the filter
    """
    corpus = 'utils/test.cor'
    data2cor(data,corpus,selectionfield,selectionsets,valuefield)
    test_corpus = list(read_corpus(corpus, tokens_only=True))
    res=[]
    for doc_id in range(len(test_corpus)):
        res.append(model.infer_vector(test_corpus[doc_id]))
    return res
