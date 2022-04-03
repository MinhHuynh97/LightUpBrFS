import time,os, psutil
CRED = '\033[33m'
CEND = '\033[0m'
class Board:
    def __init__(self,size):
        self.size=size
        self.Blacks=[]
        self.Whites=[]
        self.parent=None
        self.change=[]
        self.heuristic=[]
    def setParent(self,parent):
        self.parent=parent
    def setChange(self,x,y):
        self.change=[x,y]
    def setHeuristic(self,x,y):
        self.heuristic=[x,y]
    def compareToOther(self,otherBoard):
        for white in self.Whites:
            otherWhite=otherBoard.findCell(white.x,white.y)
            if otherWhite is None or not white.compareOther(otherWhite):
                return False
        return True
    def addBlackCell(self,x,y,num):
        self.Blacks.append(Black(x,y,num))
    def setRemainWhite(self):
        for y in range(1,self.size+1):
            for x in range(1,self.size+1):
                cell=self.findCell(x, y)
                if cell is None:
                    self.Whites.append(White(x,y))
                
    def findCell(self,x,y):
        for black in self.Blacks:
            if black.isPosition(x,y):
                return black 
        for white in self.Whites:
            if white.isPosition(x,y):
                return white
        return None
    def lookLeft(self,x,y):
        return self.findCell(x-1, y) if x-1>0 else None
    def lookRight(self,x,y):
        return self.findCell(x+1, y) if x+1<=self.size else None
    def lookAbove(self,x,y):
        return self.findCell(x, y-1) if y-1>0 else None
    def lookBelow(self,x,y):
        return self.findCell(x, y+1) if y+1<=self.size else None
    def lookAround(self,x,y):
        pass

    def printOut1(self):
        print("-----------------------------------")
        for y in range(1,self.size+1):
            for x in range(1,self.size+1):
                cell=self.findCell(x, y)
                if cell is not None and cell.isBlack:
                    if cell.isNum:
                        print("["+str(cell.num)+"] ",end='')
                    else:
                        print("[#] ",end='')
                else:
                    print("[_] ",end='')
            print('\n')
    def printOut(self):
        print("-----------------------------------")
        for y in range(1,self.size+1):
            for x in range(1,self.size+1):
                cell=self.findCell(x, y)
                if cell is None:
                    print("Lỗi")
                if cell.isBlack:
                    if cell.isNum:
                        print("["+str(cell.num)+"] ",end='')
                    else:
                        print("[#] ",end='')
                else:
                    if cell.isBulb:
                        print(CRED+"[b] "+CEND,end='')
                    elif cell.isLight:
                        print(CRED+"[_] "+CEND,end='')
                    else:
                        print("[_] ",end='')
            print('\n')
    #return True if new bulb can add here
    def checkAroundNewBulb(self,cell):
        left=self.lookLeft(cell.x, cell.y)
        right=self.lookRight(cell.x, cell.y)
        above=self.lookAbove(cell.x, cell.y)
        below=self.lookBelow(cell.x, cell.y)
        def checkNoneBulb(val,cell):
            return True if val is None or not val.isBlack or val.checkAddBulb(self) else False
        return checkNoneBulb(left, cell) and checkNoneBulb(right, cell) and checkNoneBulb(above, cell) and checkNoneBulb(below, cell)
    #return True if there is bulb
    def checkBulbOnX(self,cell):
        i=1
        while(cell.x-i>0):
            lcell=self.findCell(cell.x-i, cell.y)
            if lcell is not None:
                if lcell.isBlack:
                    break
                elif lcell.isBulb:
                    return True
                    
            i+=1
        i=1
        while(cell.x+i<=self.size):
            lcell=self.findCell(cell.x+i, cell.y)
            if lcell is not None:
                if lcell.isBlack:
                    break
                elif lcell.isBulb:
                    return True
                    
            i+=1
        return False
    #return True if there is bulb
    def checkBulbOnY(self,cell):
        i=1
        while(cell.y-i>0):
            lcell=self.findCell(cell.x, cell.y-i)
            if lcell is not None:
                if lcell.isBlack:
                    break
                elif lcell.isBulb:
                    return True
            i+=1
        #below
        i=1
        while(cell.y+i<=self.size):
            lcell=self.findCell(cell.x, cell.y+i)
            if lcell is not None:
                if lcell.isBlack:
                    break
                elif lcell.isBulb:
                    return True
            i+=1
        return False
    def setLightNewBulb(self,cell):
        #left
        i=1
        while(cell.x-i>0):
            lcell=self.findCell(cell.x-i, cell.y)
            if lcell is not None:
                if lcell.isBlack:
                    break
                else:
                    lcell.setLight()
            i+=1
        #right
        i=1
        while(cell.x+i<=self.size):
            lcell=self.findCell(cell.x+i, cell.y)
            if lcell is not None:
                if lcell.isBlack:
                    break
                else:
                    lcell.setLight()
            i+=1
        #above
        i=1
        while(cell.y-i>0):
            lcell=self.findCell(cell.x, cell.y-i)
            if lcell is not None:
                if lcell.isBlack:
                    break
                else:
                    lcell.setLight()
            i+=1
        #below
        i=1
        while(cell.y+i<=self.size):
            lcell=self.findCell(cell.x, cell.y+i)
            if lcell is not None:
                if lcell.isBlack:
                    break
                else:
                    lcell.setLight()
            i+=1
    def setNewBlub(self,cell):
        if not self.checkAroundNewBulb(cell) or self.checkBulbOnX(cell) or self.checkBulbOnY(cell):
            return False
        cell.setBulb()
        self.setLightNewBulb(cell)
        return True
       
    def createInitState(self):
        for white in self.Whites:
            def checkAround(val):
                return True if(val is None) or val.isBlack else False
            if checkAround(self.lookLeft(white.x, white.y)) and checkAround(self.lookRight(white.x,white.y)) and checkAround(self.lookAbove(white.x,white.y)) and checkAround(self.lookBelow(white.x,white.y)):
                self.setNewBlub(white)
                AddBulb(white.x, white.y, self)
            added=False
            for black in self.Blacks:
                if black.isNum and black.num!=0:
                    left=self.lookLeft(black.x, black.y)
                    right=self.lookRight(black.x, black.y)
                    above=self.lookAbove(black.x, black.y)
                    below=self.lookBelow(black.x, black.y)
                    def checkAround(val):
                        return 1 if (val is not None) and not val.isBlack else False
                    if black.num==checkAround(left)+checkAround(right)+checkAround(above)+checkAround(below):
                        for cell in [left,right,above,below]:
                            if cell is not None and not cell.isBlack and not cell.isBulb and not cell.isLight:
                                added=self.setNewBlub(cell)
                                AddBulb(cell.x, cell.y, self)
                        #list(map(lambda cell:self.setNewBlub(cell) if cell is not None and not cell.isBlack and not cell.isBulb and not cell.isLight else False ,[left,right,above,below]))
            while(added):
                added=False
                for black in self.Blacks:
                    if black.certainBulb(self):
                        left=self.lookLeft(black.x, black.y)
                        right=self.lookRight(black.x, black.y)
                        above=self.lookAbove(black.x, black.y)
                        below=self.lookBelow(black.x, black.y)
                        for cell in [left,right,above,below]:
                            if cell is not None and not cell.isBlack and not cell.isLight:
                                added=self.setNewBlub(cell)
                                AddBulb(cell.x, cell.y, self)


            
        
    def duplicated(self):
        newboard=Board(self.size)
        newboard.Blacks=list(map(lambda black:black.dup(),self.Blacks))
        newboard.Whites=list(map(lambda white:white.dup(),self.Whites))
        return newboard
    def genState(self,x,y):
        newboard=self.duplicated()
        newbulb=newboard.findCell(x, y)
        if newboard.setNewBlub(newbulb):
            newboard.setParent(self)
            newboard.setChange(x, y)
            return newboard
        else:
            return None
    def genSpace(self):
        priorityList=[]
        for black in self.Blacks:
            listCell=black.checkBulbNeed(self)
            if len(listCell) != 0:
                priorityList=joinList(priorityList, listCell)
        if len(priorityList)!=0:
            returnList=[]
            for pos in priorityList:
                res=self.genState(pos[0], pos[1])
                if res is not None:
                    returnList+=[res]
            return returnList

        for white in self.Whites:
            if not white.isLight:
                priorityList+=[[white.x,white.y]]
        if len(priorityList)!=0:
            returnList=[]
            for pos in priorityList:
                res=self.genState(pos[0], pos[1])
                if res is not None:
                    returnList+=[res] 
            return returnList
        else:
            return []   
    def checkIsGoal(self):
        for black in self.Blacks:
            if len(black.checkBulbNeed(self))!=0:
                return False
        for white in self.Whites:
            if not white.isLight:
                return False
        return True
    def checkHeuristic(self):
        for black in self.Blacks:
            if not black.enoughWhite(self):
                self.setHeuristic(-1,-1)
                return -1,-1
        numBulbNeed=sum(map(lambda black:black.numBulbNeed(self),self.Blacks))
        numNotLight=sum(map(lambda white: 1 if not white.isLight else 0,self.Whites))
        self.setHeuristic(numBulbNeed,numNotLight)
        return numBulbNeed,numNotLight
