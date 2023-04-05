from time import perf_counter
from random import randint
from graphviz import Digraph
class EnsembleDisjoint:
    """
    Cette classe permet de gérer les ensmebles disjoints. Deux éléments sont
    considérés dans le même ensemble s'ils ont le même parent.
    """
    parent = {}

    # Création de n ensemble disjoints, état de départt de notre graphe
    def __init__(self,g):
        for element  in g.nodes:
            self.parent[element] = element

    # Fonction qui permet de retrouver le parent le plus lointain
    def get_parent(self, k):
        if self.parent[k] != k:
            self.parent[k]=self.get_parent(self.parent[k])
        return self.parent[k]

    # Union de deux ensembles jusque là disjoints
    def Union(self, a, b):
        x = self.get_parent(a)
        y = self.get_parent(b)
        self.parent[x] = y
class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.power=[]
        self.edges=[]

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    

    #Question 1

    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        #On vérifie d'abord si les noeuds de notre nouevlle arrette existe déja dans notre graph, sinon on les ajoute
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1

    #Question 3 ( voir la suite de la question 3 aussi)
    
    def get_path_with_power(self,src, dest, power):
# un petit developpement de la fonction get_precedent pour avoir le chemin
        def get_precedent(graph,depart,arrivée,power):
            precedent={x:None for x in graph.keys()}
            visited_nodes={x:False for x in graph.keys()}
            pile=[depart]
            visited_nodes[depart]=True
            while pile:
                sommet=pile.pop()
                liste_nouveau_sommets_voisins=[voisin for voisin in graph[sommet]if not visited_nodes[voisin[0]]]
                for voisin in liste_nouveau_sommets_voisins:
                    if voisin[1]<=power:
                        precedent[voisin[0]]=sommet
                        visited_nodes[voisin[0]]=True
                        if voisin[0] ==arrivée:
                            return precedent
                        else:
                            pile.append(voisin[0])
            return precedent
        precedent=get_precedent(self.graph,src,dest,power)
        depart=src
        arrivée=dest
        if precedent[arrivée]== None:
            return None
        else:
            path=[]
            dernier=arrivée
            while dernier!=depart:
                path.append(dernier)
                dernier=precedent[dernier]
            path.append(depart)
            path.reverse()
            return path

        # la complexité de get_path_with_power est la même que la complexité de la fonction get_precedent
        # C'est une complexité de l'ordre O(V**2) , avec V le nombre de sommets.
           
#Question 5 : le chemin le plus court 
    def plus_court_chemin(self,src, dest, power):
        distance, precedent=dijkstra(self.graph,src,power)
    
        if distance[dest]== "inf":
            return None
        else:
            path=[]
            dernier=dest
            while dernier!=src:
                path.append(dernier)
                dernier=precedent[dernier]
            path.append(src)
            path.reverse()
            return path,distance[dest]
