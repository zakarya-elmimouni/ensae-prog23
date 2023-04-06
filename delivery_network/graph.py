from time import perf_counter
from random import randint
from graphviz import Digraph

class UnionFind:
    """""   Class UnionFind
    Attributs : 
    -----------
    parent : liste
    rank : liste 
    Methodes : 
    ----------
    get_parent(): obtenir le parent d'un noeud qui est un représentant d'un groupe de noeuds
    Union(): permet de réunir deux groupes de noeuds
    """

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def Union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x != root_y:
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y
                if self.rank[root_x] == self.rank[root_y]:
                    self.rank[root_y] += 1
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
    

    # Question 1:

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
        # On vérifie d'abord si les noeuds de notre nouevlle arrette existe déjà dans notre graphe
        # Sinon on les ajoute
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

    # Question 2

    def connected_components(self):
        """ Description:
        ---------------
        cette fonction permet de retourner les composantes connexes du graphe  

        Parameters:
        ------------ 
        Output:
        ---------
        liste contenant tous les composantes connexes du graphe

        Complexity:
        Dans le pire des cas où tous les sommets sonts isolés on va avoir une complexité de l'ordre O(V**2)
        et dans le cas d'un graphe connexe on aura une complexité de l'ordre O(V)
        """
        composantes_connexes=[]
        visited_nodes={noeud:False for noeud in self.nodes}

        def parcours_profondeur(s):
            composantes=[s]
            for neighboor in self.graph[s]:
                neighboor=neighboor[0]
                if not visited_nodes[neighboor]:
                    visited_nodes[neighboor]=True
                    composantes+=parcours_profondeur(neighboor)
            return composantes
        
        for s in self.nodes:
            if not visited_nodes[s]:
                composantes_connexes.append(parcours_profondeur(s))
        return composantes_connexes

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))



    # Question 3 : Existence de trajet

    
    def get_path_with_power(self,src, dest, power):
        """Description
        ------------------
        cette fonction permet de retourner un chemin qu'un camion de puissance 'power' peut faire 

        Parameters
        -----------
           src: Nodetype
               c'est le départ de notre camion
           dest: Nodetype
               la destination
           power: Numeric
                la puissance du camion qui parcourt ce chemin

        Output
        --------
          path:list
            un chemin possible pour faire passer le camion de la source à la destination

        -----------

        """

        def get_precedent(graph,depart,arrivée,power):
            """Description:
            ---------------
            Cette focntion permet de faire un parcours en largeur en commençant par le sommet de départ.
            Le parcours s'arrête une fois on atteint le sommet d'arrivée
            
            Parameters:
            -----------
            graph:dict
                un dictionnaire représentant le graphe
            depart:Nodetype
                sommet de départ
            arrivée: Nodetype
                sommet d'arrivée
            
            Output:
            -------
            dictionnaire qui comporte les sommets comme es clés et l'élément précédent de chaque sommet comme valeur 
            """
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

        # La complexité de get_path_with_power est la même que la complexité de la fonction get_precedent
        # C'est une complexité de l'ordre O(V**2) , avec V le nombre de sommets.

           


    # Question 5 : Le plus court chemin 


    def plus_court_chemin(self,src, dest, power):
        """Description:
        ---------------
        cette fonction permet de retourner le plus court chemin (en terme de distance) que peut parcourir 
        un camion de puissance "power" en se basant sur l'algorithme classique de Dijstra 

        Parameters:
        ------------
        src:Nodetype
          la source (le départ du camion)
        dest:Nodetype
          la destination (l'arrivée du camion)
        power:Numeric
         puissance du camion parcourant ce trajet

        Output:
        ---------
        liste représentant le chemin le plus court et la distance correspnodante à ce chemin


        -----------
        La même complicité que l'algorithme de Dikjstra
        """
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

    # Nous pouvons  faire un test pour voir si le départ et l'arrivée sont dans la même composante connexe
    # Dans ce cas on peut directement conclure sans passer par l'algorithme Djikstra 
    
    


    #Question 6 : min_power

    # Le programme de la question 6 est basée sur une recherche dichotomique

    def min_power(self, src, dest):
        """Description:
        ---------------
        cette fonction permet de calculer la puissance minimale d'un trajet par une méthode 
        dichotomique

        Parameters:
        ------------
        src:Nodetype
          la source (le départ du camion)
        dest:Nodetype
          la destination (l'arrivée du camion)

        Output:
        ---------
        liste représentant le chemin le plus court et la distance correspondante à ce chemin
        
        
        """
        if src==dest:
            return [dest,src],0
        else:
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



    # Question 7 


    def graphique(self) :
        """Description:
        ---------------
        cette fonction permet de tracer le graphe en entrée 

        Parameters:
        ------------
      self: Graphe

        Output:
        ---------
        Un dessin représentant notre graphe 
        """
         # Création du graphe avec Graphviz
        dot = Digraph()
        for node in self.graph:
            dot.node(str(node))
        for node in self.graph:
            for edge in self.graph[node]:
                dot.edge(str(node), str(edge[0]), label=str(edge[1]))
        # Affichage du graphe
        dot.render('graph')

    
    # Question 14 : puissance minimale à partir de l'arbre couvrant
    
    #recherche de la puissance minimale dans l'arbre couvrant
    def puissance_min(self,arbre_couvrant,src,dest):

        """
        Description:
        ---------------
        Cette fonction permet de retourner la puissance minimale d'un graphe en se basant sur son arbre couvrant
        
        Parameters:
        ------------
        src:Nodetype
          la source (le départ du camion)
        dest:Nodetype
          la destination (l'arrivée du camion)

        Output:
        ---------
        liste représentant un chemin possible  et la puissance minimale d'un camion qui peut parcourir ce chemin
        """
        fin=0
        debut=0
        arbre_couvrant=arbre_couvrant.graph
        power=[]
        if src==dest:
            return [dest,src],0
        else:
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

    #Question 18 (Séance 4):

    #Manière 1 : Brute force

    # On définira une fonction qui retourne une liste avec tous les trajets et le meilleur camion associé
    # Le meilleur camion qu'on peut associer à chaque trajet est évidement un camion qui peut passer
    # Et dont le coût est minimal

    def collection(self,liste_trajets,liste_camions):
        G = self.graph
        arbre=kruskal(self)
        W = liste_trajets
        T = liste_camions
        for i in range(len(W)) :
            L,a = self.puissance_min(arbre,W[i][0], W[i][1])
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


    # Méthode 2 : Sac à dos

    def maximiser_profit_cout(self,liste_camions,liste_trajets):
    
        ''' Description:
        ----------------
        Cette fonction permet de calculer pour chaque trajet le rapport profit/cout maximal et le camion
        correspondant à ce rapport et il retourne le résultat sous forme d'un dictionnaire sous la forme 
        {"trajet":[rapport (profit/cout)maximale,Camion_correspondant à ce rapport]...}
        
        Parameters:
        ------------
        liste_camions: list
        liste de tous les Camions ayant la forme [(camion,puissance,cout)...]
        liste_trajets: list
        une liste de tous les trajets possibles [(debut,fin,profit)....]

        Output:
        --------
        Dictionnaire qui comporte chaque arêtes associé au rapport profit/cout maximal
        ainsi que le camion associé à ce rapport
        
        Complexity:
        ------------
        La complexité de l'algorithme estde l'ordre de O(len(liste_camions)*len(liste_trajets))'''
        
        dict_profit_cout={} 
        """"Nous allons definir une liste de puissance minimale pour chaque trajet"""

        puissance_min_trajets={}
        arbre=kruskal(self)
        for trajet in liste_trajets:
            depart=trajet[0]
            arrivée=trajet[1]
            liste,puissance_min=self.puissance_min(arbre,depart,arrivée)
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
        ''' Description:
        ----------------
        Cette fonction permet de chercher la meilleur combinaison des trajets et camions qui permet 
        la maximisation du profit , en se basant sur l'algorithme du sac à dos
        
        Parameters:
        ------------
        liste_camions: list
        liste de tous les Camions ayant la forme [(camion,puissance,cout)...]
        liste_trajets: list
        une liste de tous les trajets possibles [(debut,fin,profit)....]

        Output:
        --------
        liste_finale: la liste des trajets avec les camion correspondants 
        elle est sous la forme [(trajet,[rapport_max,camion_correspondant à ce trajet])]
        cout_total: c'est le cout qu_on a dépensé <=B 
        profit_total:le profit qu'on a obtenu         
        
        Complexity:
        ------------
        La complexité de l'algorithme estde l'ordre de O(len(liste_camions)*len(liste_trajets))
        '''
        dict_profit_cout=self.maximiser_profit_cout(liste_camions,liste_trajets)
        liste_trajet_profit_cout_triée= sorted(dict_profit_cout.items(), key=lambda item:item[1][0],reverse=True)

        # Liste trié selon raport_maximale de chaque trajet sous la forme [(trajet,[rapport_ma x,camion])]
        liste_finale=[]
        #C'est juste un troncation de la liste_trajet_profit_cout_triée
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
        if cout_totale>Budget:#Condition de Budget
            cout_totale=cout_totale-cout_camion   
            #on retire le cout du dernier camion ajouté
            profit_totale=profit_totale-rapport_max*cout_camion 
            #on retire le profit du dernier trajet ajouté
            liste_finale.remove(liste_trajet_profit_cout_triée[i-1])
        output_liste=[]
        #Une liste sous la forme [(camion,trajet)]
        for element in liste_finale:
            output_liste.append((element[1][1],element[0]))
        return frozenset(output_liste),cout_totale,profit_totale


    # Méthode 3 : élimination

    def eliminer_elements_inutils(self,liste_camions):
        ''' Description:
        ----------------
        Cette fonction permet d'éliminer les camions qui nous avons au moins un meilleur camion qu'eux
        (càd un meilleur camion en fonction du cout (plus petit) et une meilleure puissance(plus grande))
        
        Parameters:
        ------------
        liste_camions: list
        liste de tous les Camions ayant la forme [(camion,puissance,cout)...]

        Output:
        --------
        nb_initiale_camions: le nombre des camions initials         
        nb_camion_finale: le nombre de camion à l'état final
        liste_camions: la liste finale des camions après élimination des éléments inutils
        Complexity:
        ------------
        La complexité de l'algorithme est de l'ordre de O(len(liste_camions)^2)
        '''
        nb_initial_camions=len(liste_camions)
        liste_initiale=liste_camions.copy()
        for i in range (nb_initial_camions):
            for j in range (i+1,nb_initial_camions):
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
                if cout1>=cout2 and puissance1<=puissance2:
                    liste_camions.remove(camion1)
        return nb_initial_camions,len(liste_camions),liste_camions