class Cell:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def isPosition(self,x,y):
        return True if self.x==x and self.y==y else False
    def onX(self,x):
        return True if self.x==x else False
    def onY(self,y):
        return True if self.y==y else False
    def dup(self):
        pass
class Black(Cell):
    def __init__(self,x,y,num):
        self.x=x
        self.y=y
        self.isBlack=True
        self.isNum=num!=-1
        self.num=num
    def checkAddBulb(self,board):
        if not self.isNum: return True
        left=board.lookLeft(self.x, self.y)
        right=board.lookRight(self.x, self.y)
        above=board.lookAbove(self.x, self.y)
        below=board.lookBelow(self.x, self.y)
        numOfBulbsAround=sum(map(lambda val: 1 if val is not None and not val.isBlack and val.isBulb else 0 ,[left,right,above,below]))
        return True if (self.isNum and self.num >numOfBulbsAround) else False

    def checkBulbNeed(self,board):
        if not self.isNum:
            return []
        left=board.lookLeft(self.x, self.y)
        right=board.lookRight(self.x, self.y)
        above=board.lookAbove(self.x, self.y)
        below=board.lookBelow(self.x, self.y)
        whiteCellAround=[]
        numOfBulbsAround=0
        for cell in [left,right,above,below]:
            if cell is not None and not cell.isBlack and not cell.isLight:
                whiteCellAround+=[[cell.x,cell.y]]
            if cell is not None and not cell.isBlack and cell.isBulb:
                numOfBulbsAround+=1
        
        if self.isNum and self.num>numOfBulbsAround:
            return whiteCellAround
        else:
            return []
    def numBulbNeed(self,board):
        if not self.isNum:
            return 0
        left=board.lookLeft(self.x, self.y)
        right=board.lookRight(self.x, self.y)
        above=board.lookAbove(self.x, self.y)
        below=board.lookBelow(self.x, self.y)
        numOfBulbsAround=0
        for cell in [left,right,above,below]:
            if cell is not None and not cell.isBlack and cell.isBulb:
                numOfBulbsAround+=1
        
        if self.isNum and self.num>=numOfBulbsAround:
            return self.num-numOfBulbsAround
        else:
            return 0 
    def enoughWhite(self,board):
        if not self.isNum:
            return True
        left=board.lookLeft(self.x, self.y)
        right=board.lookRight(self.x, self.y)
        above=board.lookAbove(self.x, self.y)
        below=board.lookBelow(self.x, self.y)
        whiteCellAround=0
        numOfBulbsAround=0
        for cell in [left,right,above,below]:
            if cell is not None and not cell.isBlack and not cell.isLight:
                whiteCellAround+=1
            if cell is not None and not cell.isBlack and cell.isBulb:
                numOfBulbsAround+=1
        
        if self.isNum and self.num>numOfBulbsAround:
            return whiteCellAround>=self.num-numOfBulbsAround
        elif self.isNum and self.num==numOfBulbsAround:
            return True
        else:
            return False
    def certainBulb(self,board):
        if not self.isNum:
            return False
        left=board.lookLeft(self.x, self.y)
        right=board.lookRight(self.x, self.y)
        above=board.lookAbove(self.x, self.y)
        below=board.lookBelow(self.x, self.y)
        whiteCellAround=0
        numOfBulbsAround=0
        for cell in [left,right,above,below]:
            if cell is not None and not cell.isBlack and not cell.isLight:
                whiteCellAround+=1
            if cell is not None and not cell.isBlack and cell.isBulb:
                numOfBulbsAround+=1
        
        if self.isNum and self.num>numOfBulbsAround:
            return whiteCellAround==self.num-numOfBulbsAround
        else:
            return False
    def dup(self):
        return Black(self.x, self.y, self.num)
