<!-- markdownlint-disable -->

<a href="..\kgheartbeat\knowledge_graph.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `knowledge_graph.py`






---

## <kbd>class</kbd> `KnowledgeGraph`
Instanziate a KG by id. All information for analysis is recovered from the id. 

:param idKG: The Knowledge Graph id. :type idKG: str 

<a href="..\kgheartbeat\knowledge_graph.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(id)
```








---

<a href="..\kgheartbeat\knowledge_graph.py#L909"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `calculateTrustValue`

```python
calculateTrustValue()
```

Calculate the trust value of the KG. It is a value between -1 and 1, -1 when all believability data is absent, value beetween 0 and 1 based on how many values are present. 

:return: trust value of the KG :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkAuth`

```python
checkAuth()
```

Check if authentication is required to do SPARQL query on the endpoint. 

:return: True if authentication is required, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L405"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkDatatypeProblem`

```python
checkDatatypeProblem()
```

Count the number of literal that do not match the data type indicated. 

:return: number of literal with datatype problem. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L623"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkDeprecatedClassesProp`

```python
checkDeprecatedClassesProp()
```

Check if deprecated classes and properties are used in the KG. 

:return: list of deprecated classes and properties used in the KG, if the SPARQL endpoint is online. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkDownload`

```python
checkDownload()
```

Check if the link for download the KG as rdf dump is present and online. 

:return: The availability of rdf dump. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L357"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkEmptyLabel`

```python
checkEmptyLabel()
```

Count the number of empty label (if any) in the dataset. 

:return: number of empty label if SPARQL endpoint is online. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkEndpointAv`

```python
checkEndpointAv()
```

Check the SPARQL endpoint availability. 

:return: The SPARQL endpoint availability. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1591"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkExample`

```python
checkExample()
```

Check if query examples are provided with the KG. This information is obtained by analyzing the KG metadata, in particular, the field other resources. 

:return: True if there are any query examples, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L440"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkFPViolations`

```python
checkFPViolations()
```

Check for functional properties with inconsistent value, analyzing all triples with predicate owl:FunctionalProperty and checking if there is any violations. 

:return: Number of triples with functional property violations. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L287"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkHTTPS`

```python
checkHTTPS()
```

Check if data exchange on the SPARQL endpoint takes place on HTTPS protocol. 

:return: True if HTTPS is used, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L472"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkIFPViolations`

```python
checkIFPViolations()
```

Check for invalid usage of inverse-functional properties, analyzing all triples with predicate owl:InverseFunctionalProperty and checking if there is any violations.  

:return: Number of triples with inverse-functional properties violations. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkInactiveLinks`

```python
checkInactiveLinks()
```

Check if there are inactive link associated with the KG. 

:return: The availability of links. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L673"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkMisplacedClasses`

```python
checkMisplacedClasses()
```

Check if the classes are used incorrectly, classes are used in the position of the predicate. 

:return: list of misplaced class, if SPARQL endpoint is online. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L720"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkMisplacedProperty`

```python
checkMisplacedProperty()
```

Check if the properties are used incorrectly, properties are used in the position of the subject. 

:return: list of properties with misplaced propery problem :rtype: list  

---

<a href="..\kgheartbeat\knowledge_graph.py#L643"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkOntologyHijacking`

```python
checkOntologyHijacking()
```

Check for the ontology hijacking problem, if the SPARQL endpoint is online. This problem is present if there are a re-definition of classes or properties considered standard for LOD. 

:return: True if there is a Ontology Hijacking problem, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1466"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkRDFStr`

```python
checkRDFStr()
```

Check if RDF data structures is used in the KG.  

:return: True is are used, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1486"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkReuseTerms`

```python
checkReuseTerms()
```

Check usage of existing terms. This check is done using the Linked Open Vocabulary, a KG that contains vocabulary and terms standard for Linked Open Data. 

:return: True if no new terms are defined, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1510"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkReuseVocabs`

```python
checkReuseVocabs()
```

Check usage of existing vocabularies. This check is done using the Linked Open Vocabulary, a KG that contains vocabularies and terms standard for Linked Open Data. 

:return: True if no new vocabularies are defined, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1065"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkSign`

```python
checkSign()
```

Check if the KG is signed. 

:return: True if is signed, False otherwise. :rtype: bool 

---

<a href="..\kgheartbeat\knowledge_graph.py#L381"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `checkWhiteSpace`

```python
checkWhiteSpace()
```

