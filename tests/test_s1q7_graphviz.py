# This will work if ran from the root folder.
import sys 

sys.path.append("delivery_network")
from graph import Graph, graph_from_file
from graphviz import Digraph
g = graph_from_file("input/network.00.in")

print(g.graphique())