class White(Cell):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.isBlack=False
        self.isBulb=False
        self.isLight=False
    def setBulb(self):
        self.isBulb=True
        self.isLight=True
    def setLight(self):
        self.isLight=True
    def compareOther(self,other):
        if self.isBlack==other.isBlack and self.isBulb==other.isBulb and self.isLight==other.isLight and self.x==other.x and self.y==other.y:
            return True
        return False
    def dup(self):
        newWhite=White(self.x, self.y)
        newWhite.isBulb=self.isBulb
        newWhite.isLight=self.isLight

        return newWhite
def AddBulb(x,y,board):
    print("Thêm đèn ở vị trí ("+str(x)+", "+str(y)+")")
    board.printOut()
def Goal():
    print("Hoàn thành")
    #a>=b ?
def CompareHeuristic(a,b):
    if a[0]>b[0]:
        return False
    elif a[0]==b[0]:
        if a[1]>b[1]:
            return False
        else:
            return True
    else:
        return True

def BFS(board):
    if (board.checkIsGoal()):
        return board
    """ 
        Best-Fist Search
    """
    Open=[]
    Closed=[]
    currbest=board
    i=0
    while(True):
        newBoards=currbest.genSpace()
        removeList=[]

        for closedboard in Closed:
            for newboard in newBoards:
                if newboard.compareToOther(closedboard):
                    removeList+=[newboard]
                    break
        newBoards=removeFromList(newBoards,removeList)
        removeList=[]
        for newboard in newBoards:
            if (newboard.checkIsGoal()):
                return newboard
            newboard.checkHeuristic()
            if newboard.heuristic[0]==-1:
                removeList+=[newboard]

        newBoards=removeFromList(newBoards,removeList)

        for newboard in newBoards:
            idx=0
            for openboard in Open:
                if CompareHeuristic(newboard.heuristic, openboard.heuristic):
                   break
                else:
                    idx+=1
            Open.insert(idx,newboard) 
        currbest=Open[0]
        Open.pop(0)
        Closed.append(currbest)