#un pont à améliorer dans ce programme c'est de faire un teste de composante connxe au début
#si le depart et l'arrivée ne sont pas dans la meme composante connexes on va pas se casser la tete
#dans ce cas ça vaut pas le cout de passer par l'algorithme de dijkstra qui de complexité assez grande 
    
    def connected_components(self):
        composantes_connexes=[]
        visited_nodes={noeud:False for noeud in self.nodes}

        def deep_parcours(s):
            composantes=[s]
            for neighboor in self.graph[s]:
                neighboor=neighboor[0]
                if not visited_nodes[neighboor]:
                    visited_nodes[neighboor]=True
                    composantes+=deep_parcours(neighboor)
            return composantes
        
        for s in self.nodes:
            if not visited_nodes[s]:
                composantes_connexes.append(deep_parcours(s))
        return composantes_connexes
    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    #Question 6

    # le programme de la question 6 est basée sur une recherche dichotomique
    #début 0 et fin égale au max des puissances des arretes
    def min_power(self, src, dest):
        if self.get_path_with_power(src,dest,float('inf'))!=None:
            self.power.sort()
            fin=len(self.power)-1
            debut=0
            milieu=(fin+debut)//2
            while debut<fin:
                if self.get_path_with_power(src,dest,self.power[milieu])!=None:
                    fin=milieu
                else:
                    debut=milieu+1
                milieu=(debut+fin)//2
            return self.get_path_with_power(src,dest,self.power[milieu]), self.power[debut]
        raise Exception('pas de chemin')
     #Question 7 

    def graphique(self) :
         # Création du graphe avec Graphviz
        dot = Digraph()
        for node in self.graph:
            dot.node(str(node))
        for node in self.graph:
            for edge in self.graph[node]:
                dot.edge(str(node), str(edge[0]), label=str(edge[1]))
        # Affichage du graphe
        dot.render('graph')
    #Question 14
    
    def puissance_min(self,src,dest):#recherche de la puissance minimale dans l'arbre couvrant
        fin=0
        debut=0
        arbre_couvrant=kruskal(self)
        arbre_couvrant=arbre_couvrant.graph
        power=[]
        for sommet in arbre_couvrant.keys():#recherche de la puissance maximale des arretes
            for voisin in arbre_couvrant[sommet]:
                power.append(voisin[1])
                  #récuperation du maximum
        if self.get_path_with_power(src,dest,float('inf'))!=None:
            power.sort()
            fin=len(power)-1
            debut=0
            milieu=(fin+debut)//2
            while debut<fin:
                if self.get_path_with_power(src,dest,power[milieu])!=None:
                    fin=milieu
                else:
                    debut=milieu+1
                milieu=(debut+fin)//2
            return self.get_path_with_power(src,dest,power[milieu]),power[milieu]
        raise Exception('pas de chemin')
    #Question 1 séance4:
        #Manière 1 : Brute force
    # On définira une fonction qui retourne une liste avec tous les trajets et le meilleur camion associé
    # Le meilleur camion qu'on peut associer à chaque trajet est évidement un camion qui peut passer
    # Et dont le coût est minimal
    def collection(self,liste_trajets,liste_camions):
        G = self.graph
        W = liste_trajets
        T = liste_camions
        for i in range(len(W)) :
            L,a = self.puissance_min(W[i][0], W[i][1])
            W[i]= [W[i][0],W[i][1],a,W[i][2]]
        # On trie les camions selon la 2 ème variable (le coût)
        T.sort(key = lambda x :x[2] )
        R = []
        for i in range(len(W)):
            b = T[0][1]
            j=0
             # On cherche le premier qui peut passer et dont le coût est le plus petit
            while b < W[i][2]:
                j=j+1
                b=T[j][1]
            R.append([W[i][0],W[i][1],W[i][2],W[i][3],T[j][0],T[j][1],T[j][2]])
        return R

    # On cherche maintenant à trouver la combinaison de trajets qui soit optimale
    def liste_trajet_camion_convenable_0(self,liste_trajets,liste_camions,Budget):
            # Nous allons définir une fonction intermédiaire qui retourne toutes les parties d'un ensemble
    # En l'occurence ici ça sera une liste et on retournera une liste avec toutes les parties (P(E))
        def partiesliste(L):
            P = []
            i, i_max = 0, 2**len(L)-1
            while i <= i_max:
                s = []
                j, j_max = 0, len(L)-1
                while j <= j_max:
                    if (i>>j)&1 == 1:
                        s.append(L[j])
                    j += 1
                P.append(s)
                i += 1 
            return P
        R = self.collection(liste_trajets,liste_camions)
        P = partiesliste(R)
        T = []
    # Nous allons calculer l'utilité totale pour toutes les parties de notre listes ( 2**len(L))
        for i in range(1,len(P)) :
            u = 0
            c = 0
            L=P[i]
        
            # On regarde les combinaisons de trajets dont les camions vérifie la contrainte de budget
            for j in range(len(L)) : 
                B = L[j]
                c = c + B[6]
                u = u + B[3]
            if c <= Budget :
                L.append(u)
                L.append(c)
                T.append(L)
            # On trie les différentes combinaisons selon l'utilité totale en ordre décroissant
        T.sort(key = lambda x :x[-2] , reverse=True)
        Z=[]
        L=[]
        for element in T[0][:-2]:
            D=[(element[4],element[5],element[6])] 
            G=[(element[0],element[1],element[3])] 
            Z.append(tuple(D+G))
        L.append(frozenset(Z))
        L.append(T[0][-1])
        L.append(T[0][-2])
        return tuple(L)

    def maximiser_profit_cout(self,liste_camions,liste_trajets):
    
        '''---input---
    liste_camions va etre une liste ayyant la forme [(camion,puissance,cout)]
    liste_trajets va etre un liste de tous les trajets possibles [(debut,fin,profit)]
    ---outpout---
    dictionnaire qui comporte chaque aretes associé au rapport profit/cout maximal
    ainsi que le caion associé à ce rapport'''
        dict_profit_cout={}#ce dictionnaire va contenir chaque trajet avec un rapport profit-cout maximal et le camion qui verifie ce rapport 
    #liste_trajets va etre un liste de tous les trajets possibles [(debut,fin,profit)]
    #liste_camions va etre une liste ayyant la forme [(camion,puissance,cout)]
        """"je vais definir une liste de puissance minimale de chaque trajet"""
        #puissance_min_trajets={trajet:self.puissance_min(trajet[0],trajet[1])[1]for trajet in liste_trajets}
        puissance_min_trajets={}
        for trajet in liste_trajets:
            depart=trajet[0]
            arrivée=trajet[1]
            liste,puissance_min=self.puissance_min(depart,arrivée)
            puissance_min_trajets[trajet]=puissance_min
        for trajet in liste_trajets:
            profit_trajet=trajet[2]
            max_profit_cout=0
            for camion in liste_camions:
                puissance_camion=camion[1]
                cout_camion=camion[2]
                if puissance_camion>=puissance_min_trajets[trajet]:
                    if (profit_trajet/cout_camion)>max_profit_cout:
                        max_profit_cout=profit_trajet/cout_camion
                        dict_profit_cout[trajet]=[max_profit_cout,camion]
        return dict_profit_cout
    def liste_trajet_camion_convenable(self,liste_trajets,liste_camions,Budget):
        """"output
    --------------
    liste_finale: la liste des trajets avec les camion correspondants 
    elle est sous la forme [(trajet,[rapport_max,camion_correspondant à ce trajet])]
    cout_total: c'est le cout qu_on a dépensé <=B 
    profit_total:le profit qu'on a obtenu"""
        dict_profit_cout=self.maximiser_profit_cout(liste_camions,liste_trajets)
        liste_trajet_profit_cout_triée= sorted(dict_profit_cout.items(), key=lambda item:item[1][0],reverse=True)

    #liste trié selon raport_maximale de chaque trajet sous la forme [(trajet,[rapport_amx,camion])]
    
        liste_finale=[]#c'est juste un troncation de la liste_trajet_profit_cout_triée
        cout_totale=0
        profit_totale=0
        i=0 #indice d'itération
        while cout_totale<=Budget and i<len(liste_trajet_profit_cout_triée):
            liste_finale.append(liste_trajet_profit_cout_triée[i])
            camion=liste_trajet_profit_cout_triée[i][1][1]
            cout_camion=camion[2]
            cout_totale=cout_camion+cout_totale
            rapport_max=liste_trajet_profit_cout_triée[i][1][0]
            profit_totale+=rapport_max*cout_camion
            i+=1
        if cout_totale>Budget:
            cout_totale=cout_totale-cout_camion   #on retire le cout du dernier camion ajouté
            profit_totale=profit_totale-rapport_max*cout_camion  #on retire le profit du dernier trajet ajouté
            liste_finale.remove(liste_trajet_profit_cout_triée[i-1])
        output_liste=[]#Une liste sous la forme [(camion,trajet)]
        for element in liste_finale:
            output_liste.append((element[1][1],element[0]))
        
        return frozenset(output_liste),cout_totale,profit_totale
    #une première amélioration qu'on pourra rajouter au code est d'iliminer certains camionq de la liste des camion à traiter
