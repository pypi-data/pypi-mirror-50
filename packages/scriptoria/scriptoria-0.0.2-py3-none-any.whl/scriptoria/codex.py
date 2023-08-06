#!/usr/bin/env python

import os
import tempfile
import nltk; nltk.download('stopwords')
from nltk.corpus import stopwords
from gensim.corpora import Dictionary


stopset = set(stopwords.words('english'))


class Medusa(object):

    def __init__(self, soul):
        self.soul = soul

    def gaze(self, dictionary):
        
        laughter = {
            'positions': dct.num_pos,
            'documents' : dct.num_docs,
            'collectionfrequency' : dct.cfs,
            'documentfrequency': dct.dfs
        }

        return laughter

                    
class BookBinder(object):

    def __init__(self, recordpath):

        self.recordpath = recordpath

    def __next__(self):

        with open(self.recordpath, 'r') as record:

            for letters in record.readlines():

                yield letters.strip('\n')


def dialogues2records(dialogues, stopset):
    """
    A record is a tokenized turn and records is a list of all turns.
    Gensim's `Dictionary` module expects an `iterable of iterable of str`.
    To keep multiturns intact use `Dictionary.add_documents(dialogue)` instead
    of Dictionary(turns).  
    """
    records = []

    for dialogue in dialogues:

        for turn in dialogue:

            for words in turn:

                lessfrequent = list(filter(lambda w : w not in stopset, turn.lower().split()))

                records.append([word for word in lessfrequent])

    return records


def binder2dictionary(bookbinder, stopset, dialogue_count=10000, dictionarypath="dictionarypath"):
    """Lazy load multiturns, transform into turns only, create dictionary."""

    dialogues = [multiturn.split('__eou__')[:-1] for multiturn in list(iter(next(bookbinder)))[:dialogue_count]]
    
    records = dialogues2records(dialogues, stopset)                  
    
    dictionary = Dictionary(records)   
    
    dictionary.filter_extremes(no_below=2, no_above=0.5, keep_n=25000)
    
    dictionary._smart_save(dictionarypath)
    
    return dictionary


def corpus2tsv(filename):

    pass


def corpus2csv(pathname):

    tmp = tempfile.gettempdir()

    dataframe.to_csv(os.path.join(tmp, 'dialogues.csv'))


def corpus2pickle(dataframe):

    tmp = tempfile.gettempdir()

    dataframe.to_pickle(os.path.join(tmp, 'dialogues.pickle'))