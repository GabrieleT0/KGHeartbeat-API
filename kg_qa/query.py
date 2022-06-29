import datetime
import re
from SPARQLWrapper import *
from SPARQLWrapper import SPARQLWrapper
from xml.dom.minidom import Document
import time
from kg_qa import utils

def log_in_out(func):

    def decorated_func(*args, **kwargs):
        print("Doing ", func.__name__)
        result = func(*args, **kwargs)
        print("Done ")
        return result

    return decorated_func

@log_in_out
def checkEndPoint(url): 
    sparql = SPARQLWrapper(url) 
    sparql.setQuery("""
    SELECT ?s
    WHERE {?s ?p ?o .}
    LIMIT 1
    """)
    sparql.setTimeout(600) #10 minutes
    result = sparql.query().convert()
    return result

@log_in_out
def getNumTripleQuery(url): #TODO QUERY WITHOUT COUNT (MAY NOT BE SUPPORTED)
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
    SELECT (COUNT(?s) AS ?triples) 
    WHERE { ?s ?p ?o }
    """)
    sparql.setTimeout(300) #5 minutes
    sparql.setReturnFormat(XML)
    results = sparql.query().convert()
    if isinstance(results,Document):
        desc = results.getElementsByTagName("binding")[0]
        triples = desc.getElementsByTagName("literal")
        triplesValue = triples[0].firstChild.nodeValue
        return (int(triplesValue))

@log_in_out
def testLatency(url): 
    sparql = SPARQLWrapper(url)
    latency = []
    for i in range(5):
        sparql.setQuery("""
        SELECT *  
        WHERE {?s ?p ?o .}
        LIMIT 1
        """)
        sparql.setTimeout(180)
        start = time.time()
        sparql.query()
        latencyValue = (time.time() - start)
        latency.append(latencyValue)
    return latency

@log_in_out
def numBlankNode(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
    SELECT (COUNT(?bnode) AS ?triples) 
    WHERE { ?bnode ?p ?o
    FILTER (isBlank(?bnode))}
    """)
    sparql.setReturnFormat(JSON) #ASKS TO RECEIVE DATA IN JSON FORMAT IS SUPPORTED
    sparql.setTimeout(300) #5 minutes
    results = sparql.query().convert()
    if isinstance(results,dict):
        numBnode = utils.getResultsFromJSONCountInt(results) #BEFORE WITHOUT INT
        return numBnode
    elif isinstance(results,Document):
        numBnode = utils.getResultsFromXMLCount(results)
        return numBnode
    else:
        return False

@log_in_out
def getLangugeSupported(url):
    languages = []
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
    SELECT DISTINCT ?triples 
    WHERE{
    ?s ?p ?o.
    BIND(LANG(?o) as ?triples)}
    """)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(300) #5 minutes
    results = sparql.query().convert()
    if isinstance(results,dict):
        languages = utils.getResultsFromJSONCount(results)
        return languages
    elif isinstance(results,Document): #IF RESULT IS IN XML 
        languages = utils.getResultsFromXML(results)
        return languages
    else:
        return False

@log_in_out
def checkRDFDataStructures(url):  
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT *
    WHERE{
    {?s rdf:type rdf:List }
    UNION
    {?s rdf:type rdf:Statement}
    UNION
    {?s rdf:type rdf:Alt}
    UNION
    {?s rdf:type rdf:Bag}
    UNION
    {?s rdf:type rdf:Seq}
    UNION
    {?s rdf:type rdf:Container}
    UNION
    {?s rdf:subject ?o}
    UNION
    {?s rdf:predicate ?o}
    UNION
    {?s rdf:object ?o}
    UNION
    {?s rdfs:member ?o}
    UNION
    {?s rdf:first ?o}
    UNION
    {?s rdf:rest ?o}
    UNION
    {?s rdf:_'[0-9]+'}
    }
    LIMIT 1
    """)
    sparql.setTimeout(180) #5 minutes
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        result = results.get('results')
        bindings = result.get('bindings')
        if isinstance(bindings,list):
            if len(bindings) > 0:
                return True
            else:
                return False
        else:
            return False
    elif isinstance(results,Document):
        numTags = results.getElementsByTagName("binding").length
        if numTags > 0:
            return True
        else:
            return False
    else:
        return False

