#!/usr/bin/python3

from time import sleep
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
font = pygame.font.Font("freesansbold.ttf", 32)
pygame.display.set_caption("E-VOLVE Sim")
popCount = popCount_t = 0
SCREEN_W = 1200
SCREEN_H = 900
WIN = 500 # window size
WIN_2X = WIN/2
WIN_2Y = WIN*1.5
color = {"black":(0,0,0), "gray":(170,170,170), "white":(255,255,255), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "pink":(255,0,255), "yellow":(255,255,0), "cyan":(0,255,255),
         "bk":(0,0,0), "gy":(170,170,170), 'w':(255,255,255), 'r':(255,0,0), 'g':(0,255,0), 'b':(0,0,255), 'p':(255,0,255), 'y':(255,255,0), 'c':(0,255,255)}
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
running = True
pops = pygame.sprite.Group()
verboseMode = "-v" in sys.argv
t = 1
maxGen = 0
phenotypes = {'a':[], 'A':[]}
q = p = 0

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
        self.surf = pygame.Surface((25,25))
        self.gender = "-m" if random.randint(0,1) else "-f"
        self.clr = tuple(map(lambda x,y : (x+y)/2, parents[0].clr, parents[1].clr)) if Color is None else Color
        self.horny = False
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
        while running and self.alive:
            sleep(t*100)
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
            if self.gen+1 <= maxGen:
                continue
            else:
                sleep(t*11)
            self.horny = True
            verbose(f">{self.Id}: I am horny!")
            for i in pops:
                if i.gender != self.gender and i.horny and self.gen == i.gen: # my game has to be homophobic, sorry :\ ; at least I'm preventing pedophilia *and* nonconsensual relationships!
                    self.pos = i.pos
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
            elif ("-m" in cin) != ("-f" in cin):
                for i in pops:
                    if i.gender in cin:
                        i.clr = Color
                        verbose(f">{i.Id}: Was painted {Color}")
        except IndexError:
            error("Color must be provided")
    elif cin[0] == "spawn":
        Color = ()
        if "-c" in cin:
            Color = colorize(tuple(cin[cin.index("-c")+1:]))
            if Color == -1:
                return
            cin = cin[:cin.index("-c")]
        j = 1
        try:
            j = int(cin[1])
        except (IndexError, ValueError): #TODO: Add multiple species and move IndexError to its own except
            pass
        for i in range(j):
            pops.add(Pop((random.randint(((SCREEN_W-WIN)/2)-(WIN/4), (SCREEN_W/2)+(WIN/4)), random.randint((SCREEN_H-WIN)/2, (SCREEN_H/2)+(WIN/2))), (0,0,255) if len(Color) != 3 else Color))
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
        maxGen = sab(cin, maxGen, "MAX GENERATION")
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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(color["bk"])
    pygame.draw.rect(screen, color['w'], [((SCREEN_W-WIN)/2)-(WIN/4),(SCREEN_H-WIN)/2,WIN,WIN])
    pygame.draw.rect(screen, color["gy"], [(SCREEN_W/2)+(WIN/2)+(WIN/10),(SCREEN_H-WIN_2Y)/2,WIN_2X,WIN_2Y])
    for pop in pops:
        pop.surf.fill(pop.clr)
        screen.blit(pop.surf, pop.pos)
    pygame.display.flip()

pygame.quit()
