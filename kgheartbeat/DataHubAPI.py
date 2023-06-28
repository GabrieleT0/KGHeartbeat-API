import requests

"""
This module is used to extract the metadata for a particular KG from DataHub (https://old.datahub.io/). 

Examples:
    >>> from kgheartbeat import DataHubAPI
    >>> DataHubAPI.getDataPackage('dbpedia')

This module contains the following functions:

- `getDataPackage(idKG)` - Returns a JSON with all the metadata of the KG.
- `getNameKG(metadata)` -  Find the KG name in the metadata.
- `getLicense(metadata)` - Find the license in the metadata.
- `getSource(metadata)` -  Find any source from the metadata.
- `getAuthor(metadata)` - Find the KG author in the metadata.
- `getOtherResources(jsonFile)` - Returns all other resources related to the KG (e.g. example of SPARQL query).
- `getSPARQLEndpoint(jsonFile)` - Returns the SPARQL endpoint of the KG from its ID.
- `checkRDFDump(jsonFile)` - Get the link for download the KG in RDF format, if present.
- `getTriples(jsonFile)` - Get the number of triples in the KG indicated in the metadata.
- `getExternalLinks(jsonFile)` - Returns the KG with which the KG is connected.
- `getDescription(jsonFile)` - Returns the description of KG from its metadata.
- `getExtrasLang(jsonFile)` - Returns languages supported by the KG indicated in the metadata.
- `getKeywords(jsonFile)` - Returns all the keyword related with the KG.

"""

def getDataPackage(idDataset):
    """Get the JSON file with all matadata about the KG from its id.
    
    Args:
        idDataset (string): A string that represent the ID of KG that we want to fetch the metadata.
    
    Returns:
        dict: A dict that contains all the metadata of the KG.
    """
    api_url = "https://old.datahub.io/dataset/%s/datapackage.json" %idDataset
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            responseApi = response.json()
            return responseApi
        elif response.status_code == 404:
            print("Dataset not found on DataHub")
            return False
    except:
        print('Failed to connect to DataHub')
        return False

def getNameKG(metadata):
    """Get the KG name form the kg metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG name
    """
    if isinstance(metadata,dict):
        title = metadata.get('title')
        return title
    else:
        return False

def getLicense(jsonFile):
    """
    Get the license info from the metadata recovered.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG license.
    """
    if isinstance(jsonFile,dict):
        license = jsonFile.get('license')
        if isinstance(license,dict):
            licenseTitle = license.get('title')
            type = license.get('type')
            licenseStr = '%s - %s -'%(licenseTitle,type)
            return licenseStr
        else:
            return False
    else:
        return False

def getSources(jsonFile):
    """Get the KG source from the KG metadata.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.
    """
    if isinstance(jsonFile,dict):
        sources = jsonFile.get('sources',False)
        if isinstance(sources,list):
            return sources[0]
        else:
            return False
    else:
        return False


def getAuthor(jsonFile):
    """Get the KG author from the KG metadata.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.
    """
    if isinstance(jsonFile,dict):
        author = jsonFile.get('author')
        if isinstance(author,dict):
            authorName = author.get('name')
            authorEmail = author.get('email')
            authorStr = 'Name: %s, Email:%s'%(authorName,authorEmail)
            return authorStr
        else:
            return False
    else:
        return False

def getOtherResources(jsonFile):
    """Get all the other resources related with the KG (e.g. examples of SPARQL query) and delete the duplicate links.

    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        list: A list of dict that contains all the links to other resources.
    """
    if isinstance(jsonFile,dict):
        resources = []
        resources = jsonFile.get('resources')
        if isinstance(resources,list):
            for i in range(len(resources)):  #DELETING UNNECESSARY ELEMENT FROM THE DICTIONARY 
                resources[i].pop('name',None)
                resources[i].pop('hash',None)
            return resources
        else:
            return False
    else: 
        return False

def getSPARQLEndpoint(jsonFile):
    """Get the SPARQL endpoint from the KG metadata.    
    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        string: A string that is the SPARQL endpoint link.
    """
    if isinstance(jsonFile,dict):
        resources = jsonFile.get('resources')
        if isinstance(resources,list):
            for i in range(len(resources)):
                d = resources[i]
                format = d.get('format','')
                name = d.get('name','')
                if format == 'api/sparql' or 'sparql' in name:
                    url = d.get('path',False)
                    return url
            return False
        else:
            return False
    else:
        return False

def checkRDFDump(jsonFile):
    """Get the link to the RDF dump.

    Args:
        jsonFile (dict): A dict which contains all KG metadata.

    Returns:
        list: A list that contains all the links to other resources.
    """
    if isinstance(jsonFile,dict):
        resources = jsonFile.get('resources')
        if isinstance(resources,list):
            for i in range(len(resources)):
                format = resources[i].get('format')
                if format =='ZIP' or format == 'RAR:RDF' or format == 'RDF':
                    return True
        else:
            return False
    else:
        return False

def getTriples(jsonFile):
    """Get the number of KG triples indicated in the metadata.

    Args:
        jsonFile (dict): A dict which contains all KG metadata.

    Returns:
        int: An integer that is the number of triples in the KG.
    """
    if isinstance(jsonFile,dict):
        extras = jsonFile.get('extras')
        if isinstance(extras,dict):
            triples = extras.get('triples',0)
            return triples
        else:
            return False
    else:
        return False

def getExternalLinks(jsonFile):
    """Get all the external links related to the KG.
    
    Args:
        jsonFile (jsonFile): A dict which contains all the metadata of the KH.

    Returns:
        dict: A dict which contains the links and the info about the links.
    """
    if isinstance(jsonFile,dict):
        extras = {}
        extras = jsonFile.get('extras')
        if isinstance(extras,dict):
            extras = {i:extras[i] for i in extras if'links:' in i} #CLEAN THE DICTIONARY FROM OTHER ENTRY THAT ISN'T LINKS
            for i in extras.copy().keys():
              extras[i.removeprefix('links:')] = extras.pop(i,None) #REMOVING THE PREFIX LINK
            return extras
    else:
        return False

def getDescription(jsonFile):
    """Get the KG description.
    Args:
        jsonFile (dict): A dict that contains the KG metadata.

    Returns:
        string: A string that is the description of the data in the KG.
    """
    if isinstance(jsonFile,dict):
        description = jsonFile.get('description','absent')
        return description
    else:
        return False

def getExtrasLang(jsonFile):
    """Get the languages of the data in the KG.
    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        dict: A dict that contains the languages supported by the KG .
    """
    extras = jsonFile.get('extras')
    if isinstance(extras,dict):
        extras = {i:extras[i] for i in extras if'language' in i}
        return extras
    else:
        return False

def getKeywords(jsonFile):
    """Get the KG keyowords.
    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        string: A string that is the concatenation of all the KG keywords.
    """
    if isinstance(jsonFile,dict):
        keywords = jsonFile.get('keywords')
        return keywords
    else:
        return False
