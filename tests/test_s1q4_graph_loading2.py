import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file
import unittest   # The test framework
class Test_MST(unittest.TestCase):
    def test_network04(self):
        g = graph_from_file("input/network.04.in")
        g_excpected = { 1: [(4, 11, 6), (2, 4, 89)],
                        2: [(3, 4, 3), (1, 4, 89)],
                        3: [(2, 4, 3), (4, 4, 2)],
                        4: [(3, 4, 2), (1, 11, 6)],
                        5: [],
                        6: [],
                        7: [],
                        8: [],
                        9: [],
                        10: []}
        self.assertEqual(g.graph,g_excpected)
    def test_network05(self):
        g = graph_from_file("input/network.05.in")
        g_excpected = { 1:  [(2, 6, 1), (3, 2, 1), (4, 4, 1)],
                        2:  [(1, 6, 1), (3, 7, 1), (4, 8, 1)],
                        3:  [(1, 2, 1), (2, 7, 1), (4, 5, 1)],
                        4:  [(1, 4, 1), (2, 8, 1), (3, 5, 1)]}
        self.assertEqual(g.graph,g_excpected)
if __name__ == '__main__':
    unittest.main()
