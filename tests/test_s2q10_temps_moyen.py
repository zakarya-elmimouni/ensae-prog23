
import sys 
sys.path.append("delivery_network")
from graph import  temps_moyen_1,temps_moyen_2 
#print("tempsmoyens_routes.1",temps_moyen("input/network.1.in","input/routes.1.in"))
print("tempsmoyens_routes.2_power_min",temps_moyen_1("input/network.2.in","input/routes.2.in"))
print("tempsmoyens_routes.4_power_min",temps_moyen_1("input/network.4.in","input/routes.4.in"))
