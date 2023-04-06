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



        #puissance_min_trajets={trajet:self.puissance_min(trajet[0],trajet[1])[1]for trajet in liste_trajets}