@log_in_out
def checkSerialisationFormat(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX void: <http://rdfs.org/ns/void#>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    SELECT DISTINCT ?o 
    WHERE{ 
    {?s void:feature ?o}
    UNION
    {?s dcat:mediaType ?o}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        link = utils.getResultsFromJSON(results)
        return link
    elif isinstance(results,Document):
        link = utils.getResultsFromXML(results)
        return link
    else:
        return False

@log_in_out
def checkDataDump(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX void: <http://rdfs.org/ns/void#>
    SELECT DISTINCT ?o 
    WHERE 
    {?s void:dataDump ?o}
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        link = utils.getResultsFromJSON(results)
        return link
    elif isinstance(results,Document):
        link = utils.getResultsFromXML(results)
        return link
    else:
        return False

@log_in_out
def checkLicenseMR(url): #PROBLEM ON http://lod.b3kat.de/sparql
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX cc: <http://creativecommons.org/ns#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX schema: <http://schema.org/>
    PREFIX doap: <http://usefulinc.com/ns/doap#>
    PREFIX xhtml: <http://www.w3.org/1999/xhtml#>
    SELECT DISTINCT ?o
    WHERE{
    {?s ?p ?o}
    VALUES (?p) {(dct:license) (dct:rights) (cc:license) (dc:license) (schema:license) (doap:license) (xhtml:license) (dc:rights)}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        licenses = utils.getResultsFromJSON(results)
        return licenses
    elif isinstance(results,Document):
        licenses = utils.getResultsFromXML(results)
        return licenses
    else:
        return False

@log_in_out
def checkLicenseMR2(url):   #USED IN CASE THE QUERY WITH VALUES ISN'T SUPPORTED
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX cc: <http://creativecommons.org/ns#>
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX schema: <http://schema.org/>
    PREFIX doap: <http://usefulinc.com/ns/doap#>
    PREFIX xhtml: <http://www.w3.org/1999/xhtml#>
    SELECT DISTINCT ?o
    WHERE{
    {?s dct:license ?o}
    UNION
    {?s dct:rights ?o}
    UNION
    {?s dc:rights ?o}
    UNION
    {?s cc:license ?o}
    UNION
    {?s dc:license ?o}
    UNION
    {?s schema:license ?o}
    UNION
    {?s xhtml:license ?o}
    UNION
    {?s doap:license ?o}
    }
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        licenses = utils.getResultsFromJSON(results)
        return licenses
    elif isinstance(results,Document):
        licenses = utils.getResultsFromXML(results)
        return licenses
    else:
        return False
@log_in_out
def checkLicenseHR(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX schema: <http://schema.org/>
    SELECT ?o
    WHERE{
        {?s rdfs:label  ?o}
    UNION
        {?s dct:description  ?o}
    UNION
        {?s rdfs:comment  ?o}
    UNION
        {?s rdfs:label  ?o}
    UNION
        {?s schema:description  ?o}
    FILTER regex(?o,".*(licensed?|copyrighte?d?).*(under|grante?d?|rights?).*")
    } 
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        result = results.get('results')
        bindings = result.get('bindings')
        if isinstance(bindings,list):
            if len(bindings) > 0:
                return True
            else:
                return False
        else:
            return False
    elif isinstance(results,Document):
        numTags = results.getElementsByTagName("binding").length
        if numTags > 0:
            return True
        else:
            return False
    else:
        return False
@log_in_out
def numberOfProperty(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT (COUNT(?o) AS ?triples)
    WHERE {
    { ?o a rdf:Property}
    UNION
    {?o a owl:DatatypeProperty}
    UNION
    {?o a skos:Property}
    }
    ''') 
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONCountInt(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXMLCount(results)
        return value
    else:
        return False
@log_in_out
def getNumLabel(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX skosxl:<http://www.w3.org/2008/05/skos-xl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX awol: <http://bblfish.net/work/atom-owl/2006-06-06/#>
    PREFIX wdrs: <http://www.w3.org/2007/05/powder-s#>
    PREFIX schema: <http://schema.org/>
    SELECT (COUNT(?o) AS ?triples)
    WHERE{
    {?s rdfs:label ?o}
    UNION
    {?s foaf:name ?o}
    UNION
    {?s skos:prefLabel ?o}
    UNION
    {?s dcterms:title ?o}
    UNION
    {?s dcterms:decription ?o}
    UNION
    {?s rdfs:comment ?o}
    UNION
    {?s awol:label ?o}
    UNION
    {?s dcterms:alternative ?o}
    UNION
    {?s skos:altLabel ?o}
    UNION
    {?s skos:note ?o}
    UNION
    {?s wdrs:text ?o}
    UNION
    {?s skosxl:altLabel ?o}
    UNION
    {?s skosxl:hiddenLabel ?o}
    UNION
    {?s skosxl:prefLabel ?o}
    UNION
    {?s skosxl:literalForm ?o}
    UNION
    {?s schema:name ?o}
    UNION
    {?s schema:description ?o}
    UNION
    {?s schema:alternateName ?o}
    }
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONCountInt(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXMLCount(results)
        return value
    else:
        return False
@log_in_out
def checkUriRegex(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX void: <http://rdfs.org/ns/void#>
    SELECT DISTINCT ?o 
    WHERE{
    {?s void:uriRegexPattern ?o}
    UNION
    {?s void:uriPattern ?o}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        regex = utils.getResultsFromJSON(results)
        return regex
    elif isinstance(results,Document):
        regex = utils.getResultsFromXML(results)
        return regex
    else:
        return False
@log_in_out
def checkUriPattern(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX void: <http://rdfs.org/ns/void#>
    SELECT DISTINCT ?o 
    WHERE
    {?s void:uriSpace ?o}
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        regex = utils.getResultsFromJSON(results)
        return regex
    elif isinstance(results,Document):
        regex = utils.getResultsFromXML(results)
        return regex
    else:
        return False
@log_in_out
def getVocabularies(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX void: <http://rdfs.org/ns/void#>
    SELECT DISTINCT ?o
    WHERE{?s void:vocabulary ?o }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        vocabularies = utils.getResultsFromJSON(results)
        return vocabularies
    elif isinstance(results,Document):
        vocabularies = utils.getResultsFromXMLUri(results)
        return vocabularies
    else:
        return False
@log_in_out
def getCreator(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT DISTINCT ?o 
    WHERE{ 
    {?s dc:creator ?o }
    UNION
    {?s dcterms:creator ?o}
    UNION
    {?s foaf:maker ?o}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        creators = utils.getResultsFromJSON(results)
        return creators
    elif isinstance(results,Document):
        creators = utils.getResultsFromXML(results)
        return creators
    else:
        return False
@log_in_out
def getPublisher(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dc: <http://purl.org/dc/elements/1.1/>
    SELECT DISTINCT ?o
    WHERE {?s dc:publisher ?o}
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        creators = utils.getResultsFromJSON(results)
        return creators
    elif isinstance(results,Document):
        creators = utils.getResultsFromXML(results)
        return creators
    else:
        return False
@log_in_out
def getNumEntities(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX void:<http://rdfs.org/ns/void#>
    SELECT ?triples
    WHERE {?s void:entities ?triples}
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        entities = utils.getResultsFromJSONCountInt(results)
        return entities
    elif isinstance(results,Document):
        entities = utils.getResultsFromXMLCount(results)
        return entities
    else:
        return False
@log_in_out
def getNumEntitiesRegex(url,entityRe):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
   SELECT (COUNT(?s) as ?triples)
   WHERE{
   {?s ?p ?o}
   FILTER(regex(?s,"%s"))
   }
    '''%entityRe)
    sparql.setTimeout(600)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        entities = utils.getResultsFromJSONCountInt(results)
        return entities
    elif isinstance(results,Document):
        entities = utils.getResultsFromXMLCount(results)
        return entities
    else:
        return False        
@log_in_out
def getContributors(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms:<http://purl.org/dc/terms/>
    SELECT DISTINCT ?o
    WHERE {?s dcterms:contributor ?o.}
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        contributors = utils.getResultsFromJSON(results)
        return contributors
    elif isinstance(results,Document):
        contributors = utils.getResultsFromXML(results)
        return contributors
    else:
        return False
@log_in_out
def getSameAsChains(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT (COUNT(?o) AS ?triples)
    WHERE {
    ?s owl:sameAs ?o
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONCountInt(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXMLCount(results)
        return value
    else:
        return False
@log_in_out
def getFrequency(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms:<http://purl.org/dc/terms/>
    SELECT DISTINCT ?o
    WHERE{
    {?s dcterms:accrualPeriodicity ?o}
    UNION
    {?s dcterms:Frequency ?o}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        frequency = utils.getResultsFromJSON(results)
        return frequency
    elif isinstance(results,Document):
        frequency = utils.getResultsFromXML(results)
        return frequency
    else:
        return False
@log_in_out
def getCreationDate(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms: <http://purl.org/dc/terms/>
    SELECT DISTINCT ?o
    WHERE{?s dcterms:created ?o}
    ORDER BY ASC(?o)
    LIMIT 1
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        creation = utils.getResultsFromJSON(results)
        match = re.search(r'\d{4}-\d{2}-\d{2}', creation[0])
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        date = str(date)
        return date
    elif isinstance(results,Document):
        creation = utils.getResultsFromXML(results)
        match = re.search(r'\d{4}-\d{2}-\d{2}', creation[0])
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        date = str(date)
        return date
    else:
        return False
@log_in_out
def getCreationDateMin(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms: <http://purl.org/dc/terms/>
    SELECT DISTINCT (MIN (?o) AS ?min)
    WHERE{
    {?s dcterms:created ?o}
    UNION
    {?s dcterms:issued ?o }
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        creation = utils.getResultsFromJSONMin(results)
        match = re.search(r'\d{4}-\d{2}-\d{2}', creation[0])
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        date = str(date)
        return date
    elif isinstance(results,Document):
        creation = utils.getResultsFromXML(results)
        match = re.search(r'\d{4}-\d{2}-\d{2}', creation[0])
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        date = str(date)
        return date
    else:
        return False
@log_in_out
def getModificationDate(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms: <http://purl.org/dc/terms/>
    SELECT DISTINCT ?o
    WHERE{
    {?s dcterms:modified ?o}
    }
    ORDER BY ASC(?o)
    LIMIT 1
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        modification = utils.getResultsFromJSON(results)
        if len(modification) > 0:
            match = re.search(r'\d{4}-\d{2}-\d{2}', modification[0])
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            date = str(date)
            return date
        else:
            return False
    elif isinstance(results,Document):
        modification = utils.getResultsFromXML(results)
        if len(modification) > 0:
            match = re.search(r'\d{4}-\d{2}-\d{2}', modification[0])
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            date = str(date)
            return date
        else:
            return False
    else:
        return False
@log_in_out
def getModificationDateMax(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms:<http://purl.org/dc/terms/>
    SELECT DISTINCT (MAX (?o) AS ?max)
    WHERE{
    {?s dcterms:modified ?o}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        modification = utils.getResultsFromJSONMax(results)
        if len(modification) > 0:
            match = re.search(r'\d{4}-\d{2}-\d{2}', modification[0])
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            date = str(date)
            return date
        else:
            return False
    elif isinstance(results,Document):
        modification = utils.getResultsFromXML(results)
        if len(modification) > 0:
            match = re.search(r'\d{4}-\d{2}-\d{2}', modification[0])
            date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
            date = str(date)
            return date
        else:
            return False
    else:
        return False

@log_in_out
def getDateUpdates(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX dcterms:<http://purl.org/dc/terms/>
    SELECT DISTINCT ?o
    WHERE{
    {?s dcterms:modified ?o}
    }
    ''')
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    modificationDate = []
    if isinstance(results,dict):
        modification = utils.getResultsFromJSONo(results)
        if len(modification) > 0:
            for i in range(len(modification)):
                match = re.search(r'\d{4}-\d{2}-\d{2}', modification[i])
                date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                date = str(date)
                modificationDate.append(date)
            return modificationDate
        else:
            return False
    elif isinstance(results,Document):
        modification = utils.getResultsFromXML(results)
        if len(modification) > 0:
            for i in range(len(modification)):
                match = re.search(r'\d{4}-\d{2}-\d{2}', modification[i])
                date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
                date = str(date)
                modificationDate.append(date)
            return modificationDate
        else:
            return False
    else:
        return False

@log_in_out
def getNumUpdatedData(url,date):
    if date != False:
        sparql = SPARQLWrapper(url)
        sparql.setQuery('''
        PREFIX dcterms:<http://purl.org/dc/terms/>
        SELECT DISTINCT (COUNT(?o) AS ?triples)
        WHERE{
        {?s dcterms:modified ?o}
        FILTER regex(?o,'%s')
        }
        '''%date)
    sparql.setTimeout(180)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONCountInt(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXMLCount(results)
        return value
    else:
        return False
@log_in_out
def getAllObject(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    SELECT DISTINCT ?o
    WHERE{?s ?p ?o.}
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        uriList = utils.getResultsFromJSON(results)
        return uriList
    elif isinstance(results,Document):
        uriList = utils.getResultsFromXML(results)
        return uriList
    else:
        return False

@log_in_out
def getAllPredicate(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    SELECT DISTINCT ?p
    WHERE{?s ?p ?o.}
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        uriList = utils.getResultsFromJSONp(results)
        return uriList
    elif isinstance(results,Document):
        uriList = utils.getResultsFromXML(results)
        return uriList
    else:
        return False

@log_in_out
def getDeprecated(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT ?s
    WHERE{
    {?s  rdf:type owl:DeprecatedClass}
    UNION
    {?s rdf:type owl:DeprecatedProperty}
    }''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        deprecated = utils.getResultsFromJSONs(results)
        return deprecated
    elif isinstance(results,Document):
         deprecated = utils.getResultsFromXML(results)
         return deprecated
    else:
        return False
@log_in_out
def getLabel(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX skosxl:<http://www.w3.org/2008/05/skos-xl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX awol: <http://bblfish.net/work/atom-owl/2006-06-06/#>
    PREFIX wdrs: <http://www.w3.org/2007/05/powder-s#>
    PREFIX schema: <http://schema.org/>
    SELECT ?o
    WHERE{
    {?s rdfs:label ?o}
    UNION
    {?s foaf:name ?o}
    UNION
    {?s skos:prefLabel ?o}
    UNION
    {?s dcterms:title ?o}
    UNION
    {?s dcterms:decription ?o}
    UNION
    {?s rdfs:comment ?o}
    UNION
    {?s awol:label ?o}
    UNION
    {?s dcterms:alternative ?o}
    UNION
    {?s skos:altLabel ?o}
    UNION
    {?s skos:note ?o}
    UNION
    {?s wdrs:text ?o}
    UNION
    {?s skosxl:altLabel ?o}
    UNION
    {?s skosxl:hiddenLabel ?o}
    UNION
    {?s skosxl:prefLabel ?o}
    UNION
    {?s skosxl:literalForm ?o}
    UNION
    {?s schema:name ?o}
    UNION
    {?s schema:description ?o}
    UNION
    {?s schema:alternateName ?o}
    }
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        labelList = utils.getResultsFromJSON(results)
        return labelList
    elif isinstance(results,Document):
        labelList = utils.getResultsFromXML(results)
        return labelList
    else:
        return False
@log_in_out
def getDisjoint(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    SELECT DISTINCT (COUNT(?s) AS ?triples) 
    WHERE 
    {?s owl:disjointWith ?o.}
    ''')
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONCountInt(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXMLCount(results)
        return value
    else:
        return False

@log_in_out
def getAllTriplesP(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
    SELECT DISTINCT (?p AS ?triples)
    WHERE { ?s ?p ?o }
    """)
    sparql.setTimeout(300) #5 minutes
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONCount(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXML(results)
        return value
    else:
        return False

@log_in_out
def getAllClasses(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery("""
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?s
    WHERE {?s rdf:type owl:Class}
    """)
    sparql.setTimeout(300) #5 minutes
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        value = utils.getResultsFromJSONs(results)
        return value
    elif isinstance(results,Document):
        value = utils.getResultsFromXML(results)
        return value
    else:
        return False
@log_in_out
def getAllProperty(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?p
    WHERE {
    { ?s ?p rdf:Property}
    UNION
    {?s ?p owl:DatatypeProperty}
    UNION
    {?s ?p skos:Property}
    }
    ''') 
    sparql.setTimeout(300)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        properties = utils.getResultsFromJSONp(results)
        return properties
    elif isinstance(results,Document):
        properties = utils.getResultsFromXML(results)
        return properties
    else:
        return False

@log_in_out
def getAllType(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?s
    WHERE {?s rdf:type ?o}
    ''')
    sparql.setTimeout(300) #5 minutes
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if isinstance(results,dict):
            properties = utils.getResultsFromJSONs(results)
            return properties
        elif isinstance(results,Document):
            properties = utils.getResultsFromXML(results)
            return properties
        else:
            return False
    except Exception as e :
        return e
@log_in_out
def getAllTypeO(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?o
    WHERE {?s rdf:type ?o}
    ''')
    sparql.setTimeout(300) #5 minutes
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if isinstance(results,dict):
        properties = utils.getResultsFromJSONo(results)
        return properties
    elif isinstance(results,Document):
        properties = utils.getResultsFromXML(results)
        return properties
    else:
        return False
@log_in_out
def getAllTriplesSPO(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    SELECT *
    WHERE{?s ?p ?o}
    ''')
    sparql.setTimeout(600) #10 minutes
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if isinstance(results,dict):
            result = results.get('results')
            bindings = result.get('bindings')
            return bindings
        elif isinstance(results,Document): 
            bindings = utils.xmlToDictSPO(results)
            return bindings
        else:
            return False
    except Exception as e:
        return e

@log_in_out
def getSign(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX swp:<http://www.w3.org/2004/03/trix/swp-2/>
    SELECT ?s ?o
    WHERE{
    {?s swp:signature ?o}
    UNION
    {?s swp:authority ?o}
    UNION
    {?s swp:certificate ?o}
    UNION
    {?s swp:quotedBy ?o}
    UNION
    {?s swp:assertedBy ?o}
    }
    ''')
    sparql.setTimeout(600) #10 minutes
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if isinstance(results,dict):
            result = results.get('results')
            bindings = result.get('bindings')
            return len(bindings)
        elif isinstance(results,Document):
            bindings = utils.xmlToDict(results)
            return len(bindings)
        else:
            return False
    except Exception as e:
        return e
    
@log_in_out
def getAllPropertySP(url):
    sparql = SPARQLWrapper(url)
    sparql.setQuery('''
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT DISTINCT ?s ?p
    WHERE {
    { ?s ?p rdf:Property}
    UNION
    {?s ?p owl:DatatypeProperty}
    UNION
    {?s ?p skos:Property}
    }
    ''') 
    sparql.setTimeout(600) #10 minutes
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        if isinstance(results,dict):
            result = results.get('results')
            bindings = result.get('bindings')
            return bindings
        elif isinstance(results,Document): #TODO XML AS RESPONSE
            bindings = utils.xmlToDictP(results)
            return bindings
        else:
            return False
    except Exception as e:
        return e