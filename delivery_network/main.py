

def way_from_file(filename):
    with open(filename,"r") as file : 
        n= int(file.readline())
        W = []
        for _ in range(n):
            way = list(map(int,file.readline().split()))
            if len(way)== 3 :
                W.append(way)
            else : 
                raise Exception("Format incorrect")
    return W
way_from_file("input/routes.1.in")