# Question 1 (suite) et Question 4 : 
        
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


# Définition des fonctions d'ouverture des fichiers : 

def way_from_file(filename):
    ''' Description:
        ----------------
        Cette fonction permet de lire les fichiers text des routes et de retourner à partir de ces
        fichiers une liste de trajets  
        
        Parameters:
        ------------
        filename: fihchier text
              fichier sous la forme 'routes.xx.in'

        Output:
        --------
        W:list
            liste des trajets dans le fichier        
        
        Complexity:
        ------------
        La complexité de l'algorithme est de l'ordre de O(n) telle que n le nombre de ligne du fichier
        '''
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
    ''' Description:
        ----------------
        Cette fonction permet de lire les fichiers text des trucks et de retourner à partir de ces
        fichiers la liste de camions correspondante 
        
        Parameters:
        ------------
        filename: fihchier text
              fichier sous la forme 'trucks.xx.in'

        Output:
        --------
        W:list
            liste des camions contenus dans le fichier        
        
        Complexity:
        ------------
        La complexité de l'algorithme est de l'ordre de O(n) telle que n le nombre de ligne du fichier
        '''
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

def trucks_from_file_1(filename): 
    ''' Description:
        ----------------
    
        Cette fonction permet de lire les fichiers text des trucks et d'éliminer les Camions par rapport aux quels 
        nous avons au moins un meilleur camion que celui-ci  (i.e. càd une plus grande puissance et un cout plus petit)
        fichiers la liste de camions correspondante 
        
        Parameters:
        ------------
        filename: fihchier text
              fichier sous la forme 'trucks.xx.in'

        Output:
        --------
        W:list
            liste des camions utils contenus dans le fichier        
        
        Complexity:
        ------------
        La complexité de l'algorithme est de l'ordre de O(n) telle que n le nombre de ligne du fichier
        '''
    with open(filename,"r") as file :
        n= int(file.readline())
        T=[]
        L=[]
        for i in range(n):
            truck = list(map(int,file.readline().split()))
            truck=tuple(truck)
            if len(truck) == 2 :
                T.append((i+1,truck[0],truck[1]))
                L.append((i+1,truck[0],truck[1]))

                if i>=1 and T[i][2] < T[i-1][2] :
                    L.remove(T[i-1])
            else :
                raise Exception("Format incorrect")
    return L