Count the number of label that have a whitespace at the beginning or at the end. 

:return: number of label with whitespace problem if SPARQL endpoint is online. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1675"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getAccessAtKG`

```python
getAccessAtKG()
```

Get the ways in which you can access the KG. This information is retrived by analyzing the metadata and/or querying the SPARQL endpoint. 

:return: a list with the links to access at the KG. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L980"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getAuthors`

```python
getAuthors()
```

Get all KG authors. This information is retrived from the SPARQL endpoint or VOID file. 

:return: authors list. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L220"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getCentrality`

```python
getCentrality()
```

Get the centrality of kg in the graph constructed with all the kg discoverable. At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch. 

:return: centrality. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getClusteringCoefficient`

```python
getClusteringCoefficient()
```

Get the clustering coefficient of kg in the graph constructed with all the kg discoverable. At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch. 

:return: local clustering coeffcient. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1026"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getContributors`

```python
getContributors()
```

Get all the KG contributors. This information is retrived from the SPARQL endpoint or VOID file. 

:return: contributors list. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1094"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getCreationDate`

```python
getCreationDate()
```

Get the KG creation date. This information is retrived from the SPARQL endpoint or VOID file. False is returned if SPARQL endpoint is offline 

:return: KG creation date :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getDegreeOfConnection`

```python
getDegreeOfConnection()
```

Get the degree of connection of kg in the graph constructed with all the kg discoverable. At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch. 

:return: degree of connection. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L884"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getDescription`

```python
getDescription()
```

Get the description of the KG by analyzing the metadata. 

:return: description of KG. :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L506"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getDisjointValue`

```python
getDisjointValue()
```

Get the disjoint value. It is calculated by counting the number of triples with predicate owl:disjointWith and then making the ratio between number of triples with that predicate and number of entities. 

:return: disjoint value if triples and entity is recovered correctly form SPARQL endpoint. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L803"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getExtensionaConc`

```python
getExtensionaConc()
```

Get the extensional conciseness value, it is calculated by the following formula: 1.0 - #duplicated triples (calculated with Bloom filter algorithm) / #triples in the dataset. 

:return: intensional conciseness value. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getExternalProvider`

```python
getExternalProvider()
```

Return a dict with all external provider the key is the id of the KG it is connected to and the value is the number of triples connected, this information is obtained by analyzing the metadata. 

:return: external provider dictonary. :rtype: dict 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1204"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getFrequencyUp`

```python
getFrequencyUp()
```

Get the KG update frequency. This information is retrived from SPARQL endpoint or VOID file. 

:return: KG update frequency. :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L755"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getIntensionalConc`

```python
getIntensionalConc()
```

Get the intensional conciseness value, it is calculated by the following formula: 1.0 - #duplicated properties (calculated with Bloom filter algorithm)/#triples in the dataset. 

:return: intensional conciseness value. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1229"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getInterlinkingComp`

```python
getInterlinkingComp()
```

Calcuate the interlinking completeness. It is calculated by the ratio between the number of linked triples and number of all triples in the dataset. 

:return: interlinking completeness. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1657"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getLanguages`

```python
getLanguages()
```

Get the languages supported by the KG. This information is retrieved by querying the SPARQL endpoint. 

:return: a list with all language supported. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getLastUp`

```python
getLastUp()
```

Get the elapsed time since the last modification (in days). 

:return: days that have passed since the last modification. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L311"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getLatency`

```python
getLatency()
```

Get the latency of the sparql endpoint, is the time passed between the request for a triple and when is returned. The value returned is the average latency  of the 5 attempts performed. 

:return: average latency if SPARQL endpoint is online. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getLicenseHR`

```python
getLicenseHR()
```

Get the human-redeable license, search for a label on the triples in the KG. 

:return: human-redeable license. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L138"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getLicenseMR`

```python
getLicenseMR()
```

Return the machine-redeable license of the kg, checking on the SPARQL endpopint, in the metadata and in the void file . 

:return: machine-redeable license. :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getModificationDate`

```python
getModificationDate()
```

Get the KG modification date. This information is retrived from SPARQL endpoint or VOID file. False is returned if SPARQL endpoint is offline. 

:return: KG modification date. :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L872"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getName`

```python
getName()
```

Get the title of the KG by analyzing the metadata. 

:return: title of KG. :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1293"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getNumEntities`

```python
getNumEntities()
```

Count the number of entities in the dataset. This information can be obtained by a SPARQL endpoint or analyzing the VoID file. 

