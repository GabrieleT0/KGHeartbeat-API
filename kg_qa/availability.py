from os import access
from kg_qa import query as q
from kg_qa import utils

def checkEndpoindAv(url):
    '''
    Check the SPARQL endpoint availability.

    Parameters:
            url (str): SPARQL endpoint url
    
    Returns:
            availability (boolean): True for online, False for offline

    '''
    try:
        result = q.checkEndPoint(url)
        if isinstance(result,bytes):
            newUrl = utils.checkRedirect(url)
            result = q.checkEndPoint(newUrl)
            if isinstance(result,bytes):
                available = False
            else:
                available = True
        else:
            available = True
    except:
        available = False
    
    return available

def checkDownload(url):
    '''
    Check the RDF Dump availability 
    

    Parameters:
            url (str): SPARQL endpoint url
    
    Returns:
            availability (boolean): True for online, False for offline
    '''
    try:
        result = q.checkDataDump(url)
        if isinstance(result,list):
            available = True
        else:
            available = False
    except:
        available = False
    
    return available


    
