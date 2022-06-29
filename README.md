# KG_QA
Library that allows you to perform Knowledge Graph (Linked Open Data) quality analysis.

### Installation
```
pip install kg-qa
```

###Get started 
How check SPARQL endpoint availability with this library:
```Python
from quality_analysis import KnowledgeGraph

# Instanziate a KnowledgeGraph object, passing the id of the kg to be analyzed
kg = KnowledgeGraph('dbpedia')

# Call the check availability enpoint method
result = kg.checkEndpointAv()
```