:return: The number of entities in the KG. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1540"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getNumLabels`

```python
getNumLabels()
```

Count the number of label on the triples in the KG. This count is done by using a query on the SPARQL endpoint. 

:return: Number of label in the KG. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1348"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getNumProperty`

```python
getNumProperty()
```

Get the number of property in the KG. This information is retrived by executing a query on the SPARQL endpoint. 

:return: poperty number :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getNumTriples`

```python
getNumTriples()
```

Get the number of triples in the KG. This information can be obtained by SPARQL endpoint or analyzing the metadata of the dataset. 

:return: Number of triples. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1614"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getNumbBN`

```python
getNumbBN()
```

Get the blank node number. This is obtained by querying the SPARQL endpoint. 

:return: blank node number. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L858"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getPageRank`

```python
getPageRank()
```

Get the pagerank of KG based on the graph constructed with all the kg discoverable. 

:return: pagerank value :rtype: float  

---

<a href="..\kgheartbeat\knowledge_graph.py#L1148"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getPercentageUpData`

```python
getPercentageUpData(modificationDate)
```

Get the percentage of updated data. The percentage is calcualted based on the modificationDate given as a parameter. 

:return: percentage of updated data. :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1003"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getPublishers`

```python
getPublishers()
```

Get all the KG pubilshers. This information is retrived from the SPARQL endpoint or VOID file. 

:return: publishers list. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1558"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getRegex`

```python
getRegex()
```

Return the uri regex of the KG. This check id done by using a query on the SPARQL endpoin or by analyzing the VoID file if available. 

:return: A list with the uri regex. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getSameAsChains`

```python
getSameAsChains()
```

Return the number of sameAs chains, counting the triples with the predicate equal to owl:sameAs. 

:return: number of sameAs chains. :rtype: int 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1634"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getSerializationFormat`

```python
getSerializationFormat()
```

Get the KG serialization formats. This information is retrived by executing a query on the SPARQL endpoint or from VoID file if available. 

:return: list of serialization formats. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1049"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getSources`

```python
getSources()
```

Get the KG sources. This return a Sources object that contains three field: web, email, name. 

:return: sources object with information about: web address, email, name authors or maintainer. :rtype: Sourcecs object 

---

<a href="..\kgheartbeat\knowledge_graph.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getThroughput`

```python
getThroughput()
```

Get the throughput of the sparql endpoint, is the number of triples obtained by the endpoint in one second. The value returned is the average thrpughput of the 5 attempts performed. 

:return: average throughput if SPARQL endpoint is online. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getURIsDef`

```python
getURIsDef()
```

Check the URIs deferenceability. This test is done based on 5000 triples retrieved randomly from the SPARQL endpoint, and for each triple a GET requests is performed. 

:return: A value which is the ratio between: number of deferenceable URIs and number of total URIs considered. :rtype: float 

---

<a href="..\kgheartbeat\knowledge_graph.py#L549"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getUndefinedClass`

```python
getUndefinedClass()
```

Get the classes used without declaration. 

:return: list of class undefined if SPARQL endpoint is online. :rtype: list  

---

<a href="..\kgheartbeat\knowledge_graph.py#L586"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getUndefinedProp`

```python
getUndefinedProp()
```

Get the properties used without declaration. 

:return: list of properties undefined if SPARQL endpoint is online. :rtype: list  

---

<a href="..\kgheartbeat\knowledge_graph.py#L896"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getUri`

```python
getUri()
```

Get the URI of the KG by analyzing the metadata. 

:return: URI of the KG :rtype: str 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1402"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getUriLenghtObj`

```python
getUriLenghtObj()
```

Get the uri's length in the object position. The returned value is a list in which the values are respectively min-max-average-standard deviation. 

:return: object uri's length. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1434"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getUriLenghtPr`

```python
getUriLenghtPr()
```

Get the uri's length in the predicate position. The returned value is a list in which the values are respectively min-max-average-standard deviation. 

:return: predicate uri's length. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L1368"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getUriLenghtSub`

```python
getUriLenghtSub()
```

Get the uri's length in the subject position. The returned value is a list in which the values are respectively min-max-average-standard deviation. 

:return: subject uri's length. :rtype: list 

---

<a href="..\kgheartbeat\knowledge_graph.py#L957"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `getVocabularies`

```python
getVocabularies()
```

Get all the vocabularies used in the KG. This information is retrived from the SPARQL endpoint or VOID file. 

:return: vocabularies list :rtype: list 




---

