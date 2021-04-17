#!/usr/bin/python3

from time import sleep
import os
import _thread
import random
import sys
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


pygame.init()
hFont = pygame.font.Font("freesansbold.ttf", 26)
font = pygame.font.Font("freesansbold.ttf", 16)
pygame.display.set_caption("E-VOLVE Sim")
popCount = popCount_t = 0
SCREEN_W = 1200
SCREEN_H = 900
WIN = 500 # window size
WIN_2X = WIN/1.9
WIN_2Y = WIN*1.5
color = {"black":(0,0,0), "gray":(170,170,170), "white":(255,255,255), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "pink":(255,0,255), "yellow":(255,255,0), "cyan":(0,255,255),
         "bk":(0,0,0), "gy":(170,170,170), 'w':(255,255,255), 'r':(255,0,0), 'g':(0,255,0), 'b':(0,0,255), 'p':(255,0,255), 'y':(255,255,0), 'c':(0,255,255)}
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
running = True
pops = pygame.sprite.Group()
verboseMode = "-v" in sys.argv
t = 1
maxGen = 0
phenotypes = {'a':[], 'A':[], 'm':[]}
q = p = r = 0 
dominantP = recessiveP = mutantP = -1
genlist = []
randomMate = True
noSelection = True
noMutation = True

def verbose(msg):
    if verboseMode:
        print(msg)

def findPop(idPop):
    for i in pops:
        if i.Id == idPop:
            return i
    return 0

def error(msg):
    print(">\u001b[31;1mERROR:\u001b[0m " + msg)

class Pop(pygame.sprite.Sprite):
    def __init__(self, position, Color=None, parents=None):
        global pops
        global running
        global phenotypes
        global maxGen
        super(Pop, self).__init__()
        self.alive = True
        if parents is not None:    
            self.gtype = parents[0].gtype[random.randint(0,1)]+parents[1].gtype[random.randint(0,1)]
            self.gen = parents[0].gen + 1
            if self.gen >= maxGen:
                verbose(f">Cannot exceed F{maxGen}!")
                self.alive = False
                return
        else:
            self.gtype = list(phenotypes.keys())[random.randint(0,1)]*2
            self.gen = 0
        genlist.append(self.gen)
        if not noMutation and not random.randint(0,3):
            self.gtype = self.gtype[0]+'m'
            verbose(">{self.Id} is a mutant")
        self.surf = pygame.Surface((25,25))
        self.gender = "-m" if random.randint(0,1) else "-f"
        if 'A' in self.gtype: 
            self.clr = dominantP
        elif 'm' in self.gtype:
            self.clr = mutantP
        else:
            self.clr = recessiveP
        if self.clr == -1: self.clr = tuple(map(lambda x,y : (x+y)/2, parents[0].clr, parents[1].clr)) if Color is None else Color
        self.attracted = False
        self.pregnant = False
        self.surf.fill(self.clr)
        self.Id = 10000000
        while findPop(self.Id):
            self.Id = random.randint(10000000, 99999999)
        self.pos = position
        verbose(f">{self.Id}: Position is now {self.pos}")
        pops.add(self)
        verbose(f">{self.Id}: Added self to pops list")
        _thread.start_new_thread(self.move, ())
        _thread.start_new_thread(self.mate, ())
        _thread.start_new_thread(self.age, ())
    def age(self):
        global t
        if running and self.alive:
            sleep(t*30)
        self.alive = False
        pops.remove(self)
        for i in self.gtype:
            try:
                phenotypes[i].remove(self.Id)
            except ValueError:
                continue
    def move(self):
        global t
        global running
        movement = lambda Pos : Pos+(random.choice([-1,1])*random.choice([0,5,10,25,50]))
        while running and self.alive:
            sleep(0.125*t)
            self.cachePos = self.pos
            self.pos = (0,0)
            while not ((self.pos[0] > ((SCREEN_W-WIN)/2)-(WIN/4) and self.pos[0] < (SCREEN_W/2)+(WIN/4)) and (self.pos[1] > (SCREEN_H-WIN)/2 and self.pos[1] < (SCREEN_H/2)+(WIN/2))):
                self.pos = (movement(self.cachePos[0]), movement(self.cachePos[1]))
            verbose(f">{self.Id}: Position is now {self.pos}")
            if not random.randint(0,19) and not noSelection:
                self.enemySurf = pygame.Surface((25,25))
                self.enemySurf.fill(color['p'])
                screen.blit(self.enemySurf, (self.pos[0]+5, self.pos[1]+5))
                verbose(f">{self.Id}: Encountered an enemy")
                sleep(t)
                if random.randint(1,100) > (80 if 'A' in self.gtype else 50):
                    self.alive = False
                    verbose(f">{self.Id}: Lost to enemy")
                else:
                    verbose(f">{self.Id} Won against enemy")
                    del self.enemySurf
    def pregnate(self, father):
        global t
        global running
        if self.alive and running: # Necrophilia is not allowed
            self.pregnant = True
            sleep(t*2)
            Pop(self.pos, Color=None, parents=[self, father])
            self.pregnant = False
    def mate(self):
        global running
        global t
        global pops
        global maxGen
        while (running and self.alive):
            if self.gen+1 > maxGen:
                continue
            sleep(t*11)
            self.attracted = True
            verbose(f">{self.Id}: Prepared to mate")
            for i in pops:
                if i.gender != self.gender and i.attracted and self.gen == i.gen: # my game has to be homophobic, sorry :\ ; at least I'm preventing pedophilia *and* nonconsensual relationships!
                    self.pos = i.pos
                    if not randomMate and 'm' not in i.gtype:
                        continue
                    if self.gender == "-m" and not i.pregnant:
                        _thread.start_new_thread(i.pregnate, (self,))
