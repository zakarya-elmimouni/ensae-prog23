#test de comparaison du temps d'exécusion de la fonction qui retourne la liste des camions et des trajets correspondants
#1 ier cas sans éliminer les camions non utiles et le 2ème avec élimination
import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file,way_from_file,trucks_from_file,EnsembleDisjoint,trucks_from_file_1
import unittest   # The test framework
from time import perf_counter
#une comparaison entre le premier cas et le deuxième cas
#permier cas (force brute)
#le premier cas est un cas 
#g=graph_from_file("input/network.2.in")
#liste_routes = way_from_file("input/routes.2.in")
#deuxième cas (sans élimination des éléments inutiles)
temps1_cas2=perf_counter()
liste_camions=trucks_from_file("input/trucks.2.in")
resultat1=len(liste_camions)
Budget=25*10**3
#resultat1=g.liste_trajet_camion_convenable(liste_routes,liste_camions,Budget)
temps2_cas2=perf_counter()
time2=temps2_cas2-temps1_cas2

#pour le deuxième cas (lorsque on a éliminer les élements non utiles)
temps1_cas3=perf_counter()
liste_camions=trucks_from_file_1("input/trucks.2.in")
resultat2=len(liste_camions)
Budget=25*10**3
#resultat=g.liste_trajet_camion_convenable(liste_routes,liste_camions,Budget)
temps2_cas3=perf_counter()
time3=temps2_cas3-temps1_cas3
#print("temps1:",time1)
#print("temps2:",time2)
#print("temps3:",time3)
print("cas1",resultat1)
print("cas2",resultat2)