#par exemple si un camion est de puissance petite alors que sont cout est grand
#la meme chose pour un trajet 
# si un trajet est de puissance minimale très grande alors que son profit est bas on le supprime
    def iliminer_elements_inutiles(self,liste_camions):
    #liste_camions a la meme forme [(camion,puissance,cout)]
    #liste_trajets a aussi la meme forme:
        nb_initial_camions=len(liste_camions)
        print(nb_initial_camions)
        liste_initiale=liste_camions.copy()
        for i in range (nb_initial_camions):
            print(i)
            for j in range (i+1,nb_initial_camions):
                print(j)
                if j==nb_initial_camions:
                    break
                camion1=liste_initiale[i]
                camion2=liste_initiale[j]
                cout1=camion1[2]
                cout2=camion2[2]
                puissance1=camion1[1]
                puissance2=camion2[1]
                if cout1<=cout2 and puissance1>=puissance2:
                    if camion2 in liste_camions:
                        liste_camions.remove(camion2)
        return nb_initial_camions,len(liste_camions),liste_camions

    #une première amélioration qu'on pourra rajouter au code est d'iliminer certains camionq de la liste des camion à traiter
#par exemple si un camion est de puissance petite alors que sont cout est grand
#la meme chose pour un trajet 
# si un trajet est de puissance minimale très grande alors que son profit est bas on le supprime
def iliminer_elements_inutiles(liste_camions):
    #liste_camions a la meme forme [(camion,puissance,cout)]
    #liste_trajets a aussi la meme forme:
    nb_initial_camions=len(liste_camions)
    for i in range (len(liste_camions)):
        for j in range (i,len(liste_camions)):
            camion1=liste_camions[i]
            camion2=liste_camions[j]
            cout1=camion1[2]
            cout2=camion2[2]
            puissance1=camion1[1]
            puissance2=camion2[1]
            if cout1<=cout2 and puissance1>=puissance2:
                liste_camions.remove()
    return nb_initial_camions,len(liste_camions),liste_camions
