from kgheartbeat import DataHubAPI
from kgheartbeat import LODCloudAPI
from kgheartbeat import utils

"""
This module aggregate the metadata for a particular KG by using DataHub and LODCloud.
This module is necessary because with the AGAPI, we can't get all the KGs metadata, but only few information (such as the SPARQL endpoint), but for our task we need all of it.

Examples:
    >>> from kgheartbeat import aggregator
    >>> aggregator.getDataPackage('dbpedia')

This module contains the following functions:

- `getDataPackage(idKG)` - Returns a JSON with all the metadata of the KG.
- `getNameKG(metadata)` -  Find the KG name in the metadata.
- `getLicense(metadata)` - Find the license in the metadata.
- `getAuthor(metadata)` - Find the KG author in the metadata.
- `getSource(metadata)` -  Find any source from the metadata.
- `getTriples(metadata)` - Returns the number of KG triples indicated in the medatada. 
-  getSPARQLEndpoint(idKG) - Returns the SPARQL endpoint of the KG from its ID, by searching on both LODC and DataHUB.
-  getOtherResources(idKG) - Returns all other resources related to the KG (e.g. example of SPARQL query).
-  getExternalLinks(idKG) -  Returns all links related to the KG (e.g. ant rdf dump link available).
-  getDescription(metadata) - Returns the description of KG from its metadata.
-  getExtrasLanguage(idKg) - Returns languages supported by the KG indicated in the metadata.
-  getKeywords(idKg) - Returns all the keyword related with the KG.

"""

def getDataPackage(idKG):
    """Get the JSON file with all matadata about the KG from its id, both from LODC and DataHub.
    If metadata are available on both the services, then return the ones from DataHub.
    
    Args:
        idKG (string): A string that represent the ID of KG that we want the metadata.
    
    Returns:
        dict: A dict that contains all the metadata of the KG.
    """
    metadataDH = DataHubAPI.getDataPackage(idKG)
    metadataLODC = LODCloudAPI.getJSONMetadata(idKG)
    if isinstance(metadataDH,dict):
        return metadataDH
    elif isinstance(metadataLODC,dict):
        return metadataLODC
    else:
        return False

def getNameKG(metadata):
    """Get the KG name form the kg metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG name
    """
    nameDH = DataHubAPI.getNameKG(metadata)
    nameLODC = LODCloudAPI.getNameKG(metadata)
    if nameDH != False:
        return nameDH
    elif nameLODC != False:
        return nameLODC
    else:
        return False

def getLicense(metadata):
    """
    Get the license info from the metadata recovered.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG license.
    """
    licenseDH = DataHubAPI.getLicense(metadata)
    licenseLODC = LODCloudAPI.getLicense(metadata)
    if licenseDH != False:
        return licenseDH
    elif licenseLODC != False:
        return licenseLODC
    else:
        return False

def getAuthor(metadata):
    """Get the KG author from the KG metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.
    """
    authorDH = DataHubAPI.getAuthor(metadata)
    authorLODC = LODCloudAPI.getAuthor(metadata)
    if authorDH != False:
        return authorDH
    elif authorLODC != False:
        return authorLODC
    else:
        return False

def getSource(metadata):
    """Get the KG source from the KG metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.
    """
    sourcesDH = DataHubAPI.getSources(metadata)
    sourcesLODC = LODCloudAPI.getSourceDict(metadata)
    if sourcesDH != False:
        return sourcesDH
    elif sourcesLODC != False:
        return sourcesLODC
    else:
        return False

def getTriples(metadata):
    """Get the number of KG triples from the  metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        int: A integer that represent the number of triples in the KG.
    """
    numTriplesDH = DataHubAPI.getTriples(metadata)
    numTriplesLODC = LODCloudAPI.getTriples(metadata)
    if numTriplesDH != False:
        return numTriplesDH
    elif numTriplesLODC != False:
        return numTriplesLODC
    else:
        return False

