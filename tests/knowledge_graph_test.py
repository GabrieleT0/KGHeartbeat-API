import unittest
from quality_analysis.knowledge_graph import KnowledgeGraph

class KnowledgeGraphTestCase(unittest.TestCase):
    
    def setUp(self):
        self.kg = KnowledgeGraph('taxref-ld')
    
    def testEndpointAv(self):
        result = self.kg.checkEndpointAv()
        self.assertEqual(result,True)
    
if __name__ == '__main__':
    unittest.main()