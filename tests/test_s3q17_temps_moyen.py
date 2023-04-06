import sys 
sys.path.append("delivery_network")
from graph import temps_moyen_3
import unittest   # The test framework
print("tempsmoyens_routes.2_pluspetitancetrecommun",temps_moyen_3("input/network.2.in","input/routes.2.in"))
print("tempsmoyens_routes.4_pluspetitancetrecommun",temps_moyen_3("input/network.4.in","input/routes.4.in"))