#Question 10

def temps_moyen(file1,file2):
    g = graph_from_file(file1)
    L = way_from_file(file2)
    n=len(L)
    Times = []
    M = n//10
    i = 0
    S=0
    while i < M :
        t1 = perf_counter()
        a = Graph.puissance_min(g, L[i][0], L[i][1])
        t2 = perf_counter()
        Times.append(t2-t1)
        S = S + (t2-t1)
        i = i+1
    return S/i

#Question 11
#     On utilise l'absurde, on suppose qu'il y a un chemin plus court qui n'est pas dans l'arbre couvrant,

#  il suffira après de remplacer chaque arrete de ce nouveau chemin par une ou plusieurs arretes reliant les 2 mêmes points qui spnt dans l'arbre couvrant(c'est le principe même de l'arbre couvrant),

#  mais puisqu'elle sont dans l'arbre couvrant donc la puissance est minimale, et donc on aura pu trouver un trajet d'une puissance encore plus petite

# ==> Contradiction

#Question 13

#Question 15

# Réponse : la complexité totale de la fonction basée sur l’arbre couvrant de poids minimal 

# qui calcule la puissance minimale d'un camion pour couvrir un trajet donné 

# est donc de O(nb_edges.log (nb_nodes))("ce lui du tri rapide de kruskal") + O(nb_edges+nb_nodes), 

# qui est équivalent à O(nb_edges.log(nb_nodes))

def nouveau_temps_moyen(file1,file2):
    g = graph_from_file(file1)
    g_mst= kruskal(g)
    L= way_from_file(file2)
    n= len(L)
    Times = []
    M = n//10
    i = 0
    S=0
    while i < M :
        t1 = perf_counter()
        a = Graph.puissance_min(g_mst.graph, L[i][0], L[i][1])
        t2 = perf_counter()
        Times.append(t2-t1)
        S = S + (t2-t1)
        i = i+1
    return S/i 
