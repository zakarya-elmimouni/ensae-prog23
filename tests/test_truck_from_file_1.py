import sys 
sys.path.append("delivery_network")
from graph import Graph,graph_from_file,way_from_file,trucks_from_file,trucks_from_file_1
import unittest   # The test framework
from time import perf_counter
#trucks.2.in
#1ier cas:
liste_camions=trucks_from_file("input/trucks.2.in")
resultat1=len(liste_camions)
print(resultat1)
#2ème cas:
liste_camions=trucks_from_file_1("input/trucks.2.in")
resultat2=len(liste_camions)
print(resultat2)
#dans le deuxième cas le nombre est diminué de presque la moitié

#trucks.1.in

#1ier cas:
liste_camions=trucks_from_file("input/trucks.1.in")
resultat3=len(liste_camions)
print(resultat3)
#2ème cas:
liste_camions=trucks_from_file_1("input/trucks.1.in")
resultat4=len(liste_camions)
print(resultat4)