#il faut implémenter des tests de cette fonction à partir des graphes qu'on connait
# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file,way_from_file,trucks_from_file
import unittest   # The test framework

class Test_MST(unittest.TestCase):
    def test_route11(self):
        g=graph_from_file("input/network.11.in")
        liste_routes = way_from_file("input/routes.11.in")
        liste_camions=trucks_from_file("input/trucks.3.in")
        Budget=7
        resultat=g.liste_trajet_camion_convenable_0(liste_routes,liste_camions,Budget)
        result_expected =(frozenset({((1, 2, 3), (1, 4, 5)), ((1, 2, 3), (1, 2, 10))}), 6, 15.0)
        self.assertEqual(resultat,result_expected)
    def test_route12(self):
        g=graph_from_file("input/network.12.in")
        liste_routes = way_from_file("input/routes.12.in")
        liste_camions=trucks_from_file("input/trucks.4.in")
        Budget=15
        resultat=g.liste_trajet_camion_convenable_0(liste_routes,liste_camions,Budget)
        result_expected =(frozenset({((2, 3, 3), (1, 6, 7)), ((2, 3, 3), (1, 5, 3)), ((2, 3, 3), (1, 4, 10)), ((2, 3, 3), (2, 8, 5)), ((2, 3, 3), (3, 7, 6))}), 15, 31.0)
        self.assertEqual(resultat,result_expected)
if __name__ == '__main__':
    unittest.main()

    