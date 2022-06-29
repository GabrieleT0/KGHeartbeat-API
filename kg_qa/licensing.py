from kg_qa import query as q

def getLicenseMR(url):
    '''
    Check the SPARQL endpoint availability.

    Parameters:
            url (str): SPARQL endpoint url
    
    Returns:
            license (str): machine-redeable license

    '''
    try:
        license = q.checkLicenseMR(url)
    except:
        license = 'Error in running the query'
    
    return license

def getLicenseHR(url):
        '''
        Check the SPARQL endpoint availability.

        Parameters:
            url (str): SPARQL endpoint url
    
        Returns:
            license (str): machine-redeable license
        '''
        try:
            license = q.checkLicenseHR(url)
        except:
            license
        
        return license
        