# Question 5 (Suite) : Le plus court chemin

def dijkstra(graph,source,puissance_camion):
    ''' Description:
        ----------------
        Cette fonction est inspirée de l'algorithme classique de Dijkstra, elle constitue une première 
        étape pour le calcul du plus court chemin dans un graphe 
        
        Parameters:
        ------------
        graph: dict
            Un dictionnaore qui contient la liste d'adjacence de chaque sommet sous la forme
            graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
            p1 la puissance pour passer du sommet à son voisin1 et d1 est la distance entre le sommet 
            et son voisin1
        source:Nodetype
            C'est le sommet de départ
        puissance_camion:Numeric
            C'est la puissance du camion 

        Output:
        --------
        distance:dict
            Dictionnaire dont les clés sont les sommets le les valeurs sont la distance minimale 
            de la source. il est sous la forme
            distance[sommet]=distance minimale séparant ce sommet de la source 
        precedent:dict
            Dictionnaire dont les clés sont les sommets et les valeurs sont le sommet précedent qui 
            permet d'avoir une distance minimale. il est sous la forme 
            precedent[sommet]=noeud qui précéde ce sommet dans le plus court chemin       
        
        Complexity:
        ------------
        La complexité de l'algorithme est de l'ordre de O(Vlog(V)) telle que V est le nombre de sommets
    '''
    precedent = {x:None for x in graph.keys()}#les précedents des sommets dans le trajet minimal
    dejaTraite = {x:False for x in graph.keys()}#l'élément est déja traité? False ou True
    distance =  {x:float('inf') for x in graph.keys()}#la distance de l'origine à chaque sommet
    distance[source] = 0 #initialisation : la distance de l'origine à l'origine c"est 0
    a_traiter = [(0, source)]#il contient la liste des éléments à evaluer. 
    while a_traiter:
    # on fait un parcours en largeur 
        dist_noeud, noeud = a_traiter.pop()
        if not dejaTraite[noeud]:
            dejaTraite[noeud] = True
            for voisin in graph[noeud]:
                if voisin[1]<=puissance_camion:
                    dist_voisin = dist_noeud + voisin[2]
                    if dist_voisin < distance[voisin[0]]:
                        distance[voisin[0]] = dist_voisin
                        precedent[voisin[0]] = noeud
                        a_traiter.append((dist_voisin, voisin[0]))
        a_traiter.sort(reverse=True)
    return distance, precedent


