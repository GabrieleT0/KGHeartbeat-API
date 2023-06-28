import requests

"""
This module is used to extract the metadata for a particular KG from DataHub (https://old.datahub.io/). 

Examples:
    >>> from kgheartbeat import LODCloudAPI
    >>> LODCloudAPI.getJSONMetadata('dbpedia')

This module contains the following functions:

- `getJSONMetadata(idKG)` - Returns a JSON with all the metadata of the KG.
- `getNameKG(metadata)` -  Find the KG name in the metadata.
- `getLicense(jsonFile)` - Find the license in the metadata.
- `getAuthor(jsonFile)` - Find the KG author in the metadata.
- `getSource(jsonFile)` - Returns all sources related to the KG (e.g. email, name, website).
- `getSourceDict(jsonFile)` - Returns a dict with all sources related to the KG (e.g. email, name, website).
- `getOtherResources(jsonFile)` - Returns all other resources related to the KG (e.g. example of SPARQL query).
- `getTriples(jsonFile)` - Get the number of triples in the KG indicated in the metadata.
- `getSPARQLEndpoint(jsonFile)` - Returns the SPARQL endpoint of the KG from its ID.
- `getExternalLinks(jsonFile)` - Returns the KGs with which the KG is connected.
- `getDescription(jsonFile)` - Returns the description of KG from its metadata.
- `getKeywords(jsonFile)` - Returns all the keyword related with the KG.

"""

def getJSONMetadata(idKG):
    """Get the JSON file with all matadata about the KG from its id.
    
    Args:
        idKG (string): A string that represent the ID of KG that we want to fetch the metadata.
    
    Returns:
        dict: A dict that contains all the metadata of the KG.
    """
    url = 'https://lod-cloud.net/json/%s'%idKG
    try:
        response = requests.get(url)
        if response.status_code == 200:
            jsonMetadata = response.json()
            return jsonMetadata
        elif response.status_code == 404:
            print('Dataset not found on LOD Cloud')
            return False
    except:
        print('Failed to connect  to LOD Cloud')
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
        if (not license):
            return False
        else:
            return license
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
        owner = jsonFile.get('owner')
        if isinstance(owner,dict):
            name = owner.get('name')
            if (not name):
                name = 'absent'    
            email = owner.get('email')
            if (not email):
                email = 'absent'
            ownerStr = 'Name: %s, email: %s'%(name,email)
            return ownerStr
        else:
            return False
    else:
        return False

def getSource(jsonFile):
    """Get the KG source from the KG metadata.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        dict: A dict that contains all info about the KG source.
    """
    if isinstance(jsonFile,dict):
        website = jsonFile.get('website')
        if(not website):
            website = 'absent'
        contactPoint = jsonFile.get('contact_point')
        if isinstance(contactPoint,dict):
            contactPoint["web"] = website 
            name = contactPoint.get('name')
            email = contactPoint.get('email')
            if(not name):
                name = 'absent'
            if(not email):
                email = 'absent'
            return contactPoint
        else:
            return False
    else:
        return False

        
def getSourceDict(jsonFile):
    """Get the KG source from the KG metadata.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        dict: A dict that contains all info about the KG source.
    """
    if isinstance(jsonFile,dict):
        website = jsonFile.get('website')
        if(not website):
            website = 'absent'
        contactPoint = jsonFile.get('contact_point')
        if isinstance(contactPoint,dict):
            contactPoint["web"] = website 
            return contactPoint
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
        fullDownload = []
        example = []
        resources = []
        fullDownload = jsonFile.get('full_download')
        for i in range(len(fullDownload)):
            d = fullDownload[i]
            d['access_url'] = d.pop('download_url',None)  #RENAME THE KEY VALUE TO HAVE THE SAME NAME OF THE FIELD
            d['type'] = 'full_download'
        example = jsonFile.get('example')
        otherDownload = jsonFile.get('other_download')
        resources = example + otherDownload + fullDownload
        for i in range (len(resources)):   #DELETING UNNECESSARY ELEMENT FROM THE DICTIONARY 
            resources[i].pop('mirror',None)
            resources[i].pop('status',None)
            resources[i].pop('_id',None)
            d = resources[i]
            d['path'] = d['access_url']   #RENAME THE KEY VALUE TO HAVE THE SAME NAME OF THE FIELD IN THE DATAHUB METADATA
            del d['access_url']
            d['format'] = d.pop('media_type',None)
        return resources
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
        triples = jsonFile.get('triples',0)
        return triples
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
        listSparql = jsonFile.get('sparql')
        if isinstance(listSparql,list):
            if len(listSparql) >= 1:
                d = listSparql[0]
                url = d.get('access_url')
                return url
            else:
                return False
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
        links = jsonFile.get('links',0)
        if isinstance(links,list):
            return links
        else:
            return links
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
        en = jsonFile.get('description','absent')
        if isinstance(en,dict):
            description = en.get('en','absent')
            return description
        else:
            return 'absent'
    else:
        return False

def getKeywords(jsonfile):
    """Get the KG keyowords.
    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        string: A string that is the concatenation of all the KG keywords.
    """
    if isinstance(jsonfile,dict):
        keywords = jsonfile.get('keywords')
        return keywords
    else:
        return False