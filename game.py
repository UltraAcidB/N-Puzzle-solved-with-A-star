import random,sys

from pygame import mouse

sys.path.append('C:/academic folder/projects/artificial intelligence/final projects')

import puzzle as pz
import pygame
from pygame.locals import *
from pygame.display import update
import os
import multiprocessing
import time
#Puzzle settings
PUZZLEWIDTH=3 
PUZZLEHEIGHT=3
TILESIZE=140
#windows settings
WINDOWWIDTH=800
WINDOWHEIGHT=600
FPS=30

#Define colors
BLACK='#000000'
WHITE='#FFFFFF'

#Utilities
BGCOLOR='#C8D6B9'
BORDERCOLOR='#8FC1A9'
TILECOLOR ='#7CAA98'

#Buttons settings
TEXTCOLOR=BLACK
MESSAGECOLOR=BLACK
INDEXCOLOR=WHITE
BASICFONTSIZE=26
INDEXFONTSIZE=40

YMARGIN = int((WINDOWWIDTH - (TILESIZE * PUZZLEWIDTH + (PUZZLEWIDTH - 1))) / 3)
XMARGIN = int((WINDOWHEIGHT - (TILESIZE * PUZZLEHEIGHT + (PUZZLEHEIGHT - 1))) / 3)

def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,INDEXFONT,EASY,NORMAL,HARD,RANDOM,SOLVE
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    #set window mode: BORDERlESS WINDOWED
    #os.environ['SDL_VIDEO_CENTERED']='1' 
    #DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT),pygame.NOFRAME)
    #set window mode: WINDOWED
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

    #fonts
    BASICFONT=pygame.font.SysFont('inkfree',BASICFONTSIZE)
    INDEXFONT=pygame.font.SysFont('inkfree',INDEXFONTSIZE)
    #initiate buttons
    EASY=button('Easy',200,40,(WINDOWWIDTH-220,WINDOWHEIGHT-400),5)
    NORMAL=button('Normal',200,40,(WINDOWWIDTH-220,WINDOWHEIGHT-350),5)
    HARD=button('Hard',200,40,(WINDOWWIDTH-220,WINDOWHEIGHT-300),5)
    RANDOM=button('New',200,40,(WINDOWWIDTH-220,WINDOWHEIGHT-250),5)
    SOLVE=button('Solve',200,40,(WINDOWWIDTH-220,WINDOWHEIGHT-200),5)
    
    pygame.display.set_caption('N puzzle')
    GOAL=getStartingPuzzle()
    puzzle=GOAL
    process=None
    while True: #running
        msg=''
        if puzzle==GOAL:
            msg='Solved!'
        drawPuzzle(msg,puzzle)
        for event in pygame.event.get(): #events handling
            if event.type==MOUSEBUTTONUP:
                if EASY.pressed==True: 
                    puzzle=[[3,1,2],[6,0,8],[7,5,4]]
                elif NORMAL.pressed==True:
                    puzzle=[[4,0,1],[5,8,2],[7,6,3]]
                elif HARD.pressed==True:
                    puzzle=[[1,2,7],[3,5,4],[0,6,8]]
                elif RANDOM.pressed==True:
                    puzzle=randomizePuzzle(10)
                elif SOLVE.pressed==True:                    
                    puzzleSolver(puzzle,GOAL)
            elif event.type==QUIT:
                pygame.quit()
                sys.exit()  
        pygame.display.update()           
        FPSCLOCK = pygame.time.Clock()

