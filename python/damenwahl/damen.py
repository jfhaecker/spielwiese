import  inspect,sys




def dame(reihen, spalten):
    #print(f"Zahl{zahl}")
    #print(f"{inspect.currentframe()}")
    #print(f"Funktion dame Adresse: {inspect.currentframe().f_code}")
    stack.append("o")
    print(f"{''.join(stack)}->dame: {inspect.currentframe().f_locals}")
    #print(f"{inspect.currentframe().f_back}")
    #print(f"{inspect.currentframe().f_code.co_name}")
    #print(f"Funktion dame Caller: {inspect.currentframe().f_back}")
   # print(f"{inspect.stack()[0]}")
    if reihen == 0:
        #print(f"{''.join(stack)}->dame fertig")
        print(f"{''.join(stack)}->dame fertig: {inspect.currentframe().f_locals}")
        return [[]]
    else:
        k = dame(reihen - 1, spalten)
        r = dame_dazu(reihen - 1, spalten,k)
        stack.pop()
        return r


def dame_dazu(neue_reihe, spalten, liste):
    print(f"{''.join(stack)}->dame_dazu: {inspect.currentframe().f_locals}")
    depp = []
    for loesung in liste:
        for neue_spalte in range(spalten):
            depp.append(loesung + [neue_spalte])
    print(f"{''.join(stack)}->dame_dazu fertig: {depp}")
    return depp



#def print_frames(frame_list):
    
global stack 
stack= []

print("_________________________")
k = dame(4,4)
print("_________________________")
print(f"{len(k)} Lösungen")
for l in k:
    print(l)
