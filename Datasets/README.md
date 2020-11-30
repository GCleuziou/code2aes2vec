# Datasets presentation
Pre-processed datasets for program embedding construction with the code2ars2vec method.

| Datasets |
| ------ |
| [NewCaledonia Exercises][NCEx]|
| [NewCaledonia Attempts 1,014][NC1014]|
| [NewCaledonia Attempts 5,690][NC5690]|
| [Dublin Exercises][DBEx]|
| [Dublin Attempts 42487][DB42487]|

  [NCEx]: <https://github.com/GCleuziou/code2ars2vec/blob/master/Datasets/NewCaledonia_exercises.json>
  [NC1014]: <https://github.com/GCleuziou/code2ars2vec/blob/master/Datasets/NewCaledonia_1014.json>
  [NC5690]: <https://www.dropbox.com/s/uteg76p1a8bolhe/newcaledonia_5690.json?dl=0>
  [DBEx]: <https://github.com/GCleuziou/code2ars2vec/blob/master/Datasets/Dublin_exercises.json>
  [DB42487]: <https://www.dropbox.com/s/9vc90ns7gwsci9o/dublin_42487.json?dl=0>
  
### NewCaledonia Dataset :
The NewCaledonia dataset includes the programs submitted in 2020 by a group of 60 students from the University of New Caledonia, on a programming training platform. This plateform were developed and made available by the Computer Science department from the Orléans' Technological Institute (University of Orléans, France).

The full dataset (NewCaledonia_5690) includes 5,690 short python programs from beginner programming students over 66 exercises.

NewCaledonia_1014 is a selection of the New Caledonia datasets containing only the (1,1014) programs submitted over 8 selected exercices.

### Dublin Dataset :

The Dublin dataset is a subset of the [Azcona&Smeaton's Dataset](https://figshare.com/articles/dataset/_5_Million_Python_Bash_Programming_Submissions_for_5_Courses_Grades_for_Computer-Based_Exams_over_3_academic_years_/12610958). It includes student programs from the University of Dublin, carried out between 2016 and 2019. Although the original corpus, made available in July 2020, contains nearly 600,000 programs (Python and Bash), we propose here an enriched subset of 42,487 programs. 

### Format :

For each dataset, two JSON files are available :

 - Dataset.json (ex. NewCaledonia_1014.json) : a Python list in which each element is a dictionary defining a student attempt (program submitted on the programming plateform) using the following fields (dictionary keys) :
   - exercise_name : corresponding exercise (frequently used as class label for an attempt)
   - extension : indicating the programming language (ex. 'py'  for Python programs)
   - date : the date and time the program has been submitted on the plateform
   - correct : indicating whether the plateform evaluated the attempt as correct or not
   - upload : the submitted script
   - user : the student identifier
   - eval_set : indicating to which evaluation set the attempt belongs, given a pre-division of the dataset into three sets (training - 90%, validation - 5%, test - 5%)
   - ars0, ars1, ars2 : each field containing an Abstract Running Sequence (ARS) obtained by analyzing program execution traces on a set of test cases (three levels of abstraction)
 

 - Dataset_exercises.json (ex. NewCaledonia_exercises.json) : a Python list in which each element is a dictionary defining an exercise on the plateform using (at least) the following fields (dictionary keys) :
   - solution : the exercise solution provided by the teacher (when available)
   - funcname : the name of the function the student has to write
   - entries : a list of testcase (usefull for either evaluation or ARS construction)
   - exo_name : identifying the exercise

### Citation :

Please cite the following reference when using one of these pre-processed datasets :

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
