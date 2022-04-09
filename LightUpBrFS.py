import time,os, psutil
CRED = '\033[33m'
CEND = '\033[0m'
class Board:
    def __init__(self,size):
        self.size=size
        self.Blacks=[]
        self.Whites=[]

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
    
   
    #return True if there is bulb
    
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
    def setNewBlub(self,cell,board):
        if cell.canAddBulb(board) is False:
            return False
        cell.setBulb()
        self.setLightNewBulb(cell)
        return True
        
    def duplicated(self):
        newboard=Board(self.size)
        newboard.Blacks=list(map(lambda black:black.dup(),self.Blacks))
        newboard.Whites=list(map(lambda white:white.dup(),self.Whites))
        return newboard
    
    def checkIsGoal(self):
        for black in self.Blacks:
            if black.numBulbNeed(self) !=0:
                return False
        for white in self.Whites:
            if not white.isLight:
                return False
        return True
    def checkBulbGoal(self):
        for black in self.Blacks:
            if black.numBulbNeed(self) !=0:
                return False
        return True
    
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
    
    def checkBulds(self,board):
        if not self.isNum:
            return []
        left=board.lookLeft(self.x, self.y)
        right=board.lookRight(self.x, self.y)
        above=board.lookAbove(self.x, self.y)
        below=board.lookBelow(self.x, self.y)
        whiteCellAround=[]
        numOfBulbsAround=0
        for cell in [left,right,above,below]:
            if cell is not None and not cell.isBlack and not cell.isLight and cell.canAddBulb(board):
                whiteCellAround+=[[cell.x,cell.y]]
            if cell is not None and not cell.isBlack and cell.isBulb:
                numOfBulbsAround+=1
        
        if self.isNum and self.num>numOfBulbsAround:
            return whiteCellAround
        else:
            return []

        
    def numBulbNeed(self,board):
        if not self.isNum or self.isNum==0:
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
            return -1
    
    
    def dup(self):
        return Black(self.x, self.y, self.num)
class White(Cell):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.isBlack=False
        self.isBulb=False
        self.isLight=False

    def canAddBulb(self,board):
        if self.isLight is False:
            left=board.lookLeft(self.x, self.y)
            right=board.lookRight(self.x, self.y)
            above=board.lookAbove(self.x, self.y)
            below=board.lookBelow(self.x, self.y)
            for cell in [left,right,above,below]:
                if cell is Black and cell.numBulbNeed(board)==0:
                    return False
            return True
        else:
            return False
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




def BFS(board):
    
    ListGeneral=[]
    ListDetail=[]
    ListAddBud=[]
    k=0
    print("Loop các ô trắng cạnh ô đen")
    while(True):
        # lan 1
        for j in range(1,8):
            for i in range(1,8):
                if type(board.findCell(j,i)) is Black :
                    
                    for x in board.findCell(j,i).checkBulds(board):
                        
                        new_board=board.duplicated()
                        new_board.setNewBlub(new_board.findCell(x[0],x[1]),new_board)
                        
                        
                        if len(ListGeneral)==0:
                            ListGeneral.append(new_board)
                        else:
                            kq=True
                            for x in ListGeneral:
                                if x.compareToOther(new_board):
                                    kq=False
                                    break
                            if kq:
                                ListGeneral.append(new_board)
                                k+=1
        print("Lần 1 số loop là : {k}".format(k=k))
        
        # # # lan 2
        pl=1
        while ListGeneral:
            
            k=0
            ListDetail=[]                
            for x in ListGeneral:
                for j in range(1,8):
                    for i in range(1,8):

                        if type(x.findCell(j,i)) is Black :
                            
                            for m in x.findCell(j,i).checkBulds(x):
                                
                                new_board=x.duplicated()
                                
                                new_board.setNewBlub(new_board.findCell(m[0],m[1]),new_board)
                                k+=1
                                if len(ListDetail)==0:
                                    ListDetail.append(new_board)
                                else:
                                    kq=True
                                    for q in ListDetail:
                                        if q.compareToOther(new_board):
                                            kq=False
                                            break
                                    if kq:
                                        ListDetail.append(new_board)
                                        
                        else:
                            continue
                                        
            ListGeneral=[]
            

            for h in ListDetail:
                ListGeneral.append(h)
                # h.printOut()
                if h.checkBulbGoal():
                    
                    if len(ListAddBud)==0:
                        ListAddBud.append(h)
                    else:
                        kq1=True
                        for q in ListAddBud:
                            if q.compareToOther(h):
                                kq1=False
                                break
                        if kq1:
                            ListAddBud.append(h)
            pl+=1
            print("Lần {pl} số loop :{k} ".format(pl=pl,k=k))
        break
    
    print("Loop các ô trắng còn lại")
    while ListAddBud:
        k=0
        ListGen=[]
        for m in ListAddBud:
            for j in range(1,8):
                for i in range(1,8):
                    if type(m.findCell(j,i)) is White and  m.findCell(j,i).canAddBulb(m):
                        new_copy=m.duplicated()
                        k+=1
                        new_copy.setNewBlub(new_copy.findCell(j,i),new_copy)
                        ListGen.append(new_copy)
        ListAddBud=[]
        pl+=1
        print("Lần {pl} số loop là : {k}".format(pl=pl,k=k))
        for k in ListGen:
            ListAddBud.append(k)
            if k.checkIsGoal():
                
                return True,k
    return False,[]     


def main():
    inputBoard=[["w", "w", "w", "-1", "w", "w", "w"],
                ["w", "2", "w", "0", "w", "-1", "w"],
                ["w", "w", "w", "w", "w", "w", "w"],
                ["0", "0", "w", "w", "w", "0", "-1"],
                ["w", "w", "w", "w", "w", "w", "w"],
                ["w", "-1", "w", "0", "w", "2", "w"],
                ["w", "w", "w", "1", "w", "w", "w"]]
    print(len(inputBoard))
    board=Board(len(inputBoard))
    for y in range(0,len(inputBoard)):
        for x in range(0,len(inputBoard)):
            if inputBoard[y][x]!="w":
                board.addBlackCell(x+1, y+1, int(inputBoard[y][x]))
                
    board.setRemainWhite()
    start = time.time()
    board.printOut()
    goal=BFS(board)
    if goal[0]:
       goal[1].printOut()
    else:
        print("Không giải được theo đề bài") 
    end=time.time()
    print("Thời gian chạy : ",end-start)
    process = psutil.Process(os.getpid())
    print("Bộ nhớ đã dùng : ",process.memory_info().rss/ 1024 ** 2,"MB")

main()