def colorize(Color):
    for i in Color:
        try:
            int(i)
        except ValueError:
            try:
                Color = color[Color[0]]
            except KeyError:
                error("Unknown color")
                return -1
        return Color

hwe = lambda : p**2 + 2*p*q + q**2

def sab(cin, t, msg):
    if len(cin) == 2:
        error("No `int` was provided")
    elif len(cin) == 1:
        print(f">{msg}: {t}")
    else:
        try:
            if cin[1] == "set" or cin[1] == '=':
                t = int(cin[2])
            elif cin[1] == "add" or cin[1] == '+':
                t += int(cin[2])
            elif cin[1] == "sub" or cin[1] == '-':
                t -= int(cin[2])
            else:
                error("Unknown option [valid options are set(=),add(+),sub(-)]")
        except ValueError:
            error("Expected type `int`")
    return t

def console():
    global running
    print(">E-VOLVE console activated (cOMManDs ArE cASE SeNSiTIVe)")
    while running:
        cin = input(">>").split("&&")
        for i in cin:
            consoleTwo(i.split())
def consoleTwo(cin):
    global running
    global dominantP
    global recessiveP
    if cin[0] == "kill":
        if "-r" in cin:
            cin.remove("-r")
            try:
                if int(cin[1]) > len(pops):
                        error("Selected no. of pops cannot be greater than actual no. of pops")
                        return
                for i in range(int(cin[1])):
                    pops.remove(list(pops)[random.randint(0,len(pops)-1)])
            except ValueError:
                error("No. of pops must be type `int`" if len(cin) > 1 else "No. of pops not provided")
            return
        try:
            if 10000000 <= int(cin[1]) <= 99999999:
                pops.remove(findPop(int(cin[1])))
                print(">Killed " + cin[1])
            else:
                raise ValueError
        except ValueError:
            error("Invalid ID! Valid IDs are integers >= 10000000 && <= 99999999")
    elif cin[0] == "paint":
        cin.remove("paint")
        Color = colorize(tuple([i for i in cin if not i.startswith("-")]))
        try:
            if "-a" in cin:
                for i in pops:
                    i.clr = Color
                    verbose(f">{i.Id}: Was painted {Color}")
                    return
            if "-d" in cin:
                for i in pops:
                    if 'A' in i.gtype:
                        i.clr = Color
            elif "-r" in cin:
                for i in pops:
                    if i.gtype == "aa":
                        i.clr = Color
            if ("-m" in cin) != ("-f" in cin):
                for i in pops:
                    if i.gender in cin:
                        i.clr = Color
                        verbose(f">{i.Id}: Was painted {Color}")
        except IndexError:
            error("Color must be provided")
    elif cin[0] == "clear":
        os.system("clear")
    elif cin[0] == "pheno":
        if len(cin) == 1:
            error("Insufficient args")
            return
        if cin[1] == "dom":
            dominantP = colorize(cin[2])
        elif cin[1] == "rec":
            recessiveP = colorize(cin[2])
        elif cin[1] == "mut":
            global noMutation
            global mutantP
            mutantP = colorize(cin[2])
            noMutation = False
        else:
            error("Second arg must be 'dom', 'mut', or 'rec'")
    elif cin[0] == "smate":
        global randomMate
        randomMate = False
    elif cin[0] == "spawn":
        Color = ()
        if "-c" in cin:
            Color = colorize(tuple(cin[cin.index("-c")+1:]))
            if Color == -1:
                return
            cin = cin[:cin.index("-c")]
        if len(cin) > 1 and cin[1] == "enemy":
            global noSelection
            noSelection = False
            return
        j = 1
        try:
            j = int(cin[1])
        except (IndexError, ValueError): #TODO: Add multiple species and move IndexError to its own except
            pass
        for i in range(j):
            pops.add(Pop((random.randint(((SCREEN_W-WIN)/2)-(WIN/4), (SCREEN_W/2)+(WIN/4)), random.randint((SCREEN_H-WIN)/2, (SCREEN_H/2)+(WIN/2))), (0,0,255) if len(Color) != 3 else Color))
    elif cin[0] == "hwe":
        print(f">{int(hwe()) == 1}")
    elif cin[0] == "exit":
        running = False
    elif cin[0] == "ls":
        for k, i in enumerate(pops):
            print(f">ID={i.Id} GENOTYPE={i.gtype} GENERATION=F{i.gen} GENDER={i.gender[1]} COLOR={list(color.keys())[list(color.values()).index(i.clr)] if i.clr in list(color.values()) else i.clr}{',' if k != len(pops) else ''}")
        print(f">{len(pops)} total pops.")
    elif cin[0] == "tick":
        global t
        t = sab(cin, t, "TICK SPEED")
    elif cin[0] == "maxgen":
        global maxGen
        maxGen = sab(cin, maxGen, "MAX GENERATION") + 1
    elif cin[0] == 'p':
        global p
        p = sab(cin, p, 'p')
    elif cin[0] == 'q':
        global q
        q = sab(cin, q, 'q')
    elif ' '.join(cin).strip() == "coconut mall":
        print(">You got coconut malled! Share this with your friends to totally coconut mall them!")
        running = False
    else:
        error("Unknown command")

