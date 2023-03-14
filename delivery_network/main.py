from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.01.in"

g = graph_from_file(data_path + file_name)
print(g)
def kruskal(g):
        arretes=g.edges
        d = {}
        for liste in arretes:
            a= tuple(liste[:2])
            if a not in d:
                d[a] = liste
        resultat = list(d.values())
        arretes = resultat
        nb_nodes = g.nb_nodes
        arretes.sort(key = lambda x :x[2] )
        a=1
        A=[]
        S=[]
        liste_aretes=[]
        for x in arretes : 
            if (x[0] not in S) and (x[1] in S):
                S.append(x[0])
                A.append(x)
                liste_aretes.append(tuple(x[:2]))
            elif (x[0] in S) and (x[1] not in S):
                S.append(x[1])
                A.append(x)
                liste_aretes.append(tuple(x[:2]))
            elif (x[0] not in S) and (x[1] not in S):
                S.append(x[0])
                S.append(x[1])
                A.append(x)
                liste_aretes.append(tuple(x[:2]))
            elif  (x[0] in S) and (x[1] in S):
                for sommet in S:
                    if ((x[0],sommet) in liste_aretes)and((x[1],sommet) in liste_aretes):
                        a=0
                        break#pas besoin de voir sur les autres sommets
                    elif((sommet,x[0]) in liste_aretes)and((x[1],sommet) in liste_aretes):
                        a=0
                        break#pas besoin de voir sur les autres sommets
                    elif((x[0],sommet) in liste_aretes)and((sommet,x[1]) in liste_aretes):
                        a=0
                        break #pas besoin de voir sur les autres sommets
                    elif((sommet,x[0]) in liste_aretes)and((sommet,x[1]) in liste_aretes):
                        a=0
                        break #pas besoin de voir sur les autres sommets
                    else:
                        a=1
                if a==1:
                    A.append(x)
                    liste_aretes.append(tuple(x[:2]))






        g_mst={}
        S=set(S)#juste pour eliminer les doublons
        S=list(S)
        S.sort()
        for m in S : 
            g_mst[m]=[]
        for m in A :
            g_mst[m[0]].append((m[1],m[2],m[3]))
            g_mst[m[1]].append((m[0],m[2],m[3]))
        return(g_mst)
g = graph_from_file("input/network.00.in")
print(g.graph)
g_mst =kruskal(g)
print(g_mst)