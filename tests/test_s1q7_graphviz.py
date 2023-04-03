# This will work if ran from the root folder.
import sys 

sys.path.append("delivery_network")
from graph import Graph, graph_from_file
from graphviz import diagraph
jls_extract_var = "/input/network00.in"
g = graph_from_file(jls_extract_var)
g.graphique()