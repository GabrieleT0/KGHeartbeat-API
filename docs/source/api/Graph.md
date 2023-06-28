# <kbd>module</kbd> `Graph.py`
---

Functions
---


`buildGraph()`
:   Constructs a graph that has all the automatically recoverable KGs as nodes and the respective relationships with the other KGs as edge.

    Returns:
        Graph: A graph with all the KGs automatically discoverable with its relationship.


`getCentrality(graph, idKg)`
:   Compute the centrality of the node in the Graph of all KGs.

    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.

    Returns:
        float: A float that is the centality of the KG in the graph og all KGs.


`getClusteringCoefficient(graph, idKG)`
:   Compute the clustering coefficient of a KG in the graph of KGs (the higher it is, the more it means that the node's ability to form a clique is high).     

    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.

    Returns:
        float: A float that is the clustering coefficient of a KG in the graph of all KGs.


`getDegreeOfConnection(graph, idKg)`
:   Compute the degree of connection of a KG (number of edges).

    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.

    Returns:
        int: A integer that is the number of edges of the KG.


`getPageRank(graph, idKg)`
:   Compute the PageRank of a KG. This is a value in range [0;10].

    Args:
:


`storeEdges(graph, nodelist)`
:   This function store info about all edges for every KG in the graph with all the KGs automatically discoverable (this is used for visualize the graph in the web app).

    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        nodelist (list): A list that contains all the IDs of the KGs whose subgraph we want to extract.