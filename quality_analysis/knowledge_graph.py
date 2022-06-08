import aggregator
from quality_analysis.DataHubAPI import getLicense
import query as q
import utils
import VoIDAnalyses
import Graph
from SPARQLWrapper import SPARQLExceptions

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
        :rtype: boolean
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
        :rtype: boolean
        '''
        resources = aggregator.getOtherResources(self.id)
        resources = utils.insertAvailability(resources)
        available = utils.checkAvailabilityForDownload(resources)

        return available
    
    def checkInactiveLinks(self):
        '''
        Check if there are inactive link associated with the KG.

        :return: The availability of links.
        :rtype: boolean
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
        
        :return: machine-redeable license 
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

        :return: human-redeable license
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
        
        :return: degree of connection
        :rtype: int
        '''
        graph = utils.checkGraphFile()
        degree = Graph.getDegreeOfConnection(graph,self.id)
        return degree
    
    def getClusteringCoefficient(self):
        '''
        Get the clustering coefficient of kg in the graph constructed with all the kg discoverable.
        At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch.
        
        :return: local clustering coeffcient
        :rtype: float
        '''
        graph = utils.checkGraphFile()
        lcc = Graph.getClusteringCoefficient(graph,self.id)
        
        return lcc
    
    def getCentrality(self):
        '''
        Get the centrality of kg in the graph constructed with all the kg discoverable.
        At the first call of a function of the interlinking metric a file is created in the directory which contains the graph with all kg discoverable, this is to avoid the construction of the graph every time from scratch.
        
        :return: centrality
        :rtype: float
        '''
        graph = utils.checkGraphFile()
        centrality = Graph.getCentrality(graph,self.id)

        return centrality

    def getSameAsChains(self):
        '''
        Return the number of sameAs chains, counting the triples with the predicate equal to owl:sameAs.

        :return: number of sameAs chains
        :rtype: int
        '''
        try:
            url = aggregator.getSPARQLEndpoint(self.id)
            numSameAs = q.getSameAsChains(url)
        except Exception as e:
            numSameAs = e

        return numSameAs

    def getExternalProvider(self):
        '''
        Return a dict with all external provider the key is the id of the KG it is connected to and the value is the number of triples connected, this information is obtained by analyzing the metadata.

        :return: external provider dictonary
        :rtype: dict
        '''

        extLinks = aggregator.getExternalLinks(self.id)

        return extLinks

kg = KnowledgeGraph('taxref-ld')
lic = kg.getExternalProvider()
print(lic)