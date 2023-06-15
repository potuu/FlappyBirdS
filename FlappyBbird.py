import pygame
import numpy
import math
from QL import ql
pygame.init()

Width = 600
Height = 400

birdpos = Height/2
SCWidth = Width

bg = pygame.image.load('data/bg.png')
bg = pygame.transform.scale(bg,(Width,Height))

bird = pygame.image.load('data/bird.png')
bird = pygame.transform.scale(bird,(Width*2//27,Height//9))

pipe = pygame.image.load('data/pipe.png')
pipe = pygame.transform.scale(pipe,(Width//6,int(100*Width/(6*14))))
pipeImgH = int(100*Width/(6*14))
Rpipe = pygame.transform.flip(pipe,False,True)
win = pygame.display.set_mode(size = (Width,Height))
pygame.display.set_caption("Flappy bird")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 50)

#number of pipe show on screen
pipenumber = 3

Width = int(Width*(1+1/pipenumber))
#global pipepos
pipepos = SCWidth + SCWidth//12 + 3
exist = []
pipeHeight = []
for i in range(pipenumber):
    exist.append(False)
    pipeHeight.append(numpy.random.uniform(0.4,0.7))
    
def drawWin():
    global pipeHeight
    win.blit(bg,(0,0))
    for i in range(pipenumber):
        if (exist[i]):
            x = pipepos-i*Width//pipenumber-SCWidth//12
            if x<-SCWidth//6:
                x += Width 
            if x>Width - SCWidth//6:
                x -= Width
            y = Height*pipeHeight[i]
            win.blit(pipe,(x,y))
            y -= pipeImgH + Height*0.4
            win.blit(Rpipe,(x,y))
    win.blit(bird,(SCWidth//4-SCWidth//27,birdpos-Height//12))
    if score == -1:
        textsurface = myfont.render('Score : '+str(0), False, (0, 0, 0))
    else:
        textsurface = myfont.render('Score : '+str(int(score)), False, (0, 0, 0))
    win.blit(textsurface,(0,0))
    pygame.display.update()



def IsOutofScreen(i):
    x = pipepos-i*Width//pipenumber
    if x<-SCWidth//12:
        x += Width 
    if x>Width - SCWidth//6:
        x -= Width
    if x>SCWidth+SCWidth//12:
        return True
    else:
        return False

'''
deal with jumps and Moves
'''

vel = 0
JumpHeight = Height*0.06
grav = 0.5 
timerate = 10
difficulty = 0.5
score = -1
Bestscore = 0
def jump():
    global vel
    vel = -math.sqrt(2*JumpHeight*grav)
    
def moveBird():
    global vel,birdpos
    birdpos += int(vel)
    vel += grav*timerate*difficulty
    if birdpos>Height:
        birdpos = Height
        vel = 0
    if birdpos < 0:
        birdpos = 0
        vel = 0
        
def movePipe():
    global pipepos
    pipepos -= timerate
    if(pipepos<0):
        pipepos += Width
    for i in range(pipenumber):
        if IsOutofScreen(i):
            pipeHeight[i]=numpy.random.uniform(0.4,0.7)
            
def collision():
    if birdpos == Height:
        print('Hit ground')
        return True
    for i in range(pipenumber):
        if not exist[i]:
            continue
        x = pipepos-i*Width//pipenumber-SCWidth//12
        if x<-SCWidth//6:
            x += Width 
        if x>Width - SCWidth//6:
            x -= Width
        x += SCWidth//12
        yh = Height*pipeHeight[i]
        bx = SCWidth//4
        if abs(bx-x)>=SCWidth//12+SCWidth//27:
            continue
        if (yh - birdpos)>=Height//27 and (yh - birdpos)<=Height*0.4-Height*2//27:
            pass
        else:
            print('Hit pipe'+str(i))
            return True
    return False
    
def reset():
    global birdpos,score,pipepos,vel,exist,pipeHeight
    birdpos = Height//2
    score = -1
    vel = 0
    pipepos = SCWidth + SCWidth//12 + 3
    for i in range(pipenumber):
        exist[i] = False
        pipeHeight[i] = numpy.random.uniform(0.4,0.85)
        
'''
AI Functions
'''
def getstate():
    nextpipe = -1
    distance = Width*2
    for i in range(pipenumber):
        if not exist[i]:
            continue
        x = pipepos-i*Width//pipenumber-SCWidth//12
        if x<-SCWidth//6:
            x += Width 
        if x>Width - SCWidth//6:
            x -= Width
        x += SCWidth//12
        bx = SCWidth//4
        if abs(bx-x)<=SCWidth//12+SCWidth//27:
            distance = x-bx+SCWidth//12
            nextpipe = i
            break
        if x-bx<distance and x>bx:
            distance = x-bx+SCWidth//12
            nextpipe = i
    pHeight = int(pipeHeight[nextpipe]*20)
    distance = int(10*distance/(Width/pipenumber))
    ground = int(20*birdpos/Height)
    #print('\npHeight :',pHeight,'\ndistance :',distance,'\nground : ',ground,'\nstate : ',distance*1+(pHeight-ground)*20 )
    return distance*1+(pHeight-ground)*10+int(vel/10)*200

def getNextpipe():
    nextpipe = -1
    distance = Width*2
    for i in range(pipenumber):
        if not exist[i]:
            continue
        x = pipepos-i*Width//pipenumber-SCWidth//12
        if x<-SCWidth//6:
            x += Width 
        if x>Width - SCWidth//6:
            x -= Width
        x += SCWidth//12
        bx = SCWidth//4
        if abs(bx-x)<=SCWidth//12+SCWidth//27:
            distance = x-bx+SCWidth//12
            nextpipe = i
            break
        if x-bx<distance and x>bx:
            distance = x-bx+SCWidth//12
            nextpipe = i
    return nextpipe

def getReward():
    yh = Height*pipeHeight[getNextpipe()]
    if (yh - birdpos)>=0 and (yh - birdpos)<=Height*0.4-SCWidth//24:
        return 1
    else:
        return -1
    
AI = ql(2000,2,0.85,0.95) 
AI.Load('data/birdking.json')         
run = True
start = False
launch = False
Human = False
state = 0
actionrate = 1
Turncount = 0
while run:
    Turncount += 1
    drawWin()
    if Human:
        pygame.time.delay(5)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if not launch:
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_SPACE]:
            launch = True
        continue
    if Human:
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_SPACE]:
            if not start:
                start = True
                reset()
            if start:
                jump()
    else:
        if not start:
            newstate = getstate()
            #AI.Reward(state,newstate,-100)
            reset()
            start = True
        if Turncount%actionrate == 0:
            old_state = state
            state = getstate()
            #if not old_state == state:
            action = AI.Action(state)
            if action == 1:
                jump()
        
    for i in range(pipenumber):
        if (not exist[i])and IsOutofScreen(i) :
            exist[i] = True
            break
    if collision():
        start = False
        print('Gameover')
    moveBird()
    movePipe()
    score += timerate*pipenumber/(Width)
    if score>Bestscore:
        Bestscore = score
    if (not Human) and Turncount%actionrate==0:
        newstate = getstate()
        if newstate == state:
            continue
        reward = getReward()
        #AI.Reward(state,newstate,1)
    
print('Best Score',int(Bestscore))
pygame.quit()
