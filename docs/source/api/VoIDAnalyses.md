# <kbd>module</kbd> `VoIDAnalyses.py`
---

Functions
---
    
`getContributors(graph)`
:   Find triples which contain the contributors of the KG.
    
    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.
    
    Returns:
        list: A list that contains all the contributors (or the contributor) of the KG.


`getCreationDate(graph)`
:   Find triples with a predicate that indicate the KG creation date.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.

    Returns:
        Date: A Date object that represent the KG creation date.


`getCreators(graph)`
:   Find triples which contain the creators of the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the creators (or the creator) of the KG.


`getDataDump(graph)`
:   Find triples which contain the url of the KG dump file.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent a link to the KG dump


`getFrequency(graph)`
:   Find triples which contain the frequency update of the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent the frequency update of the KG.


`getLanguage(graph)`
:   Find triples which contain the languages of the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the languages supported by the KG.


`getLicense(graph)`
:   Find triples which contain the license of the KG (machine-redeable).

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent the machine-redeable license of a KG.


`getModificationDate(graph)`
:   Find triples with a predicate that indicate the KG last modification date.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.

    Returns:
        Date: A Date object that represent the KG creation date.


`getNumEntities(graph)`
:   Find triples which contain the number of entities of the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        string: A string that represent the number of entities in the KG.


`getPublishers(graph)`
:   Find triples which contain the publichers of the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the publishers (or the publicher) of the KG.


`getSerializationFormats(graph)`
:   Find triples which contain the seriaization formats of the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the serialization formats available for the KG.


`getUriRegex(graph)`
:   Find triples which contain the regex of URI in the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all its triples.

    Returns:
        list: A list that contains all the regex that match the URI of the KG.


`getVocabularies(graph)`
:   Find triples with a predicate that indicate the vocabulary used in the KG.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.

    Returns:
        list: A list with all vocabularies used by the KG.


`parseVoID(url)`
:   Parse the file VoID from an url and convert triples in a Graph object.

    Args:
        url (string): A string that represent a url of a VoID file available on Internet.

    Returns:
        Graph: A Graph object that contain all the triples in the VoID file.


`parseVoIDTtl(url)`
:   Parse the file VoID with the .ttl extension from an url and convert triples in a Graph object.

    Args:
        url (string): A string that represent a url of a VoID file available on Internet.

    Returns:
        Graph: A Graph object that contain all the triples in the VoID file.


`printVoID(graph)`
:   Print all the triples in the VoID file parsed.

    Args:
        graph (Graph): A Graph that represent a VoID file parsed with all it's triples.