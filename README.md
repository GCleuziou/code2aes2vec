# code2vec
Python modules for program embeddings computation


### Functionalities :
The code2vec module offers the following functionalities :
1. load a set of programs from a (preformated) .csv file as a Dataset 
2. analyze a Dataset by generating the ARS (Abstract Running Sequence)
3. generate a corpus of ARS (.cor file) from a pre-analyzed Dataset
4. (to publish) learn a code2vec embedding model from a corpus of ARS (.cor file)
5. (to publish) compute the embedding for a new ARS given a pre-trained model
6. (to publish) visualize the symbol or code embeddings with a 2D-projection

### Processing example :

import code2ars

#load the NewCaledonia-toyset50 (demonstration dataset) as a Dataset
d = code2ars.Dataset('datasets/NewCaledonia-toyset50.csv')
#analyse the dataset by generating the ARS
d.analysis()                                               
#generate the corpus of corresponding ARS
code2ars.dataset2corpus(d,'Datasets/Corpus/NewCaledonia-toyset50.cor')  