def getSPARQLEndpoint(idKG):
    """Get the SPARQL endpoint from the KG id, try to find on both DataHub and LODCloud.
    If the link is available on both the service, is selected the one from LODCloud    
    Args:
        idKG (string): A string that contains the KG id.

    Returns:
        string: A string that is the SPARQL endpoint link.
    """
    metadataLODC = LODCloudAPI.getJSONMetadata(idKG)
    metadataDH = DataHubAPI.getDataPackage(idKG)
    endpointLODC = LODCloudAPI.getSPARQLEndpoint(metadataLODC)  
    endpointDH = DataHubAPI.getSPARQLEndpoint(metadataDH)
    if endpointLODC != False:
        if isinstance(endpointLODC,str):
            if endpointLODC != '':
                return endpointLODC
            else:
                return endpointDH
        else:
            return endpointDH
    else:
        return endpointDH

def getOtherResources(idKG):
    """Get all the other resources related with the KG (e.g. examples of SPARQL query).

    Args:
        idKG (string): A string that contains the KG id.

    Returns:
        list: A list that contains all the links to other resources.
    """
    metadataDH = DataHubAPI.getDataPackage(idKG)
    metadataLODC = LODCloudAPI.getJSONMetadata(idKG)
    otResourcesDH = DataHubAPI.getOtherResources(metadataDH)
    otResourcesLODC = LODCloudAPI.getOtherResources(metadataLODC)
    if otResourcesDH == False:
        otResourcesDH = []
    if otResourcesLODC == False:
        otResourcesLODC = []
    otherResources = utils.mergeResources(otResourcesDH,otResourcesLODC)
    return otherResources

def getExternalLinks(idKG):
    """Get all the external links related to the KG.
    
    Args:
        idKG (string): A string that contains the KG id.

    Returns:
        dict: A dict that contains the links and the info about the links.
    """
    metadataDH = DataHubAPI.getDataPackage(idKG)
    metadataLODC = LODCloudAPI.getJSONMetadata(idKG)
    linksDH = DataHubAPI.getExternalLinks(metadataDH)
    if linksDH == False or linksDH is None:
        linksDH = {}   #BECAUSE IS USED TO CLEAN THE RESULTS FROM LODCLOUD (IN CASE DATAHUB NOT HAVE EXTERNAL LINKS)
    linksLODC = LODCloudAPI.getExternalLinks(metadataLODC)
    if isinstance(linksLODC,list):
        for i in range(len(linksLODC)):
            d = linksLODC[i]
            key = d.get('target')
            value = d.get('value')
            linksDH[key] = value
        return linksDH
    else:
        return linksDH

def getDescription(metadata):
    """Get the KG description.
    Args:
        metadata (dict): A dict that contains the KG metadata.

    Returns:
        string: A string that is the description of the data in the KG.
    """
    descriptionDH = DataHubAPI.getDescription(metadata)
    descriptionLODC = LODCloudAPI.getDescription(metadata)
    if descriptionDH != False and not isinstance(descriptionDH,dict):
        return descriptionDH
    elif descriptionLODC != False:
        return descriptionLODC
    else:
        return False

def getExtrasLanguage(idKg):
    """Get the languages of the data in the KG.
    Args:
        idKG (str): A string that represents the KG id.

    Returns:
        dict: A dict that contains the languages supported by the KG .
    """
    metadataDH = DataHubAPI.getDataPackage(idKg)
    if isinstance(metadataDH,dict):
        language = DataHubAPI.getExtrasLang(metadataDH)
        if isinstance(language,dict):
            return language
        else:
            return 'absent'
    else:
        return 'absent'

def getKeywords(idKg):
    """Get the KG keyowords.
    Args:
        idKG (string): A string that represent the KG id.

    Returns:
        string: A string that is the concatenation of all the KG keywords.
    """
    metadataDH = DataHubAPI.getDataPackage(idKg)
    metadataLODC = LODCloudAPI.getJSONMetadata(idKg)
    keywordsDH = DataHubAPI.getKeywords(metadataDH)
    keywordsLODC = LODCloudAPI.getKeywords(metadataLODC)
    keywords = keywordsDH + keywordsLODC
    return keywords

