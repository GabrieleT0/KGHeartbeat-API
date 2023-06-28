# <kbd>module</kbd> `LOVAPI.py`
---

Functions
---


`autocompleteTerm(term)`
:   Search similar terms based on the term given as input.

    Args:
        term (string): A string that represent a term used in the KG analyzed.

    Returns:
        dict: A dict that contains a list of terms similar to the term passed as input.


`autocompleteVocab(vocab)`
:   Search similar vocabularies based on the vocabulary given as input.

    Args:
        term (string): A string that represent a vocabulary used in the KG analyzed.

    Returns:
        dict: A dict that contains a list of vocabularies similar to the term passed as input.


`findVocabulary(vocab)`
:   Look for a vocabulary in the LOV to see if it is considered standard or is a new defined vocabulary.

    Args:
        vocab (string): A string that represent a vocabulary used in the KG analyzed.

    Returns:
        boolean: A boolean that is True if the vocabulary is in the LOV, False otherwise.


`getAllVocab()`
:   Search for all standard vocabularies included in the LOV.

    Returns:
        dict: A dict that contains all vocabularies considered standard by the LOV.


`searchTermsList(terms)`
:   Look for a terms in the files with all terms downloaded form the LOV to see if it are considered standard or is a new defined terms.

    Args:
        terms (list): A list that represent all terms  used in the KG analyzed.

    Returns:
        list: A list that contains all terms that aren't considered standard for the LOV.