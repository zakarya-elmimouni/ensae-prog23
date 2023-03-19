from time import perf_counter
from random import randint
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
    def plus_court_chemin(graph,src, dest, power):
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
    
    #Question 14
    
    def puissance_min(self,src,dest):#recherche de la puissance minimale dans l'arbre couvrant
        fin=0
        debut=0
        arbre_couvrant=kruskal(self.graph)
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
            return self.get_path_with_power(src,dest,power[milieu]),power[debut]
        raise Exception('pas de chemin')
    
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


#Question 10

def temps_moyen(file1,file2):
    g = graph_from_file(file1)
    L= file2.split()
    M = int(L[0])//10
    i = 0
    j=1
    S=0
    while i < M :
            t1 = perf_counter()
            a = Graph.min_power(g, L[j], K[j+1])
            t2 = perf_counter()
    return S/i

#Question 11

#     On utilise l'absurde, on suppose qu'il y a un chemin plus court qui n'est pas dans l'arbre couvrant,
#  il suffira après de remplacer chaque arrete de ce nouveau chemin par une ou plusieurs arretes reliant les 2 mêmes points qui spnt dans l'arbre couvrant(c'est le principe même de l'arbre couvrant),
#  mais puisqu'elle sont dans l'arbre couvrant donc la puissance est minimale, et donc on aura pu trouver un trajet d'une puissance encore plus petite
# ==> Contradiction


#Question 13

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

def le_plus_petit_encetre_commun(v1,v2,arbre_couvrant):
    liste_precedent=[]
    

    
