#calcul de temps pour calculer la puissance moyenne de tous les trajets dans le fichier routes.4
import sys 
sys.path.append("delivery_network")
from graph import  temps_totale

print("temps_totale_routes.2",temps_totale("input/network.2.in","input/routes.2.in"))