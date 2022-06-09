from importlib.metadata import metadata
import json
from os import access
from site import execsitecustomize
import socket
from urllib.error import URLError
from urllib.request import URLopener
from numpy import source
from rdflib import VOID, Graph as rdfG
from requests import HTTPError
import aggregator
from quality_analysis.DataHubAPI import getLicense
import query as q
import utils
import VoIDAnalyses
import Graph
import LOVAPI
from SPARQLWrapper import SPARQLExceptions
from bloomfilter import BloomFilter
from sources import Sources

class KnowledgeGraph:
    '''
    Instanziate a KG by id.
    All information for analysis is recovered from the id.

    :param idKG: The Knowledge Graph id.
    :type idKG: str
    '''

    def __init__(self,id):
        self.id = id

    #AVAILABILITY
    
    def checkEndpointAv(self):
        '''
        Check the SPARQL endpoint availability.
        
        :return: The SPARQL endpoint availability.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
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
    
    def checkDownload(self):
        '''
        Check if the link for download the KG as rdf dump is present and online.

        :return: The availability of rdf dump.
        :rtype: bool
        '''
        resources = aggregator.getOtherResources(self.id)
        resources = utils.insertAvailability(resources)
        available = utils.checkAvailabilityForDownload(resources)

        return available
    
    def checkInactiveLinks(self):
        '''
        Check if there are inactive link associated with the KG.

        :return: The availability of links.
        :rtype: bool
        '''
        resources = aggregator.getOtherResources(self.id)
        resources = utils.insertAvailability(resources)
        resourcesObj = utils.toObjectResources(resources)
        inactiveLink = False
        for link in resourcesObj:
            if link.status == 'offline':
                inactiveLink = True
        
        return inactiveLink
    
    #LICENSING

    def getLicenseMR(self):
        '''
        Return the machine-redeable license of the kg, checking on the SPARQL endpopint, in the metadata and in the void file .
        
        :return: machine-redeable license.
        :rtype: str
        '''
        metadata = aggregator.getDataPackage(self.id)

        licenseM = aggregator.getLicense(metadata) #CHECKING IN THE METADATA
        if isinstance(licenseM,str): 
            return licenseM   #IF LICENSE IS INDICATED IN THE METADATE, RETURN IT

        try:
            licenseQ = q.checkLicenseMR2(aggregator.getSPARQLEndpoint(self.id)) #CHECKING ON THE SPARQL ENDPOINT
            if isinstance(licenseQ,list):
                return licenseQ
        except Exception as e:
            return e

        resources = aggregator.getOtherResources(self.id)
        resources = utils.insertAvailability(resources)
        otResources = utils.toObjectResources(resources)
        urlV = utils.getUrlVoID(otResources)
        if isinstance(urlV,str):  # CHECKING IF VOID FILE IS AVAILABLE
            try:
                voidFile = VoIDAnalyses.parseVoID(urlV)
                void = True
            except:
                try:
                    voidFile = VoIDAnalyses.parseVoIDTtl(urlV)
                    void = True
                except:
                    void = False 
        if void == True:
            licenseV = VoIDAnalyses.getLicense(voidFile)  #GETTING LICENSE FROM THE VOID FILE
            if isinstance(licenseV,str):
                return licenseV

    def getLicenseHR(self):
        '''
        Get the human-redeable license, search for a label on the triples in the KG.

        :return: human-redeable license.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        try:
            license = q.checkLicenseHR(url)
        except Exception as e:
            license = e

        return license
    
    #INTERLINKING

    def getDegreeOfConnection(self):
        '''
        Get the degree of connection of kg in the graph constructed with all the kg discoverable.
        At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch.
        
        :return: degree of connection.
        :rtype: int
        '''
        graph = utils.checkGraphFile()
        degree = Graph.getDegreeOfConnection(graph,self.id)
        return degree
    
    def getClusteringCoefficient(self):
        '''
        Get the clustering coefficient of kg in the graph constructed with all the kg discoverable.
        At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch.
        
        :return: local clustering coeffcient.
        :rtype: float
        '''
        graph = utils.checkGraphFile()
        lcc = Graph.getClusteringCoefficient(graph,self.id)
        
        return lcc
    
    def getCentrality(self):
        '''
        Get the centrality of kg in the graph constructed with all the kg discoverable.
        At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch.
        
        :return: centrality.
        :rtype: float
        '''
        graph = utils.checkGraphFile()
        centrality = Graph.getCentrality(graph,self.id)

        return centrality

    def getSameAsChains(self):
        '''
        Return the number of sameAs chains, counting the triples with the predicate equal to owl:sameAs.

        :return: number of sameAs chains.
        :rtype: int
        '''
        try:
            url = aggregator.getSPARQLEndpoint(self.id)
            if isinstance(url,str):
                numSameAs = q.getSameAsChains(url)
            else:
                numSameAs = 'SPARQL endpoint absent'
        except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
            numSameAs = 'SPARQL endpoint offline'
        except Exception as e:
            numSameAs = e

        return numSameAs

    def getExternalProvider(self):
        '''
        Return a dict with all external provider the key is the id of the KG it is connected to and the value is the number of triples connected, this information is obtained by analyzing the metadata.

        :return: external provider dictonary.
        :rtype: dict
        '''

        extLinks = aggregator.getExternalLinks(self.id)

        return extLinks

    #SECURITY
    
    def checkAuth(self):
        '''
        Check if authentication is required to do SPARQL query on the endpoint.

        :return: True if authentication is required, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                q.checkEndPoint(url)
                return False
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed):
                return 'SPARQL endpoint offline'
            except SPARQLExceptions.Unauthorized:
                return True
        else:
            return 'SPARQL endpoint absent'
    
    def checkHTTPS(self):
        '''
        Check if data exchange on the SPARQL endpoint takes place on HTTPS protocol.

        :return: True if HTTPS is used, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                isSecure = utils.checkhttps(url)
                if isSecure == True or isinstance(isSecure,list): #IF QUERY ON THE SPARQL ENDPOINT RETURN A RESULT IT IS A LIST, SO URL WITH HTTPS WORKS 
                    return True
                else:
                    return False
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except:
                return False
        else:
            return 'SPARQL endpoint absent'
    
    #PERFORMANCE

    def getLatency(self):
        '''
        Get the latency of the sparql endpoint, is the time passed between the request for a triple and when is returned.
        The value returned is the average latency  of the 5 attempts performed.

        :return: average latency if SPARQL endpoint is online.
        :rtype: float
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                latency = q.testLatency(url)
                sumL = sum(latency)
                average = sumL/len(latency)
                return average
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint absent'
    
    def getThroughput(self):
        '''
        Get the throughput of the sparql endpoint, is the number of triples obtained by the endpoint in one second.
        The value returned is the average thrpughput of the 5 attempts performed.

        :return: average throughput if SPARQL endpoint is online.
        :rtype: float
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                tp = utils.getThroughput(url)
                sumTP = sum(tp)
                average = sumTP/len(tp)
                return average
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint absent'

    #ACCURACY

    def checkEmptyLabel(self):
        '''
        Count the number of empty label (if any) in the dataset.

        :return: number of empty label if SPARQL endpoint is online.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                labels = q.getLabel(url)
                emptyL = 0
                for label in labels:
                    if utils.checkURI(label) == False:
                        if label == '':
                            emptyL = emptyL + 1
                return emptyL
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint absent'
    
    def checkWhiteSpace(self):
        '''
        Count the number of label that have a whitespace at the beginning or at the end.

        :return: number of label with whitespace problem if SPARQL endpoint is online.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                wsCount = 0
                labels = q.getLabel(url)
                for label in labels:
                    if utils.checkURI(label) == False:
                        if label != label.strip():
                            wsCount = wsCount + 1
                return wsCount
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint offline' 
    
    def checkDatatypeProblem(self):
        '''
        Count the number of literal that do not match the data type indicated.

        :return: number of literal with datatype problem.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                dataTypeProblem = 0
                triples = q.getAllTriplesSPO(url)
                if isinstance(triples,list):
                    for triple in triples:
                        obj = triple.get('o')
                        value = obj.get('value')
                        if utils.checkURI(value) == False:
                            dataType = obj.get('datatype')
                            if isinstance(dataType,str):
                                regex = utils.getRegex(dataType)
                                if regex is not None:
                                    result = utils.checkString(regex,value)
                                    if result == False:
                                        dataTypeProblem = dataTypeProblem + 1
                    return dataTypeProblem
                else:
                    return "Can't recover triples from the endpoint"
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint absent'
        
    #CONSISTENCY    
    
    def getDisjointValue(self):
        '''
        Get the disjoint value. It is calculated by counting the number of triples with predicate owl:disjointWith and then making the ratio between number of triples with that predicate and number of entities.

        :return: disjoint value if triples and entity is recovered correctly form SPARQL endpoint.
        :rtype: float
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                numDisjoint = q.getDisjoint(url)
                numEntities = q.getNumEntities(url)
                if not isinstance(numEntities,int):
                    regex = []
                    regex = q.checkUriRegex(url)
                    pattern = q.checkUriPattern(url)
                    for p in pattern:
                        newRegex = utils.trasforrmToRegex(p)
                        regex.append(newRegex)
                    if len(regex) > 0:
                        numEntities = 0
                        for r  in regex:
                            numEntities = numEntities + q.getNumEntitiesRegex(url,r)
                if isinstance(numDisjoint,int):
                    try:
                        numEntities = int(numEntities)
                        if numEntities > 0:
                            disjointValue = numDisjoint/numEntities
                        else:
                            disjointValue = 'insufficient data'
                    except:
                        disjointValue = 'insufficient data'   

                    return disjointValue     
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'   
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint absent'

    def getUndefinedClass(self):
        '''
        Get the classes used without declaration.

        :return: list of class undefined if SPARQL endpoint is online.
        :rtype: list 
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                allTriples = q.getAllTriplesSPO(url)
                allType = q.getAllType(url)
                toSearch = []
                found = False
                for i in range(len(allTriples)):
                    s = allTriples[i].get('s')
                    s = s.get('value')
                    allType.sort()
                    r = utils.binarySearch(allType,0,len(allType)-1,s)
                    if r != -1:
                        found = True
                        break
                    if found == False:
                        result = utils.checkURI(s)
                        if result == True:
                            toSearch.append(s)
                    found = False
                undClasses = LOVAPI.searchTermsList(toSearch)
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
            
            return undClasses
        else:
            return 'SPARQL endpoint absent'

    def getUndefinedProp(self):
        '''
        Get the properties used without declaration.

        :return: list of properties undefined if SPARQL endpoint is online.
        :rtype: list 
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                uriListP = q.getAllPredicate(url)
                properties = q.getAllProperty(url)
                toSearch = []
                found = False
                for i in range(len(uriListP)):
                    p = uriListP[i]
                    properties.sort()
                    r = utils.binarySearch(properties,0,len(properties)-1,p)
                    if r != -1:
                        found = True
                        break
                    if found == False:
                        result = utils.checkURI(p)
                        if result == True:
                            toSearch.append(p)
                    found = False
                undProperties = LOVAPI.searchTermsList(toSearch)
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                undProperties = 'SPARQL endpoint offline'
            except :
                undProperties = 'Could not process formulated query on indicated endpoint'
        
            return undProperties

        else:
            return 'SPARQL endpoint absent'
    
    def checkDeprecatedClassesProp(self):
        '''
        Check if deprecated classes and properties are used in the KG.

        :return: list of deprecated classes and properties used in the KG, if the SPARQL endpoint is online.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                deprecated = q.getDeprecated(url)
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                deprecated = e

            return deprecated
        else:
            return 'SPARQL endpoint absent'            

    def checkOntologyHijacking(self):
        '''
        Check for the ontology hijacking problem, if the SPARQL endpoint is online.
        This problem is present if there are a re-definition of classes or properties considered standard for LOD.

        :return: True if there is a Ontology Hijacking problem, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                allType = q.getAllType(url)
                triplesOH = False
                if isinstance(allType,list):
                    triplesOH = LOVAPI.searchTermsList(allType)
                    if len(triplesOH) > 0:
                        hijacking = True
                    else:
                        hijacking = False
                else:
                    hijacking = 'Impossible to retrieve the terms defined in the dataset'
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                hijacking = 'SPARQL endpoint offline'
            except:
                hijacking = 'Could not process formulated query on indicated endpoint'
            
            return hijacking
        else:
            return 'SPARQL endpoint absent'
    
    def checkMisplacedClasses(self):
        '''
        Check if the classes are used incorrectly, classes are used in the position of the predicate.

        :return: list of misplaced class, if SPARQL endpoint is online.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                misplacedClass = []
                properties = q.getAllProperty(url)
                allTriples = q.getAllTriplesSPO(url)
                found = False
                if isinstance(allTriples,list) and isinstance(properties,list):
                    properties.sort()
                    for i in range(len(allTriples)):
                        o = allTriples[i].get('o')
                        valueO = o.get('value')
                        s = allTriples[i].get('s')
                        valueS = s.get('value')
                        result = utils.checkURI(valueS)
                        if result == True:
                            r = utils.binarySearch(properties,0,len(properties)-1,valueS)
                            if r != -1:
                                found = True
                        resultO = utils.checkURI(valueO)
                        if found == False and resultO == True:
                            r2 = utils.binarySearch(properties,0,len(properties)-1,valueO)
                            if r2 != -1:
                                found = True
                        if found == True:
                            misplacedClass.append(valueS)
                            found = False
                else:
                    misplacedClass = 'insufficient data'
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                misplacedClass = 'SPARQL endpoint offline'
            except TimeoutError:
                misplacedClass = 'Timeout'
            except:
                misplacedClass = 'Could not process formulated query on indicated endpoint'
            
            return misplacedClass
        else:
            return 'SPARQL endpoint absent'

    def checkMisplacedProperty(self):
        '''
        Check if the properties are used incorrectly, properties are used in the position of the subject.

        :return: list of properties with misplaced propery problem
        :rtype: list 
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                misplacedProperty = []
                classes = q.getAllClasses(url)
                uriListP = q.getAllPredicate(url)
                if isinstance(uriListP,list) and isinstance(classes,list):
                    for i in range(len(uriListP)):
                        p = uriListP[i]
                        result = utils.checkURI(p)
                        if result == True:
                            classes.sort()
                            r = utils.binarySearch(classes,0,len(classes)-1,p)
                            if r != -1:
                                misplacedProperty.append(p)
                else:
                    misplacedProperty = 'insufficient data'
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                misplacedProperty =  'SPARQL endpoint offline'
            except Exception as e:
                misplacedProperty = e
            
            return misplacedProperty
        else:
            return 'SPARQL endpoint absent'

    #CONCISENESS

    def getIntensionalConc(self):
        '''
        Get the intensional conciseness value, it is calculated by the following formula: 1.0 - #duplicated properties (calculated with Bloom filter algorithm)/#triples in the dataset.

        :return: intensional conciseness value.
        :rtype: float
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                allProperty = q.getAllPropertySP(url)
                triplePropList = []
                duplicateP = []
                if isinstance(allProperty,list):
                    if len(allProperty) > 0:
                        for i in range(len(allProperty)):
                            s = allProperty[i].get('s')
                            p = allProperty[i].get('p')
                            subP = s.get('value')
                            predP = p.get('value')
                            tripleProp = subP + predP
                            triplePropList.append(tripleProp)
                        bloomF2 = BloomFilter(len(triplePropList),0.05)
                        for j in range(len(triplePropList)):
                            found = bloomF2.check(triplePropList[j])
                            if found == False:
                                bloomF2.add(triplePropList[j])
                            elif found == True:
                                duplicateP.append(triplePropList[j])
                        if len(allProperty) > 0:
                            intC = 1.0 - (len(duplicateP)/len(allProperty))
                        else:
                            intC = 'insufficient data'
                    else:
                        intC = '0 properties retrieved from the endpoint'
                else:
                    intC = 'insufficient data'
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                intC = 'SPARQL endpoint offline'
            except:
                intC = 'Could not process formulated query on indicated endpoint'
            
            return intC
        else:
            return 'SPARQL endpoint absent'

    def getExtensionaConc(self):
        '''
        Get the extensional conciseness value, it is calculated by the following formula: 1.0 - #duplicated triples (calculated with Bloom filter algorithm) / #triples in the dataset.

        :return: intensional conciseness value.
        :rtype: float
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                allTriples = q.getAllTriplesSPO(url)
                tripleList = []
                duplicate = []
                if isinstance(allTriples,list):
                    if len(allTriples)> 0:    
                        for i in range(len(allTriples)):
                            s = allTriples[i].get('s')
                            p = allTriples[i].get('p')
                            o = allTriples[i].get('o')
                            subject = s.get('value')
                            predicate = p.get('value')
                            object = o.get('value')
                            triple = subject + predicate + object
                            tripleList.append(triple)
                        bloomF = BloomFilter(len(tripleList),0.05)
                        print("Size of bit array:{}".format(bloomF.size))
                        print("False positive Probability:{}".format(bloomF.fp_prob))
                        print("Number of hash functions:{}".format(bloomF.hash_count))
                        for i in range(len(tripleList)):
                            found = bloomF.check(tripleList[i])
                            if found == False:
                                bloomF.add(tripleList[i])
                            elif found == True:
                                duplicate.append(tripleList[i])

                        if len(allTriples) > 0:
                            exC = 1.0 - (len(duplicate)/len(allTriples)) # From: Evaluating the Quality of the LOD Cloud: An Empirical Investigation (Ruben Verborgh)
                        else:
                            exC = 'insufficient data'
                    else:
                        exC = '0 triples retrieved from the endpoint'
                else:
                    exC = 'insufficient data'
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                exC = 'SPARQL endpoint offline'
            except:
                exC = 'Could not process formulated query on indicated endpoint'

            return exC
        else:
            return 'SPARQL endpoint absent'
    
    #REPUTATION
    def getPageRank(self):
        '''
         Get the pagerank of KG based on the graph constructed with all the kg discoverable.

         :return: pagerank value
         :rtype: float 
        '''
        graph = utils.checkGraphFile()
        pageRank = Graph.getPageRank(graph,self.id)

        return pageRank
    
    #BELIEVABILITY
    def getName(self):
        '''
        Get the title of the KG by analyzing the metadata.

        :return: title of KG.
        :rtype: str
        '''
        metadata = aggregator.getDataPackage(self.id)
        title = aggregator.getNameKG(metadata)
        
        return title

    def getDescription(self):
        '''
        Get the description of the KG by analyzing the metadata.

        :return: description of KG.
        rtype: str
        '''
        metadata = aggregator.getDataPackage(self.id)
        description = aggregator.getDescription(metadata)
        
        return description
    
    def getUri(self):
        '''
        Get the URI of the KG by analyzing the metadata.

        :return: URI of the KG
        :rtype: str
        '''
        metadata = aggregator.getDataPackage(self.id)
        sources = aggregator.getSource(metadata)
        url = sources.get('web','Absent')

        return url

    def calculateTrustValue(self):
        '''
        Calculate the trust value of the KG. It is a value between -1 and 1, -1 when all believability data is absent, value beetween 0 and 1 based on how many values are present.

        :return: trust value of the KG
        :rtype: int
        '''
        metadata = aggregator.getDataPackage(self.id)
        title = aggregator.getNameKG(metadata)
        description = aggregator.getDescription(metadata)
        sources = aggregator.getSource(metadata)
        url = sources.get('web','Absent')

        #CHECK IF THE KG IS IN A LIST OF RELIABLE PROVIDERS
        try:
            providers = ['wikipedia','government','bioportal','bio2RDF','academic']
            keywords = aggregator.getKeywords(self.id)
            if any(x in keywords for x in providers):
                believable = True
            else:
                believable = False
        except:
            believable = 'absent'
        valueN = 0
        valueD = 0
        valueUrl = 0
        valuePr = 0
        if isinstance(title,str):
            if title != '' and title != 'Absent' and title != 'absent':
                valueN = 1
        if isinstance(description,str):
            if description != '' and description != False and description != 'Absent':
                valueD = 1
        if isinstance(url,str):
            if url != '' and url !='Absent' and url != 'absent':
                valueUrl = 1
        if believable == True:
            valuePr = 1
        
        if valueN == 0 and valueD == 0 and valueUrl == 0 and valuePr == 0:
            trustValue = -1

        trustValue = (valueN+valueD+valueUrl+valuePr)/4
        
        return trustValue

    #VERIFIABILITY

    def getVocabularies(self):
        '''
        Get all the vocabularies used in the KG. This information is retrived from the SPARQL endpoint or VOID file.

        :return: vocabularies list
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                vocabularies = q.getVocabularies(url)
            except:
                vocabularies = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):  #IF SPARQL ENDPOINT IS OFFLINE TRY TO GET THE VOCABULARIES FROM VOID FILE
                    vocabularies = VoIDAnalyses.getVocabularies(voidFile)
        elif not isinstance(voidFile,bool): #IF SPARQL ENDPOINT IS ABSENT TRY TO GET THE VOCABULARIES FROM VOID FILE
            vocabularies = VoIDAnalyses.getVocabularies(voidFile)
        else:
            vocabularies = 'Impossible to retrieve vocabularies from SPARQL endopoint or VOID file'
        
        return vocabularies

    def getAuthors(self):
        '''
        Get all KG authors. This information is retrived from the SPARQL endpoint or VOID file.

        :return: authors list.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                authors = q.getCreator(url)
            except:
                authors = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):
                    authors = VoIDAnalyses.getCreators(voidFile)
        elif not isinstance(voidFile,bool):
            authors = VoIDAnalyses.getCreators(voidFile)
        else:
            authors = 'Impossible to retrieve vocabularies from SPARQL endopoint or VOID file'
        
        return authors

    def getPublishers(self):
        '''
        Get all the KG pubilshers. This information is retrived from the SPARQL endpoint or VOID file.

        :return: publishers list.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                publishers = q.getPublisher(url)
            except:
                publishers = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):
                    publishers = VoIDAnalyses.getPublishers(voidFile)
        elif not isinstance(voidFile,bool):
            publishers = VoIDAnalyses.getPublishers(voidFile)
        else:
            publishers = 'Impossible to retrieve vocabularies from SPARQL endopoint or VOID file'

        return publishers

    def getContributors(self):
        '''
        Get all the KG contributors. This information is retrived from the SPARQL endpoint or VOID file.

        :return: contributors list.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                contributors = q.getContributors(url)
            except:
                contributors = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):
                    contributors = VoIDAnalyses.getContributors(voidFile)
        elif not isinstance(voidFile,bool):
            contributors = VoIDAnalyses.getContributors(voidFile)
        else:
            contributors = 'Impossible to retrieve vocabularies from SPARQL endopoint or VOID file'
        
        return contributors
    
    def getSources(self):
        '''
        Get the KG sources. This return a Sources object that contains three field: web, email, name.
        
        :return: sources object with information about: web address, email, name authors or maintainer.
        :rtype: Sourcecs object
        '''
        metadata = aggregator.getDataPackage(self.id)
        sources = aggregator.getSource(metadata)
        if sources == False:
            sourcesObj = Sources('Absent','Absent','Absent')
        else:
            sourcesObj = Sources(sources.get('web','Absent'),sources.get('name','Absent'),sources.get('email','Absent'))
        
        return sourcesObj  #use sourcesKG() to print information about sources
    
    def checkSign(self):
        '''
        Check if the KG is signed.

        :return: True if is signed, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                sign = q.getSign(url)
                if isinstance(sign,int):
                    if sign > 0:
                        signed = True
                    else:
                        signed = False
                else:
                    signed = False
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                signed = 'SPARQL endpoint offline'
            except :
                signed = 'Could not process formulated query on indicated endpoint'
        else:
            signed = 'SPARQL endpoint absent'
        
        return signed
                



kg = KnowledgeGraph('taxref-ld')
result = kg.checkSign()
print(result)