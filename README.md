# code2aes2vec
Python modules for program embeddings computation using the code2aes2vec method presented in [Cleuziou&Flouvat,2021].

### Functionalities :
The code2aes2vec modules offer the following functionalities :
1. load a set of student programs from a (preformated) .json file as 'Attempt Dataset' 
2. load a set of exercises from a (preformated) .json file as 'Exercise Dataset'
2. generate the AES (Abstract Execution Sequence) of a student program by analyzing program execution traces on a set of test cases
4. train an embedding model from a training dataset of AES
5. infer embeddings of new AES given a pre-trained model

### Processing example on the NewCaledonia_1014 dataset:
Load the NewCaledonia_1014 (Attempt) dataset :
```sh
>>> from manage import jsonAttempts2data, jsonExercises2data
>>> NC1014 = jsonAttempts2data('Datasets/NewCaledonia_1014.json')
```
Load the NewCaledonia (Exercise) dataset :
```sh
>>> NCExercises = jsonExercises2data('Datasets/NewCaledonia_exercises.json')
```
Generate the AES of the first student program :
```sh
>>> from code2aes import Code2Aes
>>> aes = Code2Aes(NC1014[0],NCExercises)
```
Use the pre-computed AES and train an embedding model on the training set :
```sh
>>> from aes2vec import learnModel, inferVectors
>>> model = learnModel(NC1014)
```
Infer the embeddings of the test set given the trained model :
```sh
>>> results = inferVectors(model, NC1014)
```

### Citation :

Please cite the following reference when using the code2aes2vec modules :

```sh
@inproceedings{DBLP:conf/edm/CleuziouF21,
  author    = {Guillaume Cleuziou and
               Fr{\'{e}}d{\'{e}}ric Flouvat},
  editor    = {Sharon I{-}Han Hsiao and
               Shaghayegh (Sherry) Sahebi and
               Fran{\c{c}}ois Bouchet and
               Jill{-}J{\^{e}}nn Vie},
  title     = {Learning student program embeddings using abstract execution traces},
  booktitle = {Proceedings of the 14th International Conference on Educational Data
               Mining, {EDM} 2021, virtual, June 29 - July 2, 2021},
  publisher = {International Educational Data Mining Society},
  year      = {2021},
  timestamp = {Wed, 09 Mar 2022 16:47:22 +0100},
  biburl    = {https://dblp.org/rec/conf/edm/CleuziouF21.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
