# code2vec
Python modules for program embeddings computation


### Functionalities :
The code2vec module offers the following functionalities :
1. load a set of programs from a (preformated) .csv file as a Dataset 
2. analyze a Dataset by generating the ARS (Abstract Running Sequence)
3. generate a corpus of ARS (.cor file) from a pre-analyzed Dataset
4. learn a code2vec embedding model from a corpus of ARS (.cor file)
5. compute the embedding for a new ARS given a pre-trained model
6. visualize the token's or program's embeddings with a 2D-projection

### Processing example :

>`import code2ars`

#load the NewCaledonia-toyset50 (demonstration dataset) as a Dataset

>`d = code2ars.Dataset('Datasets/NewCaledonia-toyset50.csv')`

#analyse the dataset by generating the ARS

>`d.analysis()`

#generate the corpus of corresponding ARS

>`code2ars.dataset2corpus(d,'Datasets/Corpus/NewCaledonia-toyset50.cor')`

>`import code2vec``

#learn an embedding model from the corpus of ARS built breviously

>`model = code2vec.learnModel('Datasets/Corpus/NewCaledonia-toyset50.cor')`

#visualize a 2D-projection of the learned token's embeddings

>`code2vec.visuEmbedingstSNE(model, type='token')`
 
 #visualize a 2D-projection of the learned program's embeddings

 >`code2vec.visuEmbedingstSNE(model, type='code')`

 #infer the embeddings of new programs using the learned model (on this example we re-used the training corpus as corpus of 'new programs')

 >`results = code2vec.inferVectors(model,'Datasets/Corpus/NewCaledonia-toyset50.cor')`