#Question 1 (suite)
        
def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
                g.power.append(power_min)
                g.edges.append((node1,node2,power_min,1))
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
                g.power.append(power_min)
                g.edges.append((node1, node2, power_min, dist))
            else:
                raise Exception("Format incorrect")
    return g
def way_from_file(filename):
    with open(filename,"r") as file : 
        n= int(file.readline())
        W = []
        for _ in range(n):
            way = list(map(int,file.readline().split()))
            way=tuple(way)
            if len(way)== 3 :
                W.append(way)
            else : 
                raise Exception("Format incorrect")
    return W 

def trucks_from_file(filename): 
    with open(filename,"r") as file :
        n= int(file.readline())
        T=[]
        for i in range(n):
            truck = list(map(int,file.readline().split()))
            truck=tuple(truck)
            if len(truck) == 2 :
                T.append((i+1,truck[0],truck[1]))
            else :
                raise Exception("Format incorrect")
    return T



#Question 5
#recherche du chemin le plus court à l'aide de dijkstra
#algorithme de dijikstra
#graph={sommet:["liste des sommets lié à ce sommet, chaque sommet est sous la forme d'un tuple(sommet,power, distance)"]
def dijkstra(graph,source,puissance_camion):
        precedent = {x:None for x in graph.keys()}#les précedents des sommets dans le trajet minimal
        dejaTraite = {x:False for x in graph.keys()}#l'element est déja traité? False ou True
        distance =  {x:float('inf') for x in graph.keys()}#la distance de l'origine à chaque sommet
        distance[source] = 0 #initialisation : la distance de l'origine à l'origine c"est 0
        a_traiter = [(0, source)]#il contient la liste des maison à evaluer. aen initialisation on met notre orgine avec une distance de 0
        while a_traiter:#tant qu'il a des element à traiter on va parcourir la boucle
        # on fait parcours en larguer : une fois un element et traité on parcourt ses voisins et puis les voisins des voisins etc...
            dist_noeud, noeud = a_traiter.pop()
            if not dejaTraite[noeud]:
                dejaTraite[noeud] = True
                for voisin in graph[noeud]:#graph[noued] est une liste
                    if voisin[1]<=puissance_camion:
                        dist_voisin = dist_noeud + voisin[2]
                        if dist_voisin < distance[voisin[0]]:
                            distance[voisin[0]] = dist_voisin
                            precedent[voisin[0]] = noeud
                            a_traiter.append((dist_voisin, voisin[0]))
            a_traiter.sort(reverse=True)
        return distance, precedent


# Question 3 (suite)
def get_precedent(graph,depart,arrivée,power):
    precedent={x:None for x in graph.keys()}
    visited_nodes={x:False for x in graph.keys()}
    pile=[depart]
    visited_nodes[depart]=True
    while pile:
        sommet=pile.pop()
        liste_nouveau_sommets_voisins=[voisin for voisin in graph[sommet]if not visited_nodes[voisin[0]]]
        for voisin in liste_nouveau_sommets_voisins:
            if voisin[1]<=power:
                precedent[voisin[0]]=sommet
                visited_nodes[voisin[0]]=True
                if voisin[0] ==arrivée:
                    return precedent
                else:
                    pile.append(voisin[0])
    return precedent



#Question 11

#     On utilise l'absurde, on suppose qu'il y a un chemin plus court qui n'est pas dans l'arbre couvrant,
#  il suffira après de remplacer chaque arrete de ce nouveau chemin par une ou plusieurs arretes reliant les 2 mêmes points qui spnt dans l'arbre couvrant(c'est le principe même de l'arbre couvrant),
#  mais puisqu'elle sont dans l'arbre couvrant donc la puissance est minimale, et donc on aura pu trouver un trajet d'une puissance encore plus petite
# ==> Contradiction