class button:
    def __init__(self,text,width,height,position,elevation):
        #Core attributes
        self.pressed=False
        self.elevation=elevation
        self.dynamic_elevation=elevation
        self.original_y_pos=position[1]
        
        #top rectangle
        self.top_rect=pygame.Rect(position,(width,height))
        self.top_color='#475F77'

        #bottom rectangle
        self.bottom_rect=pygame.Rect(position,(width,height))
        self.bottom_color='#7CAA98'

        #text
        self.text_surf=BASICFONT.render(text,True,'#FFFFFF')
        self.text_rect=self.text_surf.get_rect(center=self.top_rect.center)
    
    def draw(self):
        #elevation logic
        self.top_rect.y=self.original_y_pos-self.dynamic_elevation
        self.text_rect.center=self.top_rect.center

        self.bottom_rect.midtop=self.top_rect.midtop
        self.bottom_rect.height=self.top_rect.height+self.dynamic_elevation

        pygame.draw.rect(DISPLAYSURF,self.bottom_color,self.bottom_rect,border_radius=12)
        pygame.draw.rect(DISPLAYSURF,self.top_color,self.bottom_rect,border_radius=12)

        DISPLAYSURF.blit(self.text_surf,self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color='#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation=0
                self.pressed=True
            else:
                self.dynamic_elevation=self.elevation
                if self.pressed==True:
                    self.pressed=False
        else:
            self.dynamic_elevation=self.elevation
            self.top_color='#7CAA98'

def drawText(text,color,bgcolor,left,top): 
    textSurf=BASICFONT.render(text,True,color,bgcolor) #(text,anti aliasing,color,background color)
    textRect=textSurf.get_rect()
    textRect.topleft=(left,top)
    return (textSurf,textRect)

def getLeftTopOfTile(tilex,tiley): 
    left=XMARGIN+(tilex*TILESIZE)+(tilex-1)+50
    top=YMARGIN+(tiley*TILESIZE)+(tiley-1)
    return (left,top)

def drawTile(tilex,tiley,text,adjx=0,adjy=0):
    left,top=getLeftTopOfTile(tilex,tiley)
    pygame.draw.rect(DISPLAYSURF,TILECOLOR,(top+adjx,left+adjy,TILESIZE,TILESIZE),0,3) #(surface,color,rect(),width,border)
    #indexing each tile of the puzzle
    textSurf=INDEXFONT.render(str(text),True,INDEXCOLOR)
    textRect=textSurf.get_rect()
    textRect.center=top+int(TILESIZE/2)+adjx,left+int(TILESIZE/2) +adjy
    DISPLAYSURF.blit(textSurf,textRect)

#draw the puzzle
def drawPuzzle(msg,puzzle):
    DISPLAYSURF.fill(BGCOLOR) 
    if msg:
        textSurf,textRect=drawText(msg,MESSAGECOLOR,BGCOLOR,5,5)
        DISPLAYSURF.blit(textSurf,textRect)
    #draw each tile of the puzzle except the blank
    for x in range(PUZZLEHEIGHT):
        for y in range(PUZZLEWIDTH):
            if puzzle[x][y]:
                drawTile(x,y,puzzle[x][y])
    #draw the border of the puzzle
    left,top=getLeftTopOfTile(0,0)
    width=PUZZLEWIDTH*TILESIZE
    height=PUZZLEHEIGHT*TILESIZE
    pygame.draw.rect(DISPLAYSURF,BORDERCOLOR,(top-5,left-5,height+11,width+11),5)
    #draw the buttons
    EASY.draw()
    HARD.draw()
    NORMAL.draw()
    RANDOM.draw()
    SOLVE.draw()
    pygame.display.update()

#get the initial/goal puzzle
def getStartingPuzzle():
    counter=0
    puzzle=[]
    for x in range(PUZZLEWIDTH):
        row=[]
        for y in range(PUZZLEHEIGHT):
            row.append(counter)
            counter+=1
        puzzle.append(row)
    return puzzle

#find position of the blank 
def findBlankIndex(puzzle):
    for x in range(PUZZLEWIDTH):
        for y in range(PUZZLEHEIGHT):
            if puzzle[x][y]==0:
                return (x,y)

#check if the move is valid                
def isValidMove(puzzle,move):
    x,y=findBlankIndex(puzzle)
    return(move=='up' and x!=0) or\
        (move=='down' and x!=(PUZZLEWIDTH-1)) or\
        (move=='left' and y!=0) or\
        (move=='right' and y!=(PUZZLEHEIGHT-1))

#find all possible moves 
def getRandomMove(puzzle,lastMove=None): 
    moves=['up','down','left','right']
    if lastMove=='down' or not isValidMove(puzzle,'up'):
        moves.remove('up')
    if lastMove=='up' or not isValidMove(puzzle,'down'):
        moves.remove('down')
    if lastMove=='right' or  not isValidMove(puzzle,'left'):
        moves.remove('left')
    if lastMove=='left' or not isValidMove(puzzle,'right'):
        moves.remove('right')
    return random.choice(moves)

#make move based on the blank position
def doMove(puzzle,move):
    x,y=findBlankIndex(puzzle)
    if move=='up':
        puzzle[x][y],puzzle[x-1][y]=puzzle[x-1][y],puzzle[x][y]
    if move=='down':
        puzzle[x][y],puzzle[x+1][y]=puzzle[x+1][y],puzzle[x][y]
    if move=='left':
        puzzle[x][y],puzzle[x][y-1]=puzzle[x][y-1],puzzle[x][y]
    if move=='right':
        puzzle[x][y],puzzle[x][y+1]=puzzle[x][y+1],puzzle[x][y]

#do the sliding animation  
def slideAnimation(puzzle,move,msg,animationSpeed):
    x,y=findBlankIndex(puzzle)
    if move=='up':
        movex=x-1
        movey=y
    elif move=='down':
        movex=x+1
        movey=y
    elif move=='left':
        movex=x
        movey=y-1
    elif move=='right':
        movex=x
        movey=y+1
    #prepare the base surface
    drawPuzzle(msg,puzzle)
    baseSurf=DISPLAYSURF.copy()
    #draw a blank space over the moving tile on the baseSurf.
    moveLeft,moveTop=getLeftTopOfTile(movex,movey)
    pygame.draw.rect(baseSurf,BGCOLOR,(moveTop,moveLeft,TILESIZE,TILESIZE))
    #animate the tile sliding over per frame
    for i in range(0,TILESIZE,animationSpeed):
        DISPLAYSURF.blit(baseSurf,(0,0))
        if move=='up':
            drawTile(movex,movey,puzzle[movex][movey],0,i)
        if move=='down':
            drawTile(movex,movey,puzzle[movex][movey],0,-i)
        if move=='left':
            drawTile(movex,movey,puzzle[movex][movey],i,0)
        if move=='right':
            drawTile(movex,movey,puzzle[movex][movey],-i,0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#generate randomized problem
def randomizePuzzle(num):
    puzzle=getStartingPuzzle()
    drawPuzzle('',puzzle)
    pygame.display.update()
    pygame.time.wait(500)
    lastMove=None
    for i in range(num):
        move=getRandomMove(puzzle,lastMove)
        slideAnimation(puzzle,move,'Generating new puzzle...',int(TILESIZE/10))
        doMove(puzzle,move)
        lastMove=move
    return puzzle

def puzzleSolver(initial,goal):
    solution=pz.aStar(initial,goal)
    print(solution)
    for move in solution:
        slideAnimation(initial,move,'Solving...',int(TILESIZE/10))
        doMove(initial,move)

def longTask():
    i=0
    while i<50:
        time.sleep(0.1)
        i+=1
    return i
if __name__=='__main__':
    main()   

#Preferences
# Ai Sweigart, Making Games with Python & Pygame
# Stuart J. Russell and Peter Norvig, Artificial IntelligenceA Modern Approach Third Edition
# Clear Code, Creating an animated button in Pygame

        



    







