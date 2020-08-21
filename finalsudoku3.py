import time
from itertools import combinations
class cell:
    def __init__(self, value, markUp, sets):
        self.value=value
        self.markUp=markUp
        self.sets=sets
    def getValue(self):
        return self.value
    def getMarkUp(self):
        return self.markUp
    def getSets(self):
        return self.sets
    def setMarkUp(self, markUp):
        self.markUp=markUp
    def setValue(self, value):
        self.value=value
def getStartCoord(startCoord, x, y):
    subLen=3
    for item in startCoord:
        if x<item[0]+subLen and y<item[1]+subLen:
            return (item[0], item[1])
    return None
def copy(grid):
    leng=9
    g=[[0 for x in range(leng)] for y in range(leng)]
    for x in range(leng):
        for y in range(leng):
            g[x][y]=cell(grid[x][y].getValue(), set(), [])
            for num in grid[x][y].getMarkUp():
                g[x][y].getMarkUp().add(num)
            i=0
            for s in grid[x][y].getSets():
                g[x][y].getSets().append(set())
                for coord in s:
                    g[x][y].getSets()[i].add(coord)
                i=i+1
    return g
def getCand(grid, blanks):
    m=list(blanks)[0]
    for b in blanks:
        if len(grid[b[0]][b[1]].getMarkUp())<len(grid[m[0]][m[1]].getMarkUp()) and grid[b[0]][b[1]].getValue()==".":
            m=b
    return m
def displayMarkUp(grid):
    for x in range(leng):
        for y in range(leng):
            print("mark up at (%s, %s) is %s"%(x, y, grid[x][y].getMarkUp()))
def update(grid, x, y, blanks, poss):
    g=copy(grid)
    b=set()
    for coord in blanks:
        b.add(coord)
    if (x,y) in b:
        b.remove((x,y))
    g[x][y].setValue(poss)
    l=set()
    for s in g[x][y].getSets():
        for coord in s:
            l.add(coord)
    for coord in l:
        if poss in g[coord[0]][coord[1]].getMarkUp():
            g[coord[0]][coord[1]].getMarkUp().remove(poss)
    v=set()
    v.add(g[x][y].getValue())
    g[x][y].setMarkUp(v)
    for s in g[x][y].getSets():
        m=set()
        for item in s:
            if g[item[0]][item[1]].getValue()==".":
                m.add(item)
        combs=set()
        for c in combinations(m, 2):
            combs.add(c)
        for c in combinations(m, 3):
             combs.add(c)
        for c in combs:
            markUpUnion=set()
            for coord in c:
                  markUpUnion=markUpUnion|g[coord[0]][coord[1]].getMarkUp()
            if (len(markUpUnion)==2 and len(c)==2) or (len(markUpUnion)==3 and len(c)==3):
                for item in m:
                    if item not in c:
                        for num in markUpUnion:
                            if num in g[item[0]][item[1]].getMarkUp() and g[item[0]][item[1]].getValue()==".":
                               # print("enter")
                               # display(g)
                              #  for u in m:
                              #      print("mark up for (%s, %s)"%u)
                              #      print(g[u[0]][u[1]].getMarkUp())
                              #  for coord in c:
                               #     print("coor (%s, %s)"%coord)
                                    #print("has markup: %s"%g[coord[0]][coord[1]].getMarkUp())
                                #    print("collective markup: %s"%markUpUnion)
                               # print("so (%s, %s) removed number %s"%(item[0], item[1], num))
                                g[item[0]][item[1]].getMarkUp().remove(num)
    return (g, b)
def getUnique(g, x, y):
    for s in g[x][y].getSets():
        union=set()
        for coord in s:
            if coord!=(x,y):
                for num in g[coord[0]][coord[1]].getMarkUp():
                    union.add(num)
        j=set()
        for num in g[x][y].getMarkUp():
            if num not in union:
                j.add(num)
        if len(j)==1:
            return j
        return None
def isSolvable(grid, blanks):
    for coord in blanks:
        if len(grid[coord[0]][coord[1]].getMarkUp())==0:
            return False
    return True
def getSol(grid, blanks):
    if isSolvable(grid, blanks)==False:
        return None
    elif len(blanks)==0:
        return grid
    cand=getCand(grid, blanks) #one symbol cause coordinates w/ only one symbol is top priiority
    for b in blanks:#one candidate
        j=getUnique(grid, b[0], b[1])
        if j!=None:
            grid[b[0]][b[1]].setMarkUp(j)
            grid[b[0]][b[1]].setValue(list(j)[0])
            cand=b
            break
    for poss in grid[cand[0]][cand[1]].getMarkUp().copy():
        tup=update(grid, cand[0], cand[1], blanks, poss)
        sol=getSol(tup[0], tup[1])
        if sol!=None:
            return sol
    return None
def display(grid):
    string=""
    leng=9
    for x in range(leng):
        string=""
        for y in range(leng):
            if y%3==0:
                string=string+"|%s "%grid[x][y].getValue()
            else:
                string=string+"%s "%grid[x][y].getValue()
            if y==8:
                string=string+"|"
        if x%3==0:
            print("-----------------------")
        print(string)
    print("-----------------------")
p=input("go?")
infile=open("sudoku1465.txt")
arr=infile.read().split()
grids=[]
leng=9
subLen=3
startCoord=[]
for row in range(0, leng, subLen):
    for col in range(0, leng, subLen):
        startCoord.append((row, col))
for line in arr:
    i=0
    grid=[[0 for x in range(leng)] for y in range(leng)]
    for x in range(leng):
        for y in range(leng):
            grid[x][y]=cell(line[i], set(), [])
            for count in range(3):
                grid[x][y].getSets().append(set())
            for v in range(leng):
                grid[x][y].getSets()[0].add((v, y))
                grid[x][y].getSets()[1].add((x, v))
            coord=getStartCoord(startCoord, x, y)
            r=coord[0]
            while r<coord[0]+subLen:
                c=coord[1]
                while c<coord[1]+subLen:
                    grid[x][y].getSets()[2].add((r,c))
                    c=c+1
                r=r+1
            a=1
            while a<=9:
                grid[x][y].getMarkUp().add("%s"%a)
                a=a+1
            i=i+1
    grids.append(grid)
count=1
totTime=0
maxTime=0
maxPuzz=0
for grid in grids:
    t1=time.time()
    blanks=set()
    for x in range(leng):
        for y in range(leng):
            if grid[x][y].getValue()!=".":
                tup=update(grid, x, y, blanks, grid[x][y].getValue())
                blanks=tup[1]
                grid=tup[0]
            else:
                blanks.add((x, y))
    sol=getSol(grid, blanks)
    display(grid)
    if sol==None:
        print("it's impossible")
    else:
        display(sol)
        t2=time.time()
        print("puzzle %s took %s"%(count, (t2-t1)))
        totTime=totTime+(t2-t1)
        if (t2-t1)>maxTime:
            maxPuzz=c
            maxTime=t2-t1
        print("time it has taken thus far: %s"%totTime)
    count=count+1
print("done")
print("it took %s seconds to do %s puzzles"%(totTime, count))
print("the puzzle %s that took the longest took %s"%(maxPuzz, maxTime))
