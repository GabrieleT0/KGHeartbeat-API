# <kbd>module</kbd> `LODCloudAPI.py`
---

Functions
---

    
`getAuthor(jsonFile)`
:   Get the KG author from the KG metadata.
    
    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.


`getDescription(jsonFile)`
:   Get the KG description.
    Args:
        jsonFile (dict): A dict that contains the KG metadata.

    Returns:
        string: A string that is the description of the data in the KG.


`getExternalLinks(jsonFile)`
:   Get all the external links related to the KG.

    Args:
        jsonFile (jsonFile): A dict which contains all the metadata of the KH.

    Returns:
        dict: A dict which contains the links and the info about the links.


`getJSONMetadata(idKG)`
:   Get the JSON file with all matadata about the KG from its id.

    Args:
        idKG (string): A string that represent the ID of KG that we want to fetch the metadata.

    Returns:
        dict: A dict that contains all the metadata of the KG.


`getKeywords(jsonfile)`
:   Get the KG keyowords.
    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        string: A string that is the concatenation of all the KG keywords.


`getLicense(jsonFile)`
:   Get the license info from the metadata recovered.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG license.


`getNameKG(metadata)`
:   Get the KG name form the kg metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG name


`getOtherResources(jsonFile)`
:   Get all the other resources related with the KG (e.g. examples of SPARQL query) and delete the duplicate links.

    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        list: A list of dict that contains all the links to other resources.


`getSPARQLEndpoint(jsonFile)`
:   Get the SPARQL endpoint from the KG metadata.
    Args:
        jsonFile (dict): A dict which contains all the KG metadata.

    Returns:
        string: A string that is the SPARQL endpoint link.


`getSource(jsonFile)`
:   Get the KG source from the KG metadata.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        dict: A dict that contains all info about the KG source.


`getSourceDict(jsonFile)`
:   Get the KG source from the KG metadata.

    Args:
        jsonFile (dict): A dict that contains all KG metadata.

    Returns:
        dict: A dict that contains all info about the KG source.


`getTriples(jsonFile)`
:   Get the number of KG triples indicated in the metadata.

    Args:
        jsonFile (dict): A dict which contains all KG metadata.

    Returns:
        int: An integer that is the number of triples in the KG.