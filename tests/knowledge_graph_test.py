import unittest
from kg_qa.knowledge_graph import KnowledgeGraph

class KnowledgeGraphTestCase(unittest.TestCase):
    
    def setUp(self):
        self.kg = KnowledgeGraph('taxref-ld')
    
    def testEndpointAv(self):
        result = self.kg.checkEndpointAv()
        self.assertEqual(result,True)

    def testDownload(self):
        result = self.kg.checkDownload()
        self.assertEqual(result,True)
    
    def testInactiveL(self):
        result = self.kg.checkInactiveLinks()
        self.assertEqual(result,True)
    
    def testLicenseMR(self):
        result = self.kg.getLicenseMR()
        self.assertEqual(type(result),str)
    
    def testLicenseHR(self):
        result = self.kg.getLicenseHR()
        self.assertEqual(result,False)

    def testDegreeConn(self):
        result = self.kg.getDegreeOfConnection()
        self.assertEqual(result,7)
    
    def testCC(self):
        result = self.kg.getClusteringCoefficient()
        self.assertEqual(result,0.048)
    
    def testCentrality(self):
        result = self.kg.getCentrality()
        self.assertEqual(result,0.003769520732364028)
    
    def testSameAs(self):
        result = self.kg.getSameAsChains()
        self.assertEqual(result,254729)

    def testExPr(self):
        result = self.kg.getExternalProvider()
        self.assertEqual(type(result),dict)
    
    def testAuth(self):
        result = self.kg.checkAuth()
        self.assertEqual(result,False)
    
    def testHttps(self):
        result =  self.kg.checkHTTPS()
        self.assertEqual(result,True)
    
    def testLatency(self):
        result = self.kg.getLatency()
        self.assertEqual(type(result),float)
    
    def testTP(self):
        result = self.kg.getThroughput()
        self.assertEqual(type(result),float)
    
    def testEmptyL(self):
        result = self.kg.checkEmptyLabel()
        self.assertEqual(result,0)
    
    def testDataType(self):
        result = self.kg.checkDatatypeProblem()
        self.assertEqual(result,0)
    
    def testWS(self):
        result = self.kg.checkWhiteSpace()
        self.assertEqual(result,0)
    
    def testDisjoint(self):
        result = self.kg.getDisjointValue()
        self.assertEqual(result,0.0)
    
    def testUndfClass(self):
        result = self.kg.getUndefinedClass()
        self.assertEqual(len(result),0)
    
    def testUndefPr(self):
        result = self.kg.getUndefinedProp()
        self.assertEqual(len(result),0)
    
    def testDeprecated(self):
        result = self.kg.checkDeprecatedClassesProp()
        self.assertEqual(len(result),0)
    
    def testOH(self):
        result = self.kg.checkOntologyHijacking()
        self.assertEqual(result,True)
    
    def testMispClass(self):
        result = self.kg.checkMisplacedClasses()
        self.assertEqual(len(result),3)
    
    def testMispPr(self):
        result = self.kg.checkMisplacedProperty()
        self.assertEqual(len(result),0)
    
    def testIntC(self):
        result = self.kg.getIntensionalConc()
        self.assertEqual(result,0.989)
    
    def testExC(self):
        result = self.kg.getExtensionaConc()
        self.assertEqual(result,0.986)
    
    def testPR(self):
        result = self.kg.getPageRank()
        self.assertEqual(result,0.0011)
    
    def testName(self):
        result = self.kg.getName()
        self.assertEqual(type(result),str)
    
    def testDescr(self):
        result = self.kg.getDescription()
        self.assertEqual(type(result),str)
    
    def testUri(self):
        result = self.kg.getUri()
        self.assertEqual(result,'https://inpn.mnhn.fr/programme/referentiel-taxonomique-taxref?lg=en')
    
    def testTrustV(self):
        result = self.kg.calculateTrustValue()
        self.assertEqual(result,0.75)
    
    def testVocabs(self):
        result = self.kg.getVocabularies()
        self.assertEqual(len(result),29)
    
    def testAuth(self):
        result = self.kg.getAuthors()
        self.assertEqual(type(result),list)
    
    def testPubl(self):
        result = self.kg.getPublishers()
        self.assertEqual(type(result),list)
    
    def testContrib(self):
        result = self.kg.getContributors()
        self.assertEqual(type(result),list)
    
    def testSources(self):
        result = self.kg.getSources()
        self.assertEqual(result.web,'https://inpn.mnhn.fr/programme/referentiel-taxonomique-taxref?lg=en')
    
    def testSign(self):
        result = self.kg.checkSign()
        self.assertEqual(result,False)
    
    def testCreationD(self):
        result = self.kg.getCreationDate()
        self.assertEqual(result,'2007-01-01')
    
    def testModificationD(self):
        result = self.kg.getModificationDate()
        self.assertEqual(result,'2015-10-06')
    
    def testPercUp(self):
        result = self.kg.getPercentageUpData('2015-10-06')
        self.assertEqual(result,2)
    
    def testLastUp(self):
        result = self.kg.getLastUp()
        self.assertEqual(type(result),int)
    
    def testFrequency(self):
        result = self.kg.getFrequencyUp()
        self.assertEqual(result[0],'http://purl.org/linked-data/sdmx/2009/code#freq-A')
    
    def testInterlC(self):
        result = self.kg.getInterlinkingComp()
        self.assertEqual(result,0.0)
    
    def testNumTriples(self):
        result = self.kg.getNumTriples()
        self.assertEqual(type(result),int)
    
    def testNumEnt(self):
        result = self.kg.getNumEntities()
        self.assertEqual(type(result),int)
    
    def testNumPr(self):
        result = self.kg.getNumProperty()
        self.assertEqual(type(result),int)
    
    def testUriLenSub(self):
        result = self.kg.getUriLenghtSub()
        self.assertEqual(type(result),list)
    
    def testUriLenPr(self):
        result = self.kg.getUriLenghtPr()
        self.assertEqual(type(result),list)
    
    def testUriLenObj(self):
        result = self.kg.getUriLenghtObj()
        self.assertEqual(type(result),list)
    
    def testRDFStr(self):
        result = self.kg.checkRDFStr()
        self.assertEqual(result,True)
    
    def testReuseTerms(self):
        result = self.kg.checkReuseTerms()
        self.assertEqual(result,False)
    
    def testReuseVocabs(self):
        result = self.kg.checkReuseVocabs()
        self.assertEqual(result,False)

    def testNumLabels(self):
        result = self.kg.getNumLabels()
        self.assertEqual(result,10943343)
    
    def testRegex(self):
        result = self.kg.getRegex()
        self.assertEqual(len(result),2)
    
    def testExample(self):
        result = self.kg.checkExample()
        self.assertEqual(result,True)
    
    def testNumBN(self):
        result = self.kg.getNumbBN()
        self.assertEqual(result,26003137)
    
    def testSerialFormats(self):
        result = self.kg.getSerializationFormat()
        self.assertEqual(len(result),3)

    def testLang(self):
        result = self.kg.getLanguages()
        self.assertEqual(type(result),list)

    def testAccessKG(self):
        result = self.kg.getAccessAtKG()
        self.assertEqual(len(result),4)    



    
    

if __name__ == '__main__':
    unittest.main()