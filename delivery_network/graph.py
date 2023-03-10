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
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
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
    
def get_path_with_power(graph,src, dest, power):
 
        #question 5
    #recherche du chemin le plus court à l'aide de dijkstra
    #essaie d'implementation sur mon problème
#algprithme de dijikstra
#graph={sommet:["liste des sommets lié à ce sommet, chaque sommet est sous la forme d'un tuple(sommet,power, distance)"]
def dijkstra(graph,source,puissance_camion):
    #initialisation
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
#print(dijkstra(graph,'A',5))#parfait le programme marche bien 
#il reste à chercher comment passer de ca à trouver le plus petit chemin entre deux points
def plus_court_chemin(graph,src, dest, power):
    distance, precedent=dijkstra(graph,src,power)
     #({'A': 0, 'B': 1, 'C': 3, 'D': 7, 'E': inf, 'F': inf}, {'A': None, 'B': 'A', 'C': 'B', 'D': 'B', 'E': None, 'F': None})
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
####print(get_path_with_power(graph,"A", "F", 5))
#un pont à améliorer dans ce programme c'est de faire un teste de composante connxe au début
#si le depart et l'arrivée ne sont pas dans la meme composante connexes on va pas se casser la tete
#dans ce cas ça vaut pas le cout de passer par l'algorithme de dijkstra qui de complexité assez grande 
    

    def connected_component(nodes):
        if nodes==[]:
        return []
        else:
            S=[[self.nodes[0]]]
        
        
        for element in self.graph[nodes[0]]:
            if element[0] not in S[0]:
                S[0].append(element[0])
            for x in self.graph[element[0]]:
                if x not in S[0]:
                    S[0].append(x)
        for j in range (len(S[0])):
            nodes.remove(S[0][j]) #les nodes privés de S[i]
       
        return S+ connected_component(nodes)


    def connected_components_set(self):

        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        #y'a la fonction composante connexe
        return connected_component(self.nodes)
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        k=0
        while get_path_with_power(graph,src, dest, k)==None:
            k+=1
        return K
   # un essai dichotomique
   def dichotomie(debut,fin):
        while debut<fin:
        milieu = (debut+fin)//2
        if get_path_with_power(self,src, dest, milieu) ==None:
             debut=milieu
             return dichotomie(debut,fin)
        else:
            fin = milieu
            return dichotomie(debut,fin)
        if debut==fin :
            return debut
     def min_power(self, src, dest):
        fin=0
        debut=0
        for sommet in self.graph.keys():
            for voisin in self.graph[sommet]:
                if voisin[1]>fin:
                    fin=voisin[1]# recuperation du k maximal
        return dichotomie(debut,fin),get_path_with_power(self,src, dest,dichotomie(debut,fin))
   

        
           
    


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
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g