#Question 15

# Réponse : la complexité totale de la fonction basée sur l’arbre couvrant de poids minimal qui calcule la puissance minimale d'un camion pour couvrir un trajet donné est donc de O(U.log (V))("ce lui du tri rapide de kruskal") + O(U+V), qui est équivalent à O(U.log(V)), où U est le nombre d'arretes et V le nombre de sommets(ou noeuds)

def nouveau_temps_moyen(file):
    g = graph_from_file(file)
    K= g.keys()
    a=len(K)
    i = 0
    L=[]
    S=0
    while i < 31 :
        n= randint(0, a-1)
        m= randint(0,a-1)
        if n!=m :
            t1 = perf_counter()
            a = Graph.puissance_min(g, K[n],K[m])
            t2 = perf_counter()
            L.append(t2-t1)
            S = S + t2-t1
            i = i+1
    return S/i

def kruskal(g):
    """
    Construction de l'arbre couvrant minimum à l'aide de l'algorithme de Kruskal
    Les paramètres sont :
        - Les arcs du graphe au format (début, fin, longueur)
        - Le nombre de sommets dans le graph
    """
    edges=g.edges
    edges.sort(key=lambda x: x[2])
    Arbre_couvrant =Graph([])
    ed = EnsembleDisjoint(g)
    index = 0
    while Arbre_couvrant.nb_edges!= g.nb_nodes - 1:

        (src, dest, weight,dist) = edges[index]
        index = index + 1

        x = ed.get_parent(src)
        y = ed.get_parent(dest)

        if x != y:
            Arbre_couvrant.add_edge(src, dest, weight,dist)
            ed.Union(x, y)
    return Arbre_couvrant
def profondeur (root,arbre_couvrant):
    """ça retourne un dictionnaire {'sommet':profondeur}"""
    visited_nodes={node:False for node in arbre_couvrant.nodes}
    profondeur={node:None for node in arbre_couvrant.nodes}
    peres={node:None for node in arbre_couvrant.nodes}
    pile=[]
    peres[root]=[root,0]
    pile.append(root)
    profondeur[root]=0
    while pile:
        pere=pile.pop()
        for voisin in arbre_couvrant.graph[pere]:
            if not visited_nodes[voisin[0]]:
                profondeur[voisin[0]]=profondeur[pere]+1
                visited_nodes[voisin[0]]=True
                peres[voisin[0]]=[pere,voisin[1]]
                pile.append(voisin[0])
    return profondeur,peres

def plus_petit_encetre_commun(arbre_couvrant,src,dest,root):
    peres=profondeur(root,arbre_couvrant)[1]
    liste_ancetres_src=[[src,0]]
    liste_ancetres_dest=[[dest,0]]
    element=src
    while element!=root: # O(V)
        liste_ancetres_src.append(peres[element])
        element=peres[element][0]
    liste_ancetres_src.append([root,0])
    element=dest
    while element!=root:
        liste_ancetres_dest.append(peres[element])
        element=peres[element][0]
    liste_ancetres_dest.append([root,0])
    #détermination du plus petit encetre commun 
    for i in range(len(liste_ancetres_dest)):
        for j in range(len(liste_ancetres_src)):
            ancetre_dest_couple=liste_ancetres_dest[i]
            ancetre_src_couple=liste_ancetres_src[j]
            ancetre_dest=ancetre_dest_couple[0]
            ancetre_src=ancetre_src_couple[0]
            if ancetre_src==ancetre_dest:#ancetre commun
                indice_dest=i
                indice_src=j
                break
    liste_src=liste_ancetres_src[:indice_src]
    #print(type(liste_src))
    liste_dest=liste_ancetres_dest[:indice_dest-1]
    liste_dest.reverse()
    chemin=liste_src+liste_dest
    #le chemin est donc liste_src+liste_dest
    #determination du power min
    puissance_min=max(node[1]for node in chemin)
    return puissance_min,chemin

#Question 1 Séance 4 :









            

    




    


    

    
