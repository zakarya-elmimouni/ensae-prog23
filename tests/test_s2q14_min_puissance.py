import sys 
sys.path.append("delivery_network")

from graph import graph_from_file
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network12(self):
        g = graph_from_file("input/network.12.in")
        self.assertEqual(g.puissance_min(1, 4)[1], 3)
        self.assertEqual(g.puissance_min(1, 5)[1],3 )
        self.assertEqual(g.puissance_min(3, 7)[1],3)
        self.assertEqual(g.puissance_min(8, 5)[1],1)
       
if __name__ == '__main__':
    unittest.main()