_thread.start_new_thread(console, ())

header = hFont.render(">E-VOLVE :: STATS", None, color['g'])
sidebar = [3+(SCREEN_W/2)+((3*WIN)/5),(SCREEN_H-WIN_2Y)/2]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(color["bk"])
    pygame.draw.rect(screen, color['w'], [((SCREEN_W-WIN)/2)-(WIN/4),(SCREEN_H-WIN)/2,WIN,WIN])
    pygame.draw.rect(screen, color["gy"], [sidebar[0]-3,sidebar[1],WIN_2X,WIN_2Y])
    for pop in pops:
        if not pop.alive:
            for i in pop.gtype:
                try:
                    phenotypes[i].remove(pop.Id)
                except ValueError:
                    pass
            del pop
            continue
        pop.surf.fill(pop.clr)
        screen.blit(pop.surf, pop.pos)
        if (pop.Id not in phenotypes['a']) and (pop.Id not in phenotypes['A']):
            for i in pop.gtype: phenotypes[i].append(pop.Id)
    try:
        q = len(phenotypes['a'])/(len(phenotypes['a'])+len(phenotypes['A'])+len(phenotypes['m']))
        p = len(phenotypes['A'])/(len(phenotypes['a'])+len(phenotypes['A'])+len(phenotypes['m']))
        r = len(phenotypes['m'])/(len(phenotypes['a'])+len(phenotypes['A'])+len(phenotypes['m']))
    except ZeroDivisionError:
        p = q = r = 0
    ptxt = font.render(f">>>p = {p}", None, color['g'])
    qtxt = font.render(f">>>q = {q}", None, color['g'])
    qsq = font.render(f">>>q² = {q*q}", None, color['g'])
    psq = font.render(f">>>p² = {p*p}", None, color['g'])
    tpq = font.render(f">>>2pq = {2*p*q}", None, color['g'])
    equilibrium = font.render(f">>>p² + 2pq + q² = {hwe()}", None, color['g'])
    screen.blit(header, (sidebar[0],sidebar[1]+15))
    screen.blit(font.render(f">>>POP COUNT = {len(pops)}",None,color['g']),(sidebar[0],sidebar[1]+45))
    screen.blit(ptxt, (sidebar[0],sidebar[1]+75))
    screen.blit(qtxt, (sidebar[0],sidebar[1]+105))
    screen.blit(qsq, (sidebar[0],sidebar[1]+135))
    screen.blit(psq, (sidebar[0],sidebar[1]+165))
    screen.blit(tpq, (sidebar[0],sidebar[1]+195))
    screen.blit(font.render(f">>>p + q = {p+q}",None,color['g']),(sidebar[0],sidebar[1]+225))
    screen.blit(equilibrium, (sidebar[0],sidebar[1]+255))
    screen.blit(font.render(f">>>p² + q² + r² + 2pq + 2pr + 2qr = {hwe() + r*r + 2*p*r + 2*q*r}",None,color['g']),(sidebar[0],sidebar[1]+285))
    screen.blit(font.render(f">>>NO SELECTION == {noSelection}",None,color['g']),(sidebar[0],sidebar[1]+315))
    screen.blit(font.render(f">>>NO MUTATION == {noMutation}",None,color['g']),(sidebar[0],sidebar[1]+345))
    screen.blit(font.render(f">>>NO MIGRATION == True",None,color['g']),(sidebar[0],sidebar[1]+375))
    screen.blit(font.render(f">>>LARGE POPULATION = {len(pops) >= 5}",None,color['g']),(sidebar[0],sidebar[1]+405))
    screen.blit(font.render(f">>>RANDOM MATING = {randomMate}",None,color['g']),(sidebar[0],sidebar[1]+435))
    try:
        genaverage = sum(genlist)/len(genlist)
    except ZeroDivisionError:
        genaverage = 0
    screen.blit(font.render(f">>>GENERATION AVERAGE: {genaverage}",None,color['g']),(sidebar[0],sidebar[1]+465))
    screen.blit(font.render(f">>>r = {r}", None, color['g']),(sidebar[0],sidebar[1]+495))
    pygame.display.flip()

pygame.quit()