def joinList(list1,list2):
    a=False
    for i in list2:
        for j in list1:
            if i[0]==j[0] and i[1]==j[1]:
                a=True
                break
        if a:
            a=False
            continue
        else:
            list1.append(i)
    return list1
def removeFromList(list1,list2):
    a=False
    temp=[]
    for i in list1:
        for j in list2:
            if i==j:
                a=True
                break
        if a:
            a=False
            continue
        else:
            temp+=[i]
    return temp

def stateRecur(board):
    if board.parent is None:
        return True
    if stateRecur(board.parent):
        AddBulb(board.change[0], board.change[1], board)
        return True 
def main():
    inputBoard=[["w", "w", "w", "w", "w", "0", "w"],
                ["-1", "-1", "3", "w", "w", "0", "w"],
                ["w", "w", "w", "w", "w", "0", "w"],
                ["w", "w", "w", "1", "w", "w", "w"],
                ["w", "-1", "w", "w", "w", "w", "w"],
                ["w", "1", "w", "w", "1", "1", "-1"],
                ["w", "-1", "w", "w", "w", "w", "w"]]
    print(len(inputBoard))
    board=Board(len(inputBoard))
    for y in range(0,len(inputBoard)):
        for x in range(0,len(inputBoard)):
            if inputBoard[y][x]!="w":
                board.addBlackCell(x+1, y+1, int(inputBoard[y][x]))
                
    board.setRemainWhite()
    start = time.time()
    board.printOut()
    board.createInitState()
    goal=BFS(board)
    end=time.time()
    stateRecur(goal)
    Goal()
    print("Thời gian chạy : ",end-start)
    process = psutil.Process(os.getpid())
    print("Bộ nhớ đã dùng : ",process.memory_info().rss/ 1024 ** 2,"MB")

main()