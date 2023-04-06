import sys 
sys.path.append("delivery_network")

from graph import graph_from_file,kruskal
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network12(self):
        g = graph_from_file("input/network.12.in")
        arbrecouvrant=kruskal(g)
        self.assertEqual(g.puissance_min(arbrecouvrant,1, 4)[1], 3)
        self.assertEqual(g.puissance_min(arbrecouvrant,1, 5)[1],3 )
        self.assertEqual(g.puissance_min(arbrecouvrant,3, 7)[1],3)
        self.assertEqual(g.puissance_min(arbrecouvrant,8, 5)[1],1)
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        arbrecouvrant=kruskal(g)
        self.assertEqual(g.puissance_min(arbrecouvrant,1, 4)[1], 11)
        self.assertEqual(g.puissance_min(arbrecouvrant,2, 4)[1], 10)
    
if __name__ == '__main__':
    unittest.main()
