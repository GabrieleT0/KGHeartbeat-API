# <kbd>module</kbd> `aggregator.py`
=================

Functions
---------


`getAuthor(metadata)`
:   Get the KG author from the KG metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.


`getDataPackage(idKG)`
:   Get the JSON file with all matadata about the KG from its id, both from LODC and DataHub.
    If metadata are available on both the services, then return the ones from DataHub.

    Args:
        idKG (string): A string that represent the ID of KG that we want the metadata.

    Returns:
        dict: A dict that contains all the metadata of the KG.


`getDescription(metadata)`
:   Get the KG description.
    Args:
        metadata (dict): A dict that contains the KG metadata.

    Returns:
        string: A string that is the description of the data in the KG.


`getExternalLinks(idKG)`
:   Get all the external links related to the KG.

    Args:
        idKG (string): A string that contains the KG id.

    Returns:
        dict: A dict that contains the links and the info about the links.


`getExtrasLanguage(idKg)`
:   Get the languages of the data in the KG.
    Args:
        idKG (str): A string that represents the KG id.

    Returns:
        dict: A dict that contains the languages supported by the KG .


`getKeywords(idKg)`
:   Get the KG keyowords.
    Args:
        idKG (string): A string that represent the KG id.

    Returns:
        string: A string that is the concatenation of all the KG keywords.


`getLicense(metadata)`
:   Get the license info from the metadata recovered.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG license.


`getNameKG(metadata)`
:   Get the KG name form the kg metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG name


`getOtherResources(idKG)`
:   Get all the other resources related with the KG (e.g. examples of SPARQL query).

    Args:
        idKG (string): A string that contains the KG id.

    Returns:
        list: A list that contains all the links to other resources.


`getSPARQLEndpoint(idKG)`
:   Get the SPARQL endpoint from the KG id, try to find on both DataHub and LODCloud.
    If the link is available on both the service, is selected the one from LODCloud
    Args:
        idKG (string): A string that contains the KG id.

    Returns:
        string: A string that is the SPARQL endpoint link.


`getSource(metadata)`
:   Get the KG source from the KG metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        string: A string that represent the KG author.


`getTriples(metadata)`
:   Get the number of KG triples from the  metadata.

    Args:
        metadata (dict): A dict that contains all KG metadata.

    Returns:
        int: A integer that represent the number of triples in the KG.
