Module AGAPI
============

Functions
---------


`getAllKg()`
:   Retrieve metadata of all KGs that are automatically discoverable from LODC and DataHub.

    Returns:
        list: A list of dictionaries representing the metadata of all KGs.


`getIdByName(keyword)`
:   Get the ID of the KG from its name.

    Args:
        keyword (string): The name or keyword of the KG.

    Returns:
        list: A list of KG IDs matching the keyword.


`getMetadati(idKG)`
:   Find the metadata about a KG from its id.

    Args:
        idKG (string): A string that represent the ID of KG that we want the metadata.

    Returns:
        string: A string that represent the metadata of the KG.


`getNameKG(metadata)`
:   Extract the full name of the KG from the metadata.

    Args:
        metadata (dict): The metadata of a KG.

    Returns:
        string: The full name of the KG.


`getSparqlEndpoint(metadata)`
:   Extract the SPARQL endpoint URL from the metadata.

    Args:
        metadata (dict): The metadata of a KG.

    Returns:
        string: The URL of the SPARQL endpoint.