# Question 10 : 

def temps_moyen_1(filenetwork,fileroutes):
    g=graph_from_file(filenetwork)
    with open(fileroutes,"r") as file : 
        n= int(file.readline())
        W = []
        tempstotale=0
        nb_de_tarjet_calculé=0
        for i in range(0,n,10000):
            nb_de_tarjet_calculé+=1
            way = list(map(int,file.readline().split()))
            way=tuple(way)
            if len(way)== 3 :
                t1=perf_counter()
                W.append(g.min_power(way[0],way[1]))
                t2=perf_counter()
                tempstotale+=t2-t1
            else : 
                raise Exception("Format incorrect")
        
    return tempstotale/nb_de_tarjet_calculé

# Question 11 : 

#   On utilise l'absurde, on suppose qu'il y a un chemin plus court qui n'est pas dans l'arbre couvrant,

#  il suffira après de remplacer chaque arrete de ce nouveau chemin par une ou plusieurs arretes reliant les 2 mêmes points qui spnt dans l'arbre couvrant(c'est le principe même de l'arbre couvrant),

#  mais puisqu'elle sont dans l'arbre couvrant donc la puissance est minimale, et donc on aura pu trouver un trajet d'une puissance encore plus petite

# ==> Contradiction



# Question 12 :

def kruskal(g):
    """""   Fonction : kruskal
    Description:
    -----------
    Permet d'envoyer un objet de la Class Graph qui est un arbre couvrant de poids minimal.

    Parameters:
    ------
    g : Graph
        un élement de la classe graph
    
    output:
    -------
    arbre couvrant de la classe graph

    Complexity : O(Nlog(N )).
    """

    N=g.nb_nodes
    arcs=g.edges #Les arcs sont récupérés directement dans la lecture du fichier pour gagner du temps
    arcs.sort(key=lambda x : x[2])
    Arbre_minimum=Graph(g.nodes)
    ed=UnionFind(N+1)
    index=0
    while Arbre_minimum.nb_edges!=N-1: # Cf Q.2
        (src,dest,power,dist)=arcs[index]
        index+=1

        x=ed.find(src)
        y=ed.find(dest)
        
        if x!=y:
            Arbre_minimum.add_edge(src,dest,power,dist)

            ed.Union(x,y)
    return Arbre_minimum

