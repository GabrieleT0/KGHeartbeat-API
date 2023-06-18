import requests

"""
This module interact directly with an API that aggregate all metadata about
the KGs that are automatically discoverable. Here is the service used: http://www.isislab.it:12280/kgsearchengine/

Examples:
    >>> from API import AGAPI
    >>> AGAPI.getMetadati('dbpedia')

This module contains the following functions:

- `getMetadati(idKG)` - Returns all metadata about the KG by its ID.
- `getAllKg()` - Returns all the metadata of all KG automatically discoverable from DataHub and LODC.
- `getSparqlEndpoint(metadata)` - Extract the SPARQL endpoint from the metadata.
- `getNameKG(metadata)` - Extract only the full name of the KG.
- `getIdByName(keyword)` - Returns the id of KG from its ID.

"""

def getMetadati(idKG):
    """Find the metadata about a KG from its id.

    Args:
        idKG (string): A string that represent the ID of KG that we want the metadata.

    Returns:
        string: A string that represent the metadata of the KG.
    """

    url = 'https://kgs-search-engine.herokuapp.com/brutalSearch?keyword=%s'%idKG
    try:
        response = requests.get(url)    
        if response.status_code == 200:
            response = response.json()
            results = response.get('results')
            return results
        else:
            print("Connection failed to AGAPI")
            return False
    except:
        print('Connection failed to AGAPI')
        return False

def getAllKg():
    """Retrieve metadata of all KGs that are automatically discoverable from LODC and DataHub.

    Returns:
        list: A list of dictionaries representing the metadata of all KGs.
    """

    url = 'https://kgs-search-engine.herokuapp.com/brutalSearch?keyword='
    try:
        response = requests.get(url)    
        if response.status_code == 200:
            print("Connection to API successful and data recovered")
            response = response.json()
            results = response.get('results')
            return results
        else:
            print("Connection failed")
            return False
    except:
        print('Connection failed')
        return False

def getSparqlEndpoint(metadata):
    """Extract the SPARQL endpoint URL from the metadata.

    Args:
        metadata (dict): The metadata of a KG.

    Returns:
        string: The URL of the SPARQL endpoint.
    """
    
    if isinstance(metadata,dict):
        sparqlInfo = metadata.get('sparql')
        if not sparqlInfo:
            return False
        accessUrl = sparqlInfo.get('access_url')
        return accessUrl

def getNameKG(metadata):
    """Extract the full name of the KG from the metadata.

    Args:
        metadata (dict): The metadata of a KG.

    Returns:
        string: The full name of the KG.
    """

    if isinstance(metadata,dict):
        title = metadata.get('title')
        return title
    else: 
        return False

def getIdByName(keyword):
    """Get the ID of the KG from its name.

    Args:
        keyword (string): The name or keyword of the KG.

    Returns:
        list: A list of KG IDs matching the keyword.
    """
    url = 'https://kgs-search-engine.herokuapp.com/brutalSearch?keyword=%s'%keyword
    try:
        response = requests.get(url)    
        if response.status_code == 200:
            print("Connection to API successful and data recovered")
            response = response.json()
            results = response.get('results')
            kgfound = []
            for i in range(len(results)):
                d = results[i]
                id = d.get('id')
                kgfound.append(id)
            return kgfound
        else:
            print("Connection failed")
            return False
    except:
        print('Connection failed')
        return False