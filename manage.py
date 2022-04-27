#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import json

def json2data(filename):
    """ loads a json file into a list (of dictionaries) """
    with open(filename,'r') as json_file:
        data = json.load(json_file)
    return data

def list2dic(data,field):
    """organize a list of dictionnaries as a dictionnary of dictionnaries using *field* as (unique) key"""
    dico ={}
    for elem in data:
        if elem[field] in dico.keys():
            print('Field',field,'cannont be used as key (not unique)')
            return None
        dico[elem[field]] = elem
    return dico

# Final functions =================================================================================

def jsonAttempts2data(filename):
    """ loads a dataset containing learner's attempts from a .json file to a list """
    return json2data(filename)

def jsonExercises2data(filename, field='exo_name'):
    """ loads a dataset containing exercises from a .json file to a dictionary """
    data = json2data(filename)
    for item in data:
        entries = []
        for entry in item['entries']:
            if isinstance(entry, dict) and 'items' in entry.keys():
                entries.append(tuple(entry['items']))
            else :
                entries.append(entry)
        item['entries'] = entries
    return list2dic(data,field)

