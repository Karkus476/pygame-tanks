from vector import Vector

#pv = vector
#ev = (pv, pv, v)

class Path:
    def __init__(self, pv, ev):
        self.pv = pv
        self.ev = ev
        
    def findPath(self, f, t):
        openset = [Node(None, f)]
        set = []
        toBreak = False
        while not toBreak:
            for i in openset:
                if i.pv == t:
                    toBreak = True
                    break
            for o in openset:
                set += self.getPossible(o)
            openset = set
            set = []
            
        list = []
        while i.parent:
            list.append(i.pv)
            i = i.parent
        return list[::-1]
        
            
    def getPossible(self, n):
        possible = []
        for i in self.ev:
            if i[0] == n.pv:
                possible.append(Node(n, i[1]))
            elif i[1] == n.pv:
                possible.append(Node(n, i[0]))
        return possible

    def getClosestNode(self, posV, withIndex):
        dists = []
        posV=Vector(posV[0], posV[1])
        for i in self.pv:
            diff = Vector.subV(posV, i)
            dists.append(diff.lengthSq())
        return self.pv[dists.index(min(dists))]
                    
class Node:
    def __init__(self, parent, pv):
        self.parent = parent
        self.pv = pv
        
def squareToTank(xy):
    return (Vector(xy[0]*30+15, xy[1]*30+15))
    
