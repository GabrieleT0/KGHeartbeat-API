import datetime
import json
import re
import socket
from urllib.error import URLError
from numpy import source, void
import numpy
from rdflib import VOID, Graph as rdfG
from requests import HTTPError
from kg_qa import aggregator
from kg_qa import query as q
from kg_qa import utils,VoIDAnalyses,Graph,LOVAPI
from SPARQLWrapper import SPARQLExceptions
from kg_qa.bloomfilter import BloomFilter
from kg_qa.sources import Sources

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
        lcc = "%.3f"%lcc
        
        return float(lcc)
    
    def getCentrality(self):
        '''
        Get the centrality of kg in the graph constructed with all the kg discoverable.
        At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch.
        
        :return: centrality.
        :rtype: float
        '''
        graph = utils.checkGraphFile()
        centrality = Graph.getCentrality(graph,self.id)
        centratility = "%.3f"%centrality

        return float(centrality)

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


    def checkFPViolations(self):
        '''
        Check for functional properties with inconsistent value, analyzing all triples with predicate owl:FunctionalProperty and checking if there is any violations.

        :return: Number of triples with functional property violations.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                violationFP = []
                triplesFP = q.getFP(url)
                for triple in triplesFP:
                    s = triple.get('s')
                    subject1 = s.get('value')
                    o = triple.get('o')
                    obj1 = o.get('value')
                    for triple2 in triplesFP:
                        s = triple2.get('s')
                        subject2 = s.get('value')
                        o = triple2.get('o')
                        obj2 = o.get('value')
                        if subject1 == subject2 and obj1 != obj2:
                            violationFP.append(triple)
                return len(violationFP)
            except (HTTPError,URLError,SPARQLExceptions.EndPointNotFound,socket.gaierror,SPARQLExceptions.EndPointInternalError,json.JSONDecodeError, SPARQLExceptions.QueryBadFormed,SPARQLExceptions.Unauthorized):
                return 'SPARQL endpoint offline'
            except Exception as e:
                return e
        else:
            return 'SPARQL endpoint absent'
        
    def checkIFPViolations(self):
        '''
        Check for invalid usage of inverse-functional properties, analyzing all triples with predicate owl:InverseFunctionalProperty and checking if there is any violations. 
        
        :return: Number of triples with inverse-functional properties violations.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                violationIFP = []
                triplesIFP = q.getIFP(url)
                for triple in triplesIFP:
                    s = triple.get('s')
                    subject1 = s.get('value')
                    o = triple.get('o')
                    obj1 = o.get('value')
                    for triple2 in triplesIFP:
                        s = triple2.get('s')
                        subject2 = s.get('value')
                        o = triple2.get('o')
                        obj2 = o.get('value')
                        if obj1 == obj2 and subject1 != subject2:
                            violationIFP.append(triple)
                return len(violationIFP)
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
                            disjointValue = "%.3f"%disjointValue
                            disjointValue = float(disjointValue)
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
                            intC = "%.3f"%intC
                            intC = float(intC)
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
                            exC = "%.3f"%exC
                            exC = float(exC)
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
        pageRank = "%.4f"%pageRank

        return float(pageRank)
    
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
        :rtype: str
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
    
    #CURRENCY

    def getCreationDate(self):
        '''
        Get the KG creation date. This information is retrived from the SPARQL endpoint or VOID file. False is returned if SPARQL endpoint is offline

        :return: KG creation date
        :rtype: str
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                creationD = q.getCreationDateMin(url)
            except:
                creationD = False
                try:
                    creationD = q.getCreationDate(url)
                except:
                    creationD = False
                if not isinstance(voidFile,bool) and not isinstance(creationD,str):
                    creationD = VoIDAnalyses.getCreationDate(voidFile)
        elif not isinstance(voidFile,bool):
            creationD = VoIDAnalyses.getCreationDate(voidFile)
        else:
            creationD = 'SPARQL endpoint and VoID absent'

        return creationD

    def getModificationDate(self):
        '''
        Get the KG modification date. This information is retrived from SPARQL endpoint or VOID file. False is returned if SPARQL endpoint is offline.

        :return: KG modification date.
        :rtype: str
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                modificationD = q.getModificationDateMax(url)
            except:
                modificationD = False
                try:
                    modificationD = q.getModificationDate(url)
                except:
                    modificationD = False
                if not isinstance(voidFile,bool) and not isinstance(modificationD,str):
                    modificationD = VoIDAnalyses.getCreationDate(voidFile)
        elif not isinstance(voidFile,bool):
            modificationD = VoIDAnalyses.getCreationDate(voidFile)
        else:
            modificationD = 'SPARQL endpoint and VoID absent'

        return modificationD
    
    def getPercentageUpData(self,modificationDate):
        '''
        Get the percentage of updated data. The percentage is calcualted based on the modificationDate given as a parameter.

        :return: percentage of updated data.
        :rtype: str
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                numTriplesUp = q.getNumUpdatedData(url,modificationDate)
            except:
                numTriplesUp = 'SPARQL endpoint offline'
        else:
            numTriplesUp = 'SPARQL endpoint absent'

        return numTriplesUp
    
    def getLastUp(self):
        '''
        Get the elapsed time since the last modification (in days).

        :return: days that have passed since the last modification.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                modificationD = q.getModificationDateMax(url)
            except:
                modificationD = False
                try:
                    modificationD = q.getModificationDate(url)
                except:
                    modificationD = False
                if not isinstance(voidFile,bool) and not isinstance(modificationD,str):
                    modificationD = VoIDAnalyses.getCreationDate(voidFile)
        elif not isinstance(voidFile,bool):
            modificationD = VoIDAnalyses.getCreationDate(voidFile)
        else:
            modificationD = 'SPARQL endpoint and VoID absent'
        try:
            today = datetime.date.today()
            todayFormatted = today.strftime("%Y-%m-%d")
            todayDate =  datetime.datetime.strptime(todayFormatted, "%Y-%m-%d").date()
            modificationD = datetime.datetime.strptime(modificationD, "%Y-%m-%d").date()
            delta = (todayDate - modificationD).days
        except:
            delta = 'Insufficient data'


        return delta

    #VOLATILITY
    
    def getFrequencyUp(self):
        '''
        Get the KG update frequency. This information is retrived from SPARQL endpoint or VOID file.

        :return: KG update frequency.
        :rtype: str
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                frequency = q.getFrequency(url)
            except:
                frequency = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):
                    frequency = VoIDAnalyses.getFrequency(voidFile)
        elif not isinstance(voidFile,bool):
            frequency = VoIDAnalyses.getFrequency(voidFile)
        else:
            frequency = 'SPARQL endpoint and VoID file absent'

        return frequency
    
    #COMPLETENESS

    def getInterlinkingComp(self):
        '''
        Calcuate the interlinking completeness. It is calculated by the ratio between the number of linked triples and number of all triples in the dataset.

        :return: interlinking completeness.
        :rtype: int
        '''
        externalLinks = aggregator.getExternalLinks(self.id)
        exLinksObj = utils.toObjectExternalLinks(externalLinks)
        triplesL = 0
        for i in range(len(exLinksObj)): #COUNTING THE NUMBER OF TRIPLES CROSS EXTERNAL LINK LIST IN THE METADATA
            link = exLinksObj[i]
            value = link.value
            value = str(link.value)
            value = re.sub("[^\d\.]", "",value) #CHECK IF THE VALUE IS A NUMBER
            value = int(value)
            triplesL = triplesL + value
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                triples = q.getNumTripleQuery(url) #COUNT THE NUMBER OF TRIPLES WITH A SPARQL QUERY
            except:   #IF SPARQL ENDPOINT IS OFFLINE, COUNT THE TRIPLES BY ANALYZING THE METADATA
                triples = 'SPARQL endpoint offline'
                metadata = aggregator.getDataPackage(self.id)
                triples = aggregator.getTriples(metadata)
        else:
            triples = 'SPARQL endpoint and VoID file absent'
        
        try:
            triplesL = int(triplesL)
            triples = int(triples)
            if triples > 0:
                iCompl = (triplesL/triples)
                iCompl = "%.2f"%iCompl
                iCompl = float(iCompl)
            else:
                iCompl = 'Insufficient data'
        except:
            iCompl = 'Insufficient data'

        return iCompl
    
    #AMOUNT OF DATA

    def getNumTriples(self):
        '''
        Get the number of triples in the KG. This information can be obtained by SPARQL endpoint or analyzing the metadata of the dataset.

        :return: Number of triples.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        metadata = aggregator.getDataPackage(self.id)
        if isinstance(url,str):
            try:
                triples = q.getNumTripleQuery(url)
            except:
                triples = 'SPARQL endpoint offline'
                triples = aggregator.getTriples(metadata)
        else:
            triples = aggregator.getTriples(metadata)

        return triples
    
    def getNumEntities(self):
        '''
        Count the number of entities in the dataset. This information can be obtained by a SPARQL endpoint or analyzing the VoID file.

        :return: The number of entities in the KG.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                entities = q.getNumEntities(url)
                try:
                    entities = int(entities)
                    return entities
                except:  #IF WITH THE FIRST QUERY WE DON'T GET THE RESULT, WE TRY TO COUNT THE NUMBER OF ENTITIES BY COUNTING THE NUMBER OF TRIPLES THAT MATH WITH THEKG URI REGEX
                    #GET THE REGEX OF THE URLs USED
                    regex = []
                    try:
                        regex = q.checkUriRegex(url)
                    except:
                        regex = 'Could not process formulated query on indicated enpdoint'
                    
                    #CHECK IF IS INDICATED A URI SPACE INSTEAD OF A REGEX AND WE TRAFORM IT TO REGEX
                    try:    
                        pattern = q.checkUriPattern(url)  
                        if isinstance(pattern,list):
                            for i in range(len(pattern)): 
                                newRegex = utils.trasforrmToRegex(pattern[i])
                                regex.append(newRegex)
                    except:
                        pattern = 'Could not process formulated query on indicated enpdoint'

                    #NOW COUNT THE ENITITIES USING THE REGEX
                    try:
                        if len(regex) > 0:
                            entities = 0
                            for i in range(len(regex)):
                                entities = entities + q.getNumEntitiesRegex(url,regex[i])
                        else:
                            entities = 'insufficient data'
                    except Exception as e:
                        entities = e
                    
                    return entities
            except:
                if not isinstance(voidFile,bool):
                    entities = VoIDAnalyses.getNumEntities(voidFile)
                    return entities
        elif not isinstance(voidFile,bool):
            entities = VoIDAnalyses.getNumEntities(voidFile)
            return entities
        else:
            return 'SPARQL endpoint and VoID file absent'

    def getNumProperty(self):
        '''
        Get the number of property in the KG. This information is retrived by executing a query on the SPARQL endpoint.

        :return: poperty number
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                numProperty = q.numberOfProperty(url)
            except:
                numProperty = 'SPARQL endpoint offline'
        else:
            numProperty = 'SPARQL endpoint absent'

        return numProperty

    #REPRESENTATIONAL-CONCISENESS
    
    def getUriLenghtSub(self):
        '''
        Get the uri's length in the subject position. The returned value is a list in which the values are respectively min-max-average-standard deviation.

        :return: subject uri's length.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                lengthtList = []
                triples = q.getAllTriplesSPO(url)
                for triple in triples:
                    s = triple.get('s')
                    uri = s.get('value')
                    if utils.checkURI(uri) == True:
                        lengthtList.append(len(uri))
                sumLenghts = sum(lengthtList)
                avLenghts = sumLenghts/len(lengthtList) 
                avLenghts = str(avLenghts)
                avLenghts = avLenghts.replace('.',',')
                standardDeviationL = numpy.std(lengthtList)
                standardDeviationL = str(standardDeviationL)
                standardDeviationL = standardDeviationL.replace('.',',')
                minLenghtS = min(lengthtList)
                maxLenghtS = max(lengthtList)
                length = [minLenghtS,maxLenghtS,avLenghts,standardDeviationL]
            except:
                length = 'SPARQL endpoint offline'
        else:
            length = 'SPARQL endpoint absent'

        return length
    
    def getUriLenghtObj(self):
        '''
        Get the uri's length in the object position. The returned value is a list in which the values are respectively min-max-average-standard deviation.

        :return: object uri's length.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                uriListO = q.getAllObject(url)
                lengthtList = []
                for triple in uriListO:
                    if utils.checkURI(triple) == True:
                        lengthtList.append(len(triple))
                sumLenghts = sum(lengthtList)
                avLenghts = sumLenghts/len(lengthtList) 
                avLenghts = str(avLenghts)
                avLenghts = avLenghts.replace('.',',')
                standardDeviationL = numpy.std(lengthtList)
                standardDeviationL = str(standardDeviationL)
                standardDeviationL = standardDeviationL.replace('.',',')
                minLenghtS = min(lengthtList)
                maxLenghtS = max(lengthtList)
                length = [minLenghtS,maxLenghtS,avLenghts,standardDeviationL]
            except:
                length = 'SPARQL endpoint offline'
        else:
            length = 'SPARQL endpoint absent'

        return length
    
    def getUriLenghtPr(self):
        '''
        Get the uri's length in the predicate position. The returned value is a list in which the values are respectively min-max-average-standard deviation.

        :return: predicate uri's length.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                uriListP = q.getAllPredicate(url)
                lengthtList = []
                for triple in uriListP:
                    if utils.checkURI(triple) == True:
                        lengthtList.append(len(triple))
                sumLenghts = sum(lengthtList)
                avLenghts = sumLenghts/len(lengthtList) 
                avLenghts = str(avLenghts)
                avLenghts = avLenghts.replace('.',',')
                standardDeviationL = numpy.std(lengthtList)
                standardDeviationL = str(standardDeviationL)
                standardDeviationL = standardDeviationL.replace('.',',')
                minLenghtS = min(lengthtList)
                maxLenghtS = max(lengthtList)
                length = [minLenghtS,maxLenghtS,avLenghts,standardDeviationL]
            except:
                length = 'SPARQL endpoint offline'
        else:
            length = 'SPARQL endpoint absent'

        return length

    def checkRDFStr(self):
        '''
        Check if RDF data structures is used in the KG. 

        :return: True is are used, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                rdf = q.checkRDFDataStructures(url)
            except:
                rdf = 'SPARQL endpoint offline'
        else:
            rdf = 'SPARQL endpoint absent'

        return rdf

    #REPRESENTATIONAL-CONSISTENCY

    def checkReuseTerms(self):
        '''
        Check usage of existing terms. This check is done using the Linked Open Vocabulary, a KG that contains vocabulary and terms standard for Linked Open Data.

        :return: True if no new terms are defined, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                objList = []
                triplesO = q.getAllTypeO(url)
                for term in triplesO:
                    objList.append(term)
                newTermsD = LOVAPI.searchTermsList(objList)
                if len(newTermsD) > 0:
                    return False
                else:
                    return True
            except:
                return 'SPARQL endpoint offline'
        else:
            return 'SPARQL endpoint absent'
    
    def checkReuseVocabs(self):
        '''
        Check usage of existing vocabularies. This check is done using the Linked Open Vocabulary, a KG that contains vocabularies and terms standard for Linked Open Data.

        :return: True if no new vocabularies are defined, False otherwise.
        :rtype: bool
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                newVocab = []
                vocabs = q.getVocabularies(url)
                if isinstance(vocabs,list):
                    for vocab in vocabs:
                        result = LOVAPI.findVocabulary(vocab)
                        if result == False:
                            newVocab.append(vocab)
                    if len(newVocab) > 0:
                        return False
                    else:
                        return True
                else:
                    return 'Impossible to retrieve KG vocabularies'
            except:
                return 'SPARQL endpoint offline'
        else:
            return 'SPARQL endpoint absent'

    #UNDERSTENDABILITY

    def getNumLabels(self):
        '''
        Count the number of label on the triples in the KG. This count is done by using a query on the SPARQL endpoint.

        :return: Number of label in the KG.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                numLabel = q.getNumLabel(url)
            except:
                numLabel = 'SPARQL endpoint offline'
        else:
            numLabel = 'SPARQL endpoint absent'
        
        return numLabel

    def getRegex(self):
        '''
        Return the uri regex of the KG. This check id done by using a query on the SPARQL endpoin or by analyzing the VoID file if available.

        :return: A list with the uri regex.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            regex = []
            try:
                regex = q.checkUriRegex(url)
            except Exception as e:
                regex = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):
                    regex = VoIDAnalyses.getUriRegex(voidFile) 
            #CHECK IF IS INDICATED A URI SPACE INSTEAD OF A REGEX AND WE TRAFORM IT TO REGEX
            try:    
                pattern = q.checkUriPattern(url)  
                if isinstance(pattern,list):
                    for i in range(len(pattern)): 
                        newRegex = utils.trasforrmToRegex(pattern[i])
                        regex.append(newRegex)
            except:
                pattern = 'SPARQL endpoint offline'
        elif not isinstance(voidFile,bool):
            regex = VoIDAnalyses.getUriRegex(voidFile)
        else:
            regex = 'SPARQL endpint absent'
        
        return regex

    def checkExample(self):
        '''
        Check if query examples are provided with the KG. This information is obtained by analyzing the KG metadata, in particular, the field other resources.

        :return: True if there are any query examples, False otherwise.
        :rtype: bool
        '''
        resources = aggregator.getOtherResources(self.id)
        resources = utils.insertAvailability(resources)
        otResources = utils.toObjectResources(resources)
        example = False
        for j in range(len(otResources)):
            if isinstance(otResources[j].format,str):
                if 'example' in otResources[j].format:
                    example = True
            if isinstance(otResources[j].title,str):
                if 'example' in otResources[j].title:
                    example = True

        return example
    
    #INTERPRETABILITY

    def getNumbBN(self):
        '''
        Get the blank node number. This is obtained by querying the SPARQL endpoint.

        :return: blank node number.
        :rtype: int
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                numBlankN = q.numBlankNode(url)
            except:
                numBlankN = 'SPARQL endpoint offline'
        else:
            numBlankN = 'SPARQL endpoint absent'

        return numBlankN
    
    #VERSATILIY

    def getSerializationFormat(self):
        '''
        Get the KG serialization formats. This information is retrived by executing a query on the SPARQL endpoint or from VoID file if available.

        :return: list of serialization formats.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        if isinstance(url,str):
            try:
                formats = q.checkSerialisationFormat(url)
            except:
                formats = 'SPARQL endpoint offline'
                if not isinstance(voidFile,bool):
                    formats = VoIDAnalyses.getSerializationFormats(voidFile)
        elif not isinstance(voidFile,bool):
            formats = VoIDAnalyses.getSerializationFormats(voidFile)
        else:
            formats = 'SPARQL endpoint and VoID file absent'
        
        return formats
    
    def getLanguages(self):
        '''
        Get the languages supported by the KG. This information is retrieved by querying the SPARQL endpoint.
        
        :return: a list with all language supported.
        :rtype: list
        '''
        url = aggregator.getSPARQLEndpoint(self.id)
        if isinstance(url,str):
            try:
                languages = q.getLangugeSupported(url)
            except:
                languages = 'SPARQL endpoint offline'
        else:
            languages = 'SPARQL endpoint absent'
        
        return languages
    
    def getAccessAtKG(self):
        '''
        Get the ways in which you can access the KG. This information is retrived by analyzing the metadata and/or querying the SPARQL endpoint.

        :return: a list with the links to access at the KG.
        :rtype: list
        '''
        links = []
        url = aggregator.getSPARQLEndpoint(self.id)
        voidFile = utils.checkVoidFile(self.id)
        resources = aggregator.getOtherResources(self.id)
        resources = utils.insertAvailability(resources)
        links = links + utils.getLinkDownload(resources)
        if isinstance(url,str):
            links.append(url)
            try:
                urlList = q.checkDataDump(url)
                if isinstance(urlList,list):
                    activeUrl = utils.getActiveDumps(urlList)
                    links = links + activeUrl
            except:
                pass
        elif not isinstance(voidFile,bool):
            links = links + VoIDAnalyses.getDataDump(voidFile)
        
        links = list(dict.fromkeys(links)) #REMOVE DUPLICATES IN THE LIST

        return links
