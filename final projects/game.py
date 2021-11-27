import random,sys

sys.path.append('C:/academic folder/projects/artificial intelligence/final projects')

import puzzle as pz
import pygame
from pygame.locals import *
from pygame.display import update

#Puzzle settings
PUZZLEWIDTH=3 
PUZZLEHEIGHT=3
TILESIZE=120
#windows settings
WINDOWHEIGHT=480
WINDOWWIDTH=640
FPS=30

#Define colors
BLACK=(0,0,0)
WHITE=(255,255,255)
BRIGHTBLUE=(0,50,255)
GREEN=(0,204,0)
DARKTURQUOISE=(3,54,73)
RED=(255,0,0)

#Utilities
BGCOLOR=DARKTURQUOISE
BORDERCOLOR=RED
TILECOLOR =GREEN
TEXTCOLOR=BLACK

#Buttons settings
MESSAGECOLOR=WHITE
BUTTONCOLOR=WHITE
BUTTONTEXTCOLOR=BLACK
BASICFONTSIZE=20
INDEXFONTSIZE=35

YMARGIN = int((WINDOWWIDTH - (TILESIZE * PUZZLEWIDTH + (PUZZLEWIDTH - 1))) / 2)
XMARGIN = int((WINDOWHEIGHT - (TILESIZE * PUZZLEHEIGHT + (PUZZLEHEIGHT - 1))) / 2)

def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,INDEXFONT,NEW_SURF,NEW_RECT,SOLVE_RECT,SOLVE_SURF
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT=pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)
    INDEXFONT=pygame.font.Font('freesansbold.ttf',INDEXFONTSIZE)
    
    NEW_SURF,NEW_RECT=drawText('NEW',BUTTONTEXTCOLOR,BUTTONCOLOR,WINDOWWIDTH-120,WINDOWHEIGHT-30)
    SOLVE_SURF,SOLVE_RECT=drawText('Solve',BUTTONTEXTCOLOR,BUTTONCOLOR,WINDOWWIDTH-120,WINDOWHEIGHT-60)

    GOAL=getStartingPuzzle()
    puzzle=randomizePuzzle(40)
    pygame.display.set_caption('N puzzle')
    while True:
        msg='Solving...'
        if puzzle==GOAL:
            msg='Solved!'
        drawPuzzle(msg,puzzle)
        for event in pygame.event.get():
            if event.type==MOUSEBUTTONUP:
                if NEW_RECT.collidepoint(event.pos):
                    puzzle=randomizePuzzle(40)
                elif SOLVE_RECT.collidepoint(event.pos):
                    puzzleSolver(puzzle,GOAL)
            elif event.type==QUIT:
                pygame.quit()
                sys.exit()       
        pygame.display.update()           
        FPSCLOCK = pygame.time.Clock()


def drawText(text,color,bgcolor,left,top): 
    textSurf=BASICFONT.render(text,True,color,bgcolor) #(text,antialias,color,background color)
    textRect=textSurf.get_rect()
    textRect.topleft=(left,top)
    return (textSurf,textRect)

def getLeftTopOfTile(tilex,tiley): 
    left=XMARGIN+(tilex*TILESIZE)+(tilex-1)
    top=YMARGIN+(tiley*TILESIZE)+(tiley-1)
    return (left,top)


def drawTile(tilex,tiley,text,adjx=0,adjy=0):
    left,top=getLeftTopOfTile(tilex,tiley)
    pygame.draw.rect(DISPLAYSURF,TILECOLOR,(top+adjx,left+adjy,TILESIZE,TILESIZE))
    #indexing the pieces of puzzle
    textSurf=INDEXFONT.render(str(text),True,TEXTCOLOR)
    textRect=textSurf.get_rect()
    textRect.center=top+int(TILESIZE/2)+adjx,left+int(TILESIZE/2) +adjy
    DISPLAYSURF.blit(textSurf,textRect)

def drawPuzzle(msg,puzzle):
    DISPLAYSURF.fill(BGCOLOR)
    if msg:
        textSurf,textRect=drawText(msg,MESSAGECOLOR,BGCOLOR,5,5)
        DISPLAYSURF.blit(textSurf,textRect)
    for x in range(PUZZLEHEIGHT):
        for y in range(PUZZLEWIDTH):
            if puzzle[x][y]:
                drawTile(x,y,puzzle[x][y])
    #draw the border of the puzzle
    left,top=getLeftTopOfTile(0,0)
    width=PUZZLEWIDTH*TILESIZE
    height=PUZZLEHEIGHT*TILESIZE
    pygame.draw.rect(DISPLAYSURF,BORDERCOLOR,(top-5,left-5,height+11,width+11),4)
    #draw the buttons
    DISPLAYSURF.blit(NEW_SURF,NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF,SOLVE_RECT)
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

def findBlankIndex(puzzle):
    for x in range(PUZZLEWIDTH):
        for y in range(PUZZLEHEIGHT):
            if puzzle[x][y]==0:
                return (x,y)
                
def isValidMove(puzzle,move):
    x,y=findBlankIndex(puzzle)
    return(move=='up' and x!=0) or\
        (move=='down' and x!=(PUZZLEWIDTH-1)) or\
        (move=='left' and y!=0) or\
        (move=='right' and y!=(PUZZLEHEIGHT-1))

def getRandomMove(puzzle,lastMove=None): #find all possible moves 
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
    drawPuzzle(msg,puzzle)
    baseSurf=DISPLAYSURF.copy()
    moveLeft,moveTop=getLeftTopOfTile(movex,movey)
    pygame.draw.rect(baseSurf,BGCOLOR,(moveTop,moveLeft,TILESIZE,TILESIZE))
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

#generate the problem
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
        lastMove==move
    return puzzle

def puzzleSolver(initial,goal):
    solution=pz.aStar(initial,goal)
    for move in solution:
        slideAnimation(initial,move,'',int(TILESIZE/10))
        doMove(initial,move)

if __name__=='__main__':
    main()   
        

        



    







