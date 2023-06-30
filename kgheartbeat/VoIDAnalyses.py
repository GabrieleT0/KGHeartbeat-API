import datetime
import re
from rdflib import DCAT, Graph, URIRef
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD

"""
This module expose some functions that help to parse the VoID file of a KG . 

Examples:
    >>> from kgheartbeat import VoIDAnalyses
    >>> VoIDAnalyses.parseVoIDTtl('https://raw.githubusercontent.com/frmichel/taxref-ld/master/dataset/Taxrefld_static_dataset_description.ttl')

This module contains the following functions:

- `parseVoID(url)` - Returns a Graph object which contains data in the form of subject,predicate and object.
- `parseVoIDTtl(url)` -  Returns a Graph object which contains data in the form of subject,predicate and object (this function is specific for void file with ttl extension).
- `printVoID(url)` - Print the content of a VoID file.
- `getVocabularies(graph)` - Find and return the triples with vocabulary predicate.
- `getCreationDate(graph)` - Find and return the creation date, if is indicated.
- `getCreationDate(graph)` - Find and return the modification date, if is indicated. 
- `getDataDump(graph)` - Find and return the link with KG dump.
- `getLicense(graph)` - Find and return the Machine-redeable license.
- `getCreators(graph)` - Find and return the KG creator.
- `getPublishers(graph)` - Find and return the KG publishers.
- `getContributors(graph)` - Find and return the KG contributors.
- `getNumEntities(graph)` - Find and return the number of entitie.
- `getFrequency(graph)` - Find and return the frequency update, if is indicated.
- `getUriRegex(graph)` - Find and return the URI regex.
- `getSerializationFormats(graph)` - Find and return the serialization formats available for the KG.
- `getLanguage(graph)` - Find and return the languages supported by the KG.

"""

def parseVoID(url):
    """Parse the file VoID from an url and convert triples in a Graph object.
    
    Args:
        url (string): A string that represent a url of a VoID file available on Internet.
    
    Returns:
        Graph: A Graph object that contain all the triples in the VoID file.
    """
    g = Graph()
    g.parse(url)
    return g

def parseVoIDTtl(url):
    """Parse the file VoID with the .ttl extension from an url and convert triples in a Graph object.
    
    Args:
        url (string): A string that represent a url of a VoID file available on Internet.
    
    Returns:
        Graph: A Graph object that contain all the triples in the VoID file.
    """
    g = Graph()
    g.parse(url,format='ttl')
    return g

def printVoID(graph):
    """Print all the triples in the VoID file parsed.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.
    
    """
    for s,p,o in graph:
        print(s,p,o)

def getVocabularies(graph):
    """Find triples with a predicate that indicate the vocabulary used in the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.

    Returns:
        list: A list with all vocabularies used by the KG.
    """
    vocabularies = []
    for s, p, o in graph:
        if p == VOID.vocabulary:
            o = str(o)
            vocabularies.append(o)
    newVocabularies = []
    [newVocabularies.append(x) for x in vocabularies if x not in newVocabularies] #DUPLICATE REMOVAL IF PRESENT
    return(newVocabularies)

def getCreationDate(graph):
    """Find triples with a predicate that indicate the KG creation date.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.

    Returns:
        Date: A Date object that represent the KG creation date.
    """
    date = []
    for s,p,o in graph:
        if p == DCTERMS.created or DCTERMS.issued:
            o = str(o)
            match = re.search(r'\d{4}-\d{2}-\d{2}', o)
            if match is not None:
                o = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                date.append(o)
    if len(date) > 0:       
        return min(date)
    else:
        return 'absent'

def getModificationDate(graph):
    """Find triples with a predicate that indicate the KG last modification date.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.

    Returns:
        Date: A Date object that represent the KG creation date.
    """
    date = []
    for s,p,o in graph:
        if p == DCTERMS.modified:
            o = str(o)
            match = re.search(r'\d{4}-\d{2}-\d{2}', o)
            if match is not None:
                o = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                date.append(o)
    if len(date) > 0:       
        return max(date)
    else:
        return 'absent'

def getDataDump(graph):
    """Find triples which contain the url of the KG dump file.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent a link to the KG dump
    """
    for s,p,o in graph:
        if p == VOID.dataDump:
            o = str(o)
            return o
    return 'absent'

def getLicense(graph):
    """Find triples which contain the license of the KG (machine-redeable).
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent the machine-redeable license of a KG.
    """
    for s,p,o in graph:
        if p == DCTERMS.license:
            o = str(o)
            return o
    return 'absent'

def getCreators(graph):
    """Find triples which contain the creators of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the creators (or the creator) of the KG.
    """
    creators = []
    for s,p,o in graph:
        if p == DCTERMS.creator or DC.creator:
            o = str(o)
            creators.append(o)
    if len(creators) > 0:       
        return creators
    else:
        return 'absent'

def getPublishers(graph):
    """Find triples which contain the publichers of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the publishers (or the publicher) of the KG.
    """
    publishers = []
    for s,p,o in graph:
        if p == DCTERMS.publisher or p == DC.publisher:
            o = str(o)
            publishers.append(o)
    if len(publishers) > 0:       
        return publishers
    else:
        return 'absent'

def getContributors(graph):
    """Find triples which contain the contributors of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the contributors (or the contributor) of the KG.
    """
    contributors = []
    for s,p,o in graph:
        if p == DCTERMS.contributor or p == DC.contributor:
            o = str(o)
            contributors.append(o)
    if len(contributors) > 0:       
        return contributors
    else:
        return 'absent'

def getNumEntities(graph):
    """Find triples which contain the number of entities of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent the number of entities in the KG.
    """
    for s,p,o in graph:
        if p == VOID.entities:
            o = str(o)
            if o != '':       
                return o
            else:
                return 'absent'
    return 'information abaout entities absent'

def getFrequency(graph):
    """Find triples which contain the frequency update of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent the frequency update of the KG.
    """
    for s,p,o in graph:
        if p == DCTERMS.Frequency or p == DCTERMS.accrualPeriodicity:
            o = str(o)
            if o != '':       
                return o
            
    return 'absent'

def getUriRegex(graph):
    """Find triples which contain the regex of URI in the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the regex that match the URI of the KG.
    """
    regex = []
    for s,p,o in graph:
        if p == VOID.uriRegexPattern or VOID.uriSpace:
            o = str(o)
            regex.append(o)
    if len(regex) > 0:       
        return regex
    else:
        return 'absent'

def getSerializationFormats(graph):
    """Find triples which contain the seriaization formats of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the serialization formats available for the KG.
    """
    formats = []
    for s,p,o in graph:
        if p == VOID.feature or DCAT.mediaType:
            o = str(o)
            formats.append(o)
    if len(formats) > 0:       
        return formats
    else:
        return 'absent'

def getLanguage(graph):
    """Find triples which contain the languages of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the languages supported by the KG.
    """
    formats = []
    for s,p,o in graph:
        if p == DCTERMS.language or DC.language:
            o = str(o)
            formats.append(o)
    if len(formats) > 0:       
        return formats
    else:
        return 'absent'
