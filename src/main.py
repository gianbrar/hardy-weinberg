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
popCount = popCount_t = 0
SCREEN_W = 1000
SCREEN_H = 800
WIN = 500 # window size
color = {"black":(0,0,0), "white":(255,255,255), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "pink":(255,0,255), "yellow":(255,255,0), "cyan":(0,255,255),
         "bk":(0,0,0), 'w':(255,255,255), 'r':(255,0,0), 'g':(0,255,0), 'b':(0,0,255), 'p':(255,0,255), 'y':(255,255,0), 'c':(0,255,255)}
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
running = True
pops = pygame.sprite.Group()
verboseMode = "-v" in sys.argv
t = 1

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
    def __init__(self, Color, position):
        global pops
        super(Pop, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.clr = Color
        self.gender = "-m" if random.randint(0,1) else "-f"
        self.surf.fill(Color)
        self.alive = True
        self.Id = 10000000
        while findPop(self.Id):
            self.Id = random.randint(10000000, 99999999)
        self.pos = position
        verbose(f">{self.Id}: Position is now {self.pos}")
        pops.add(self)
        verbose(f">{self.Id}: Added self to pops list")
        _thread.start_new_thread(self.updateSprite, ())
        _thread.start_new_thread(self.move, ())
    def updateSprite(self):
        global running
        while running and self.alive:
            self.surf.fill(self.clr)
    def move(self):
        global t
        global running
        movement = lambda Pos : Pos+(random.choice([-1,1])*random.choice([0,5,10,25,50]))
        while running and self.alive:
            sleep(t)
            self.cachePos = self.pos
            self.pos = (0,0)
            while not ((self.pos[0]+25 > (SCREEN_W-WIN)/2 and self.pos[0]+25 < (SCREEN_W/2)+(WIN/2)) and (self.pos[1]+25 > (SCREEN_H-WIN)/2 and self.pos[1]+25 < (SCREEN_H/2)+(WIN/2))):
                self.pos = (movement(self.cachePos[0]), movement(self.cachePos[1]))
            verbose(f">{self.Id}: Position is now {self.pos}")

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

def console():
    global running
    print(">E-VOLVE console activated (cOMManDs ArE cASE SeNSiTIVe)")
    while running:
        cin = input(">>").split()
        if cin[0] == "kill":
            if "-r" in cin:
                cin.remove("-r")
                try:
                    if int(cin[1]) > len(pops):
                            error("Selected no. of pops cannot be greater than actual no. of pops")
                            continue
                    for i in range(int(cin[1])):
                        pops.remove(list(pops)[random.randint(0,len(pops)-1)])
                except ValueError:
                    error("No. of pops must be type `int`" if len(cin) > 1 else ">No. of pops not provided")
                continue
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
            Color = ()
            try:
                if ("-m" in cin) != ("-f" in cin):
                    Color = colorize(tuple([i for i in cin if not i.startswith("-")]))
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
                    continue
                cin = cin[:cin.index("-c")]
            j = 1
            try:
               j = int(cin[1])
            except (IndexError, ValueError): #TODO: Add multiple species and move IndexError to its own except
                pass
            for i in range(j):
                pops.add(Pop((0, 0, 255) if len(Color) != 3 else Color, (random.randint((SCREEN_W-WIN)/2, (SCREEN_W/2)+(WIN/2)), random.randint((SCREEN_H-WIN)/2, (SCREEN_H/2)+(WIN/2)))))
        elif cin[0] == "exit":
            running = False
        elif cin[0] == "ls":
            k = 0
            for i in pops:
                k += 1
                print(f">ID={i.Id} COLOR={list(color.keys())[list(color.values()).index(i.clr)]}{',' if k != len(pops) else ''} GENDER={i.gender[1]}")
            print(f">{len(pops)} total pops.")
        elif cin[0] == "tick":
            global t
            if len(cin) < 3:
                error("3 args are required")
            else:
                try:
                    if cin[1] == "set":
                        t = int(cin[2])
                    elif cin[1] == "add":
                        t += int(cin[2])
                    elif cin[1] == "sub":
                        t -= int(cin[2])
                    else:
                        error("Unknown option (valid options are set, add, sub)")
                except ValueError:
                    error("Tick speed must be type `int`")
        elif cin[0] == "coconut" and cin[1] == "mall":
            print("You got coconut malled! Share this with your friends to totally coconut mall them!")
            running = False
        else:
            error("Unknown command")

_thread.start_new_thread(console, ())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(color["bk"])
    pygame.draw.rect(screen, color['w'], [(SCREEN_W-WIN)/2,(SCREEN_H-WIN)/2,WIN,WIN])
    for pop in pops:
        screen.blit(pop.surf, pop.pos)
    pygame.display.flip()

pygame.quit()
