import os
from xml.dom.minidom import Notation
import requests

"""
This module is used as an interface to the RESTful API of the Linked Open Vocabularies (https://lov.linkeddata.es/dataset/lov). 

Examples:
    >>> from kgheartbeat import LOVAPI
    >>> LOVAPI.getAllVocab()

This module contains the following functions:

- `autocompleteTerm(term)` - Returns a JSON with similar terms found.
- `autocompleteVocab(vocab)` -  Returns a JSON with similar vocabularies found.
- `getAllVocab()` - Returns a list of all vocabularies included in the LOV.
- `findVocabulary(vocab)` - Check if a vocabulary is included in the LOV.
- `searchTermsList(terms)` - Search a list of terms in the LOV (for efficiency reasons it is done offline on a downloaded list of all terms available on LOV).

"""

def log_in_out(func):
    from time import perf_counter
    def decorated_func(*args, **kwargs):
        start_time = perf_counter()
        print("Doing ", func.__name__)
        result = func(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print('{0} took {1:.8f}s to execute'.format(func.__name__, execution_time))
        return result

    return decorated_func

def autocompleteTerm(term):
    """Search similar terms based on the term given as input.

    Args:
        term (string): A string that represent a term used in the KG analyzed.
    
    Returns: 
        dict: A dict that contains a list of terms similar to the term passed as input.
    """
    url = 'https://lov.linkeddata.es/dataset/lov/api/v2/term/autocomplete?q=%s'%term
    try:
        h = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(url,headers=h)
        if response.status_code == 200:
            jsonResult = response.json()
            return jsonResult
        elif response.status_code == 404:
            print('Error in running the query on LOV')
            return False 
    except:
        print('Failed to connect to Linked Open Vocabularies')
        return False

def autocompleteVocab(vocab):
    """Search similar vocabularies based on the vocabulary given as input.

    Args:
        term (string): A string that represent a vocabulary used in the KG analyzed.
    
    Returns: 
        dict: A dict that contains a list of vocabularies similar to the term passed as input.
    """
    url = 'https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/autocomplete?q=%s'%vocab
    try:
        response = requests.get(url)
        if response.status_code == 200:
            jsonResult = response.json()
            return jsonResult
        elif response.status_code == 404:
            print('Error in running the query on LOV')
            return False 
    except:
        print('Failed to connect to Linked Open Vocabularies')
        return False

def getAllVocab():
    """Search for all standard vocabularies included in the LOV.

    Returns: 
        dict: A dict that contains all vocabularies considered standard by the LOV.
    """
    url = 'https://lov.linkeddata.es/dataset/lov/api/v2/vocabulary/list'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            jsonResult = response.json()
            return jsonResult
        elif response.status_code == 404:
            print('Error in running the query on LOV')
            return False 
    except:
        print('Failed to connect to Linked Open Vocabularies')
        return False

def findVocabulary(vocab):
    """Look for a vocabulary in the LOV to see if it is considered standard or is a new defined vocabulary.

    Args:
        vocab (string): A string that represent a vocabulary used in the KG analyzed.
    
    Returns: 
        boolean: A boolean that is True if the vocabulary is in the LOV, False otherwise.
    """
    vocabularies = getAllVocab()
    for i in range(len(vocabularies)):
        d = vocabularies[i]
        nsp = d.get('nsp')
        uri = d.get('uri')
        if nsp == vocab:
            return True
        if uri == vocab:
            return True
    return False

@log_in_out
def searchTermsList(terms):
    """Look for a terms in the files with all terms downloaded form the LOV to see if it are considered standard or is a new defined terms.

    Args:
        terms (list): A list that represent all terms  used in the KG analyzed.
    
    Returns: 
        list: A list that contains all terms that aren't considered standard for the LOV.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    lov1 = os.path.join(here,'lov1.txt')
    lov2 = os.path.join(here,'lov2.txt')
    newTerms = []
    with open(lov1, 'r',encoding='utf-8') as f1:
        with open(lov2, 'r',encoding='utf-8') as f2:
            data1 = set(f1.read().splitlines())
            data2 = set(f2.read().splitlines())
            for i in range(len(terms)):
                if terms[i] not in data1 and terms[i] not in data2:
                    newTerms.append(terms[i])
    return newTerms

