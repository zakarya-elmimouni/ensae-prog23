import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file
import unittest   # The test framework
class Test_MST(unittest.TestCase):
    def test_network00(self):

        g = graph_from_file("input/network.04.in")

        g_excpected = { 1: [(4, 11, 6),(2, 4, 89)],
             
                        2: [(3, 4, 3), (1, 4, 89)],

                        3: [(2, 4, 3), (4, 4, 2)],

                        4: [(3, 4, 2), (1, 11, 6)]}

        self.assertEqual(g.graph,g_excpected)

print(graph_from_file("input/network.04.in"))
    
if __name__ == '__main__':
    unittest.main()
