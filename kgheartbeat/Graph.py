import json
import os
import string
import networkx as nx
from kgheartbeat import AGAPI
from kgheartbeat import aggregator
from kgheartbeat import utils
import re

"""
This module is used to create a Graph which includes all the KG automatically discovered (node)  with all the relative connections with the other KG (edges).
This is useful for calculate all the metrics in the Interlinking dimension.
Examples:
    >>> from kgheartbeat import Graph
    >>> graph = Graph.buildGraph()
    >>> Graph.getCentrality(graph,idKG)

This module contains the following functions:
- `buildGraph()` - Function that build the Graph with all the KG automatically discoverable, with all its connections.
- `getPageRank(graph,idKg)` - Calculate the PageRank for a specific KG.
- `getDegreeOfConnection(graph,idKg)` - Get the degree of connection of a KG.
- `getCentrality(graph,idKg)` -  Get the centrality of the KG.
- `getClusteringCoefficient(graph,idKG)` - Get the clustering coefficient of the KG.
- `getSubgraph(graph,nodeList)` - Returns an induced graph, which contains only the KG in the list passed as parameter (nodeList).
- `storeEdges(graph,nodelist)` - Save the graph induced as a JSON file. 
"""


def buildGraph():
    """Constructs a graph that has all the automatically recoverable KGs as nodes and the respective relationships with the other KGs as edge.
    
    Returns:
        Graph: A graph with all the KGs automatically discoverable with its relationship.
    """
    allKg = AGAPI.getAllKg()
    idList = []
    G = nx.Graph()
    for i in range(len(allKg)):
        element = allKg[i]
        id = element.get('id')
        idList.append(id)
    for j in range(len(idList)):
        externalLinks = aggregator.getExternalLinks(idList[j])
        exLinksObj = utils.toObjectExternalLinks(externalLinks)
        print(idList[j])
        if isinstance(exLinksObj,list) and len(exLinksObj) > 0:
            for k in range(len(exLinksObj)):
                link = exLinksObj[k]
                value = str(link.value)
                value = re.sub("[^\d\.]", "",value)
                if value == '':
                    value = 0
                value = int(value)
                G.add_edge(idList[j],link.nameKG,weight=value)
    #pos = nx.spring_layout(G, k=0.8)
    #nx.draw(G,pos,with_labels=True,width=0.4,node_size=400)
    #plt.show()
    return G

def getPageRank(graph,idKg):
    """Compute the PageRank of a KG. This is a value in range [0;10].
    
    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.
    
    Returns:
        float: A float that is the PageRank of the KG.
    """
    pr = nx.pagerank(graph)
    return pr.get(idKg)

def getDegreeOfConnection(graph,idKg):
    """Compute the degree of connection of a KG (number of edges).
    
    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.
    
    Returns:
        int: A integer that is the number of edges of the KG.
    """
    degree = graph.degree(nbunch=idKg)
    return degree

def getCentrality(graph,idKg):
    """Compute the centrality of the node in the Graph of all KGs.
    
    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.
    
    Returns:
        float: A float that is the centality of the KG in the graph og all KGs.
    """
    degreeCentrality = nx.degree_centrality(graph)
    return degreeCentrality.get(idKg)

def getClusteringCoefficient(graph,idKG):
    """Compute the clustering coefficient of a KG in the graph of KGs (the higher it is, the more it means that the node's ability to form a clique is high).
    
    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        idKG (string): A string that represent the id of the KG whose page rank we want to calculate.
    
    Returns:
        float: A float that is the clustering coefficient of a KG in the graph of all KGs.
    """
    clusteringCoefficient = nx.clustering(graph,idKG)
    return clusteringCoefficient

def getSubgraph(graph,nodeList):
    subG = graph.subgraph(nodeList)
    return subG

def storeEdges(graph,nodelist):
    """This function store info about all edges for every KG in the graph with all the KGs automatically discoverable (this is used for visualize the graph in the web app).
    
    Args:
        graph (Graph): A Graph that represent A graph with all the KGs automatically discoverable with its relationship.
        nodelist (list): A list that contains all the IDs of the KGs whose subgraph we want to extract. 
    
    """
    save_path = './Graphs Visualization JS/Subgraphs'
    for i in range(len(nodelist)):
        newFilename = re.sub(r'[\\/*?:"<>|]',"",nodelist[i])
        remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
        newFilename = newFilename.translate(remove_punctuation_map)
        remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        newFilename = newFilename.translate(remove_punctuation_map)
        completeName = os.path.join(save_path, newFilename+".txt")
        e = graph.edges(nodelist[i])
        e = str(e)
        e = e.replace('(','[')
        e = e.replace(')',']')
        e = e.replace("'",'"')
        with open(completeName,'w',encoding="utf-8") as f:
            f.write(e)

