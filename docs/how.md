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