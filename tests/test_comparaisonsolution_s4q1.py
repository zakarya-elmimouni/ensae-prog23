#test de comparaison du temps d'exécusion de la fonction qui retourne la liste des camions et des trajets correspondants
#1 ier cas sans éliminer les camions non utiles et le 2ème avec élimination
import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file,way_from_file,trucks_from_file,EnsembleDisjoint
import unittest   # The test framework
from time import perf_counter
#une comparaison entre le premier cas et le deuxième cas
#permier cas (sans éliminer les éléments inutiles)
temps1_cas1=perf_counter()
g=graph_from_file("input/network.12.in")
liste_routes = way_from_file("input/routes.12.in")
liste_camions=trucks_from_file("input/trucks.03.in")
Budget=20
resultat=g.liste_trajet_camion_convenable(liste_routes,liste_camions,Budget)
temps2_cas1=perf_counter
time1=temps2_cas1-temps1_cas1

#pour le deuxième cas (lorsque on a éliminer les élements non utiles)
temps1_cas2=perf_counter()
g=graph_from_file("input/network.12.in")
liste_routes = way_from_file("input/routes.12.in")
liste_camions=trucks_from_file("input/trucks.03.in")
liste_camions=g.iliminer_elements_inutiles(liste_camions)
Budget=20
resultat=g.liste_trajet_camion_convenable(liste_routes,liste_camions,Budget)
temps2_cas2=perf_counter
time2=temps2_cas2-temps1_cas2
print("temps1:",time1)
print("temps2:",time2)