import time,os, psutil,copy
from bisect import bisect_left,insort_left
CBLUE = '\033[96m'
CBROWN = '\033[0;33m'
CEND = '\033[0m'

RIVER="River"
ISLAND="Island"
NUMISLAND="Numisland"

class Board():
	
	def __init__(self,coordinates ):
		"""
			In coordinates , 0 is river, -1 is island ,other numbers are numisland
		"""
		self.coordinates=coordinates
		self.size=len(coordinates)
		self.heuristic=0
	def PrintOut(self):
		print("------------------")
		for row in self.coordinates:
			for cell in row:
				if cell==0:
					print(CBLUE+"[ ] "+CEND,end='')
				elif cell==-1:
					print(CBROWN+"[ ] "+CEND,end='')
				else:
					print(CBROWN+"["+str(cell)+"] "+CEND,end='') 
			print()
	def setIsland(self,river,islands):
		cells=self.getCellAround(river[0],river[1])
		for cell in cells:
			typ=self.typ2(cell)
			if typ is not None and typ != RIVER and not isInList(islands,cell,isSameCell):
				return False
		self.coordinates[river[1]][river[0]]=-1
		return True

	def genStates(self):
		numislandList=self.getCellList()[2]
		newstateList=[]
		for numisland in numislandList:
			riveraround,islands=self.getRiverAroundIsland(numisland)
			if self.findCell2(numisland)> len(islands):
				bef=len(newstateList)
				for river in riveraround:
					newstate=Board(copy.deepcopy(self.coordinates))
					if newstate.setIsland(river,islands):
						newstateList.append(newstate)
				if bef==len(newstateList):
					return []
		return newstateList

	def checkGoal(self):
		riverList,islandList,numislandList=self.getCellList()
		returnVal=True
		#Check number of island
		totalIsland=sum(map(lambda cell:self.findCell2(cell),numislandList))
		if totalIsland != len(islandList) + len(numislandList):
			self.heuristic+=len(islandList)
			returnVAl= False
		# print("1")
		#check 4 block river
		blockCount=0
		for i in range(len(riverList)):
			cells=self.getCellBlock(riverList[i][0],riverList[i][1])
			count=0
			for j in range(i+1,len(riverList)):
				if isInList(cells,riverList[j],isSameCell):
					count+=1
			if count==3:
				blockCount+=1
				returnVal= False # there is 4 block river
		self.heuristic+=blockCount
		##
		# print("2")
		#Check river flow
		visited=[]
		prepare=[riverList[0]]
		while True:
			if len(prepare)==0:
				break
			curr=prepare.pop(0)
			visited.append(curr)
			cells=self.getCellAround(curr[0],curr[1])
			#list(map(lambda cell:prepare.append(cell) if cell is not None and self.typ(cell) and not isInList(visited,cell,lambda a,b:a.x==b.x and a.y==b.y) else False ,cells))
			for cell in cells:
				typ=self.typ2(cell)
				if typ is not None and typ==RIVER and not isInList(visited,cell,isSameCell ):
					prepare.append(cell)
		if len(visited)<len(riverList):
			self.heuristic -=self.size**2
			returnVal= False # there is isolated river
		# print("3")
		#check island
		for cell in numislandList:
			visited=[]
			prepare=[cell]
			while True:
				if len(prepare)==0:
					break
				curr=prepare.pop(0)
				visited.append(curr)
				cells=self.getCellAround(curr[0],curr[1])
				#list(map(lambda cell:prepare.append(cell) if cell is not None and self.typ(cell) and not isInList(visited,cell,lambda a,b:a.x==b.x and a.y==b.y) else False ,cells))
				for cell1 in cells:
					typ=self.typ2(cell1)
					if typ is None:
						continue
					elif typ==NUMISLAND and not isSameCell(cell1,cell):
						# print("3a")
						# print("x",curr[0])
						# print("y",curr[1])
						return False # contiguous islands
					elif typ==ISLAND and not isInList(visited,cell1,isSameCell):
						prepare.append(cell1)
			if len(visited) != self.findCell2(cell):
				# print("3b")	
				returnVal= False
		# print("4")
		return returnVal
	def getRiverAroundIsland(self,numisland):
		islands=[]
		riveraround=[]
		prepare=[numisland]
		while True:
			if len(prepare)==0:
				break
			curr=prepare.pop(0)
			islands.append(curr)
			cells=self.getCellAround(curr[0],curr[1])
			#list(map(lambda cell:prepare.append(cell) if cell is not None and self.typ(cell) and not isInList(visited,cell,lambda a,b:a.x==b.x and a.y==b.y) else False ,cells))
			for cell in cells:
				typcell=self.typ2(cell)
				if typcell is None:
					continue
				elif typcell==RIVER and not isInList(riveraround,cell,isSameCell):
					riveraround.append(cell)
				elif typcell==ISLAND and not isInList(islands,cell,isSameCell):
					prepare.append(cell)
		# #debug
		# print(riveraround)
		# print(islands)
		return riveraround,islands

	def getCellList(self):
		riverList=[]
		islandList=[]
		numislandList=[]
		for y in range(self.size):
			for x in range(self.size):
				if self.typ(x,y)==RIVER:
					riverList+=[[x,y]]
				elif self.typ(x,y)==ISLAND:
					islandList+=[[x,y]]
				else:
					numislandList+=[[x,y]]
		return riverList,islandList,numislandList
	def getTypCellAround(self,x,y):
		# above= self.typ(x,y-1)
		# below= self.typ(x,y+1)
		# right= self.typ(x+1,y)
		# left= self.typ(x-1,y)
		return self.typ(x,y-1),self.typ(x,y+1),self.typ(x+1,y),self.typ(x-1,y)
	def getCellBlock(self,x,y):
		"""
			x 1
			3 2
		"""
		return [[x+1,y],[x+1,y+1],[x,y+1]]
	def getCellAround(self,x,y):
		# above= (x,y-1)
		# below= (x,y+1)
		# right= (x+1,y)
		# left= (x-1,y)
		return [[x,y-1],[x,y+1],[x+1,y],[x-1,y]]
	def checkRiverAround(self,x,y):
		# check around if there is 3-block river
		#        1 2 3
		#		 8   4
		#		 7 6 5
		c1= self.typ(x-1,y-1)
		c2= self.typ(x,y-1)
		c3= self.typ(x+1,y-1)
		c4= self.typ(x+1,y)
		c5= self.typ(x+1,y+1)
		c6= self.typ(x,y+1)
		c7= self.typ(x-1,y+1) 
		c8= self.typ(x-1,y)
		if c1 is not None and c2 is not None and c8 is not None and c1==RIVER and c2==RIVER and c8==RIVER:
			return True
		elif c2 is not None and c3 is not None and c4 is not None and c2==RIVER and c3==RIVER and c4==RIVER:
			return True
		elif c4 is not None and c5 is not None and c6 is not None and c4==RIVER and c5==RIVER and c6==RIVER:
			return True
		elif c6 is not None and c7 is not None and c8 is not None and c6==RIVER and c7==RIVER and c8==RIVER:
			return True
		else:
			return False
	def compareCoordinate(a,b):
		for y in range(len(a)):
			for x in range(len(b)):
				if a[y][x]!=b[y][x]:
					return False
		return True
	def typ(self,x,y):
		num=self.findCell(x,y)
		if num is None:
			return None
		elif num == 0:
			return RIVER
		elif num == -1:
			return ISLAND
		else: 
			return NUMISLAND
	def typ2(self,cell):
		num=self.findCell2(cell)
		if num is None:
			return None
		elif num == 0:
			return RIVER
		elif num == -1:
			return ISLAND
		else: 
			return NUMISLAND
	def findCell(self,x,y):
		if x>=0 and y>=0 and x<len(self.coordinates) and y<len(self.coordinates):
			return self.coordinates[y][x]
		return None
	def findCell2(self,cell):
		if cell[0] >= 0 and cell[1] >= 0 and cell[0] < self.size and cell[1] < self.size:
			return self.coordinates[cell[1]][cell[0]]
		return None
