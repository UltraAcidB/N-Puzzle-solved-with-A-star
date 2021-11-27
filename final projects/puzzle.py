from copy import deepcopy
class Puzzle:
    def __init__(self,puzzle,parent=None,move=None):
        self.state=puzzle
        self.parent=parent
        self.move=move
        self.blank=(0,0)
        self.g=0 #path cost
        self.h=0 #heuristics function: Manhattan distance
        self.f=0 #evaluation function: f(n)=g(n)+h(n)
        self.blank=self.findBlankIndex()

    def __eq__(self,other):
        return self.state==other.state

    def findBlankIndex(self):
        for row in range(len(self.state)):
            for col in range(len(self.state)):
                if self.state[row][col]==0:
                    return row,col

    def manhattanDistance(self):# taxicab geometry
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                index=self.state[i][j]-1
                if index==-1:
                    distance=i+j #distance of of blank tile to its correct position with wraparound
                else:
                    distance=abs(i-(index/len(self.state)))+abs(j-(index%len(self.state))) #distance of other tiles to their correct positions with wraparound
                self.h+=distance
        return self.h
                     
    def sortMoves(self): #find all possible moves 
        moves=['up','down','left','right']
        x,y=self.blank
        if x==0:
            moves.remove('up')
        if x==(len(self.state)-1):
            moves.remove('down')
        if y==0: 
            moves.remove('left')
        if y==(len(self.state)-1):
            moves.remove('right')
        return moves

    def expand(self): #generate children
        successors=[]
        x,y=self.blank 
        moves=self.sortMoves()
        for m in moves: 
            new_puzzle=deepcopy(self.state) #copy all contents of the puzzle instead of referencing (deepcopy#shallowcopy)
            if m=='left':
                new_puzzle[x][y],new_puzzle[x][y-1]=new_puzzle[x][y-1],new_puzzle[x][y]
            if m=='right':
                new_puzzle[x][y],new_puzzle[x][y+1]=new_puzzle[x][y+1],new_puzzle[x][y]
            if m=='up':
                new_puzzle[x][y],new_puzzle[x-1][y]=new_puzzle[x-1][y],new_puzzle[x][y]
            if m=='down':
                new_puzzle[x][y],new_puzzle[x+1][y]=new_puzzle[x+1][y],new_puzzle[x][y]
            successors.append(Puzzle(new_puzzle,self,m))
        return successors        
    
    def solution(self): #return a list of moves 
        path=[]
        current=self
        while current.move is not None:
            path.append(current.move)
            current=current.parent
        return path[::-1]

#if use PriorityQueue, we cannot iterate through the open_list to narrow down the search space which make it took a long time to search and the result is not fully optimized.
#Hence, I decide to use list here in order to delete repeative value and narrow down the search.
#With the same problem, when applied priority queue, it took me approximately 3-5 minutes to get the solution, while using list with multiple conditions it took me about 5-10 seconds.
def aStar(problem,goal): 
    startNode=Puzzle(problem,None,None)
    endNode=Puzzle(goal,None,None)

    open_list=[]

    closed_list=[]

    open_list.append(startNode)
    while len(open_list):
        current=open_list[0]
        curr_index=0
        for index,item in enumerate(open_list):
            if item.f<current.f:
                current=item
                curr_index=index

        open_list.pop(curr_index)
        closed_list.append(current)

        if current.state==endNode.state:
            return current.solution()

        children=current.expand()

        for child in children:
            child.g=current.g+1
            child.h=child.manhattanDistance()
            child.f=child.g+child.h
            for open_node in open_list:
                if child==open_node and child.g<open_node.g:
                    open_list.remove(open_node)

            for closed_node in closed_list:
                if child==closed_node and child.g>closed_node.g:
                    closed_list.remove(closed_node)

            open_list.append(child)
          
if __name__ == '__main__':
    problem=[[3,1,2],[6,0,8],[7,5,4]] #easy: 10sec
    #problem=[[1,2,7],[3,4,5],[0,6,8]] #hard: approximate 6min
    goal=[[0,1,2],[3,4,5],[6,7,8]]
    solution=aStar(problem,goal)
    print(solution)