# Question 14 (Suite) : 

def temps_moyen_2(filenetwork,fileroutes):
    g=graph_from_file(filenetwork)
    arbrecouvrant=kruskal(g)
    with open(fileroutes,"r") as file : 
        n= int(file.readline())
        W = []
        tempstotale=0
        nb_de_tarjet_calculé=0
        for i in range(0,n,10000):
            nb_de_tarjet_calculé+=1
            way = list(map(int,file.readline().split()))
            way=tuple(way)
            if len(way)== 3 :
                t1=perf_counter()
                W.append(g.puissance_min(arbrecouvrant,way[0],way[1]))
                t2=perf_counter()
                tempstotale+=t2-t1
            else : 
                raise Exception("Format incorrect")
        
    return tempstotale/nb_de_tarjet_calculé

# Question 15 :

# Réponse : la complexité totale de la fonction basée sur l’arbre couvrant de poids minimal 

# qui calcule la puissance minimale d'un camion pour couvrir un trajet donné 

# est donc de O(nb_edges.log (nb_nodes))("ce lui du tri rapide de kruskal") + O(nb_edges+nb_nodes), 

# qui est équivalent à O(nb_edges.log(nb_nodes))



# Question 16 : 

def profondeur_et_peres(root,arbre_couvrant):
    ''' Description:
        ----------------
        Cette fonction permet la recherche de la profondeur et du pere de chaque élément de l'arbre 
        couvrant en partant d'une racine 'root'
        
        Parameters:
        ------------
        root: Nodetype
            Une racine du graphe
        arbre_couvrant:Graph
            Un arbre couvrant résulatant de l'algorithme de kruskal 

        Output:
        --------
        profondeur:dict
            Dictionnaire dont les clés sont les sommets le les valeurs sont la profondeur de chaque
             sommet. Il est sous la forme:
            profondeur[sommet]=profondeur de ce sommet en partant du racine
        peres:dict
            Dictionnaire dont les clés sont les sommets et les valeurs sont les peres correspondants 
            dans l'arbre couvrant. Il est sous la forme: 
            peres[sommet]=noeud père du sommet dans l'arbre couvrant       
        
        Complexity:
        ------------
        La complexité de l'algorithme est de l'ordre de O(V) telle que V est le nombre de sommets
    '''
    visited_nodes={node:False for node in arbre_couvrant.nodes}
    profondeur={node:None for node in arbre_couvrant.nodes}
    peres={node:None for node in arbre_couvrant.nodes}
    pile=[]
    peres[root]=[root,0]
    visited_nodes[root]=True
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


