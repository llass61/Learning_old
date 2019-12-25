


def list1():
    S = [ s**2 for s in range(10)]
    print S

    V = [2**i for i in range(13)]
    print V

    M = [x for x in S if x%2 == 0]
    print M

def list2():
    arr = "gridi     |STARTED\ngridibb    |STOPPED"
    d = {}
    for i in arr.split("\n"):
        d[i.split("|")[0]] = i.split("|")[1]

    print d





list2()