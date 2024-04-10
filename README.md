# KGHeartbeat API
Library that allows you to perform Knowledge Graph (Linked Open Data) quality analysis.

### Installation
```
pip install kgheartbeat
```

### Calculate the *Availability* dimension
```Python
from kgheartbeat import KnowledgeGraph

# Instanziate a KnowledgeGraph class, passing the id of the kg to be analyzed
kg = KnowledgeGraph('dbpedia')

# Check the SPARQL endpoint availability
sparqlAv = kg.checkEndpointAv()
# Check if the links for download the dataset is up
checkDump = kg.checkDownload()
# Check if there are any inactive links
inactiveLks = kg.checkInactiveLinks()
# Calculate the URI's deferenceability (based on 5000 randomly recoverable uri). THIS COULD TAKE TIME, DEPENDS ON THE SPEED OF THE ENDPOINT (~45 min. for DBpedia)
uriDef = kg.getURIsDef()

#Print all the results
print(f"SPARQL endpoint availability: {sparqlAv}\n \
       RDF dump link availability: {checkDump}\n\
       Any inactive links: {inactiveLks}\n\
       URIs deferenceability: {uriDef}")
```

### Calculate the *Licensing* dimension

```Python
from kgheartbeat import KnowledgeGraph

# Instanziate a KnowledgeGraph class, passing the id of the kg to be analyzed
kg = KnowledgeGraph('taxref-ld')

#Search for the machine-redeable license
mr_license = kg.getLicenseMR()
#Search for a human-redeable license
hr_license = kg.getLicenseHR()

print(f"Machine redeable license: {mr_license}\nHuman-redeable license: {hr_license}")
```

### Calcuate the *Versatility* dimension
```Python
# Instanziate a KnowledgeGraph class, passing the id of the kg to be analyzed
kg = KnowledgeGraph('bncf-ns')

#Find the different serialization formats available (e.g. .rdf, .n3, .xml)
formats = kg.getSerializationFormat()
#Get languages if is indicated
languages = kg.getLanguages()
#get all the links to access the KG
link_access = kg.getAccessAtKG()

print(f"Serialization formats: {formats}\nLanguages: {languages}\n Link to access the KG:{link_access}\n")
```