import sys 
sys.path.append("delivery_network")

from graph import graph_from_file,plus_petit_encetre_commun,kruskal
import unittest   # The test framework

class Test_MinimalPower(unittest.TestCase):
    def test_network0(self):
        g = graph_from_file("input/network.00.in")
        arbrecouvrant=kruskal(g)
        self.assertEqual(plus_petit_encetre_commun(arbrecouvrant,1, 4,3)[0], 11)
        self.assertEqual(plus_petit_encetre_commun(arbrecouvrant,2, 4,3)[0], 10)


if __name__ == '__main__':
    unittest.main()