def isSameCell(a,b):
	return a[0]==b[0] and a[1]==b[1]
def isInList(list,item,func):
	for i in list:
		if func(i,item):
			return True
	return False

def BFS(board):
	Open=[board]
	Closed=[]
	count=0
	while True:
		if len(Open)==0:
			print("Không tìm thấy kết quả")
			return None
		curr=Open.pop(0)
		newstateList=curr.genStates2()

		removeList=[]
		newlist=[]
		for i in range(len(newstateList)):
			if newstateList[i].checkGoal2():
				print("Solution")
				return newstateList[i]
			if newstateList[i].heuristic >0:
				newlist+=[newstateList[i]]
			else:
				removeList+=[newstateList[i]]
		newstateList=newlist

		#check newstate in closed

		for state in Closed:
			if len(newstateList)==0:
				break
			index=bisect_left(newstateList,state.heuristic,key= lambda x:x.heuristic)
			if index!=len(newstateList):
				for i in range(index,len(newstateList)):
					if newstateList[i].heuristic != state.heuristic:
						break
					elif Board.compareCoordinate(state.coordinates,newstateList[i].coordinates):
						newstateList.pop(i)
						break
		
		# Open.append(newstateList)
		# Open.sort(reverse=True,key=lambda x:x.heuristic)
		for state in newstateList:
			insort_left(Open,state,key=lambda x:x.heuristic)
		# Closed.append(curr)
		# closed.sort(key=lambda x:x.heuristic)
		insort_left(Closed,curr,key=lambda x:x.heuristic)
		for state in removeList:
			insort_left(Closed,state,key=lambda x:x.heuristic)
		#############- debug
		count+=1
		# if count==1:
		# 	return None
		print("Lần loop thứ ",count)
		print(len(Open))
		# for x in states:
		# 	x.PrintOut()

def main():
	# inputBoard=[[0,0,0,0,1],
	# 			[0,2,0,0,0],
	# 			[5,0,0,2,0],
	# 			[0,0,0,0,0],
	# 			[0,0,0,0,0]]
	# inputBoard=[[0,0,0],
	# 			[0,1,0],
	# 			[0,0,0]]
	# inputBoard=[[0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0]]
	# inputBoard=[[0, 0, 0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0, 0, 0],
	# 	        [0, 0, 0, 0, 0, 0, 0]]
	inputBoard=[[0, 0, 0, 4, 0],
		        [2, 0, 0, 0, 0],
		        [0, 0, 3, 0, 0],
		        [0, 0, 0, 1, 0],
		        [0, 0, 0, 0, 0]]
	
	board=Board(inputBoard)
	board.PrintOut()
	start = time.time()
	goal=BFS(board)
	end=time.time()
	process = psutil.Process(os.getpid())
	print("Thời gian chạy : ",end-start)
	print("Bộ nhớ đã dùng : ",process.memory_info().rss/ 1024 ** 2,"MB")
	if goal is not None:
	    goal.PrintOut()

main()