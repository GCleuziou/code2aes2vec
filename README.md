# code2ars2vec
Python modules for program embeddings computation using the code2ars2vec method presented in [Cleuziou&Flouvat,2021].

### Functionalities :
The code2ars2vec modules offer the following functionalities :
1. load a set of student programs from a (preformated) .json file as 'Attempt Dataset' 
2. load a set of exercises from a (preformated) .json file as 'Exercise Dataset'
2. generate the ARS (Abstract Running Sequence) of a student program by analyzing program execution traces on a set of test cases
4. train an embedding model from a training dataset of ARS
5. infer embeddings of new ARS given a pre-trained model

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
Generate the ARS of the first student program :
```sh
>>> from code2ars import Code2Ars
>>> ars = Code2Ars(NC1014[0],NCExercises)
```
Use the pre-computed ARS and train an embedding model on the training set :
```sh
>>> from ars2vec import learnModel, inferVectors
>>> model = learnModel(NC1014)
```
Infer the embeddings of the test set given the trained model :
```sh
>>> results = inferVectors(model, NC1014)
```

### Citation :

Please cite the following reference when using the code2ars2vec modules :

```sh
@inproceedings{cleuziou2021code2ars2vec,
  author    = {Cleuziou, Guillaume and Flouvat, Fr{\'{e}}d{\'{e}}ric},
  editor    = {},
  title     = {Apprentissage d'embeddings de codes pour l'enseignement de la programmation : une approche fond{\'{e}}e sur l'analyse des traces d'ex{\'{e}}cution},
  booktitle = {21{\`{e}}me conf{\'{e}}rence Extraction et Gestion des Connaissances,{EGC} 2021, Montpellier, France, January 25-29, 2021},
  series    = {{RNTI}},
  volume    = {},
  pages     = {(to appear)},
  publisher = {{\'{E}}ditions {RNTI}},
  year      = {2021}
  }
```