# Question 16 (Suite) :

def plus_petit_encetre_commun(arbre_couvrant,src,dest,root):
    ''' Description:
        ----------------
        Cette fonction permet le calcul de la puissance minimale  et du chemin associé en se basant 
        sur la méthode du plus petit ancêtre commun 
        
        Parameters:
        ------------
        root: Nodetype
            Une racine du graphe
        arbre_couvrant:Graph
            Un arbre couvrant résulatant de l'algorithme de kruskal 
        src:Nodetype
            Sommet de départ
        dest:Nodetype
            Sommet d'arrivée

        Output:
        --------
        puissance_min:Numeric
            La puissane minimal d'un camion pouvant parcourir le trajet    
        chemin:list
            un chemin possible correspondant à cette puissance minimale

        Complexity:
        ------------
        
    '''
    peres=profondeur_et_peres(root,arbre_couvrant)[1]
    liste_ancetres_src=[[src,0]]
    liste_ancetres_dest=[[dest,0]]
    element=src
    while element!=root: # O(V)
        liste_ancetres_src.append(peres[element])
        element=peres[element][0]
    liste_ancetres_src.append(peres[element])
    # Liste_ancetres_src.append([root,0])
    element=dest
    while element!=root:
        liste_ancetres_dest.append(peres[element])
        element=peres[element][0]
    
    liste_ancetres_dest.append(peres[element])
    # Détermination du plus petit encetre commun 
    for i in range(len(liste_ancetres_src)):
        for j in range(len(liste_ancetres_dest)):
            ancetre_dest_couple=liste_ancetres_src[i]
            ancetre_src_couple=liste_ancetres_dest[j]
            ancetre_dest=ancetre_dest_couple[0]
            ancetre_src=ancetre_src_couple[0]
            if ancetre_src==ancetre_dest:#ancetre commun
                indice_dest=j
                indice_src=i
                break
    liste_src=liste_ancetres_src[:indice_src+1]
    liste_dest=liste_ancetres_dest[:indice_dest-1]
    liste_dest.reverse()
    chemin=liste_src+liste_dest
    # Le chemin est donc liste_src+liste_dest
    # Determination du power min
    puissance_min=max(node[1]for node in chemin)
    return puissance_min,chemin



# Question 17 : 

def temps_moyen_3(filenetwork,fileroutes):
    g=graph_from_file(filenetwork)
    arbre_couvrant=kruskal(g)
    with open(fileroutes,"r") as file : 
        n= int(file.readline())
        W = []
        nb_de_tarjet_calculé=0
        tempstotale=0
        for i in range(0,n,10000):
            nb_de_tarjet_calculé+=1
            way = list(map(int,file.readline().split()))
            way=tuple(way)
            if len(way)== 3 :
                t1=perf_counter()
                W.append(plus_petit_encetre_commun(arbre_couvrant,way[0],way[1],1))
                t2=perf_counter()
                tempstotale+=t2-t1
            else : 
                raise Exception("Format incorrect")

        
    return tempstotale/nb_de_tarjet_calculé

# Question 17 de seance3 qui demande le calcul du temps d'execution des fichiers routes.x.in

def temps_totale(filenetwork,fileroutes):
    g=graph_from_file(filenetwork)
    arbre_couvrant=kruskal(g)
    with open(fileroutes,"r") as file : 
        n= int(file.readline())
        W = []
        tempstotale=0
        for i in range(0,n):
            way = list(map(int,file.readline().split()))
            way=tuple(way)
            if len(way)== 3 :
                t1=perf_counter()
                W.append(plus_petit_encetre_commun(arbre_couvrant,way[0],way[1],1))
                t2=perf_counter()
                tempstotale+=t2-t1
            else : 
                raise Exception("Format incorrect")
    return tempstotale








            

    




    


    

    
