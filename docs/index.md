# Welcome to KGHeartbeat API Docs

This is a library that helps you to analyze the quality of a Knowledge Graph directly in your Python application. See below how you can get started using the library. In the [reference](reference.md) section you can find all the documentation relating to the various modules that make up the library. 

### Installation
```
pip install kgheartbeat
```

### Get started 
How check SPARQL endpoint availability with this library:

```Python
from kgheartbeat import KnowledgeGraph

# Instanziate a KnowledgeGraph class, passing the id of the kg to be analyzed
kg = KnowledgeGraph('dbpedia')

# Call the check availability enpoint method
result = kg.checkEndpointAv()
```

For more examples go here: [more examples](tutorials.md)