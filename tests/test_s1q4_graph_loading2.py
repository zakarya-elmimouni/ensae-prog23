import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file
import unittest   # The test framework
class Test_MST(unittest.TestCase):
    def test_network00(self):

        g = graph_from_file("network.04.in")

        g_excpected = {1: [(2, 4, 89), (4, 11, 6)],

                        2: [(1, 4, 89), (3, 4, 3)],

                        3: [(2, 4, 3), (4, 4, 2)],

                        4: [(1, 11, 6), (3, 4, 2)],

                        5: [],

                        6: [],

                        7: [],

                        8: [],

                        9: [],

                        10: []}

        self.assertEqual(g_mst.graph, mst_expected)