# Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# snake segment
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(0,255,0)):
        # pos is grid pos, not pixels
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
    
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        # row
        i = self.pos[0]
        # column
        j = self.pos[1]

        # the +1s and -2s are to reduce square size enough to see grid lines
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

# snake body, comprised of cube objects
class snake(object):
    # list of cubes
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        # make head, add it to body
        self.head = cube(pos)
        self.body.append(self.head)
        # keep track of direction of movement
        self.dirnx = 0
        self.dirny = 1


    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # all key values and whether they were pressed or not
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        # iterate through body segments, match what head did here
        # for index, cube in body
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                # head moved here
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # once last cube hits turn, remove it from the list of turns
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # head didn't move here
                # check for edges, jump to other side of screen or keep going
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows -1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # check tail direction, add new cube in correct pos
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            # if head of snake, draw eyes
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    
    x = 0
    y = 0
    for i in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        # draw two lines for each iteration of the loop
        # surface, color, starting point, ending point
        # top left corner == (0, 0)?
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def redrawWindow(surface):
    global rows, width, s, snack
    # window fill color
    surface.fill((0, 0, 0))
    # draw snake
    s.draw(surface)
    #draw snack
    snack.draw(surface)
    #draw grid
    drawGrid(width, rows, surface)
    # update display
    pygame.display.update()

def generateSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        # make sure there's somewhere to put the snack
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

# def message_box(subject, content):
#     root = tk.Tk()
#     root.attributes("-topmost", True)
#     root.withdraw()
#     messagebox.showinfo(subject, content)
#     try:
#         root.destroy()
#     except:
#         pass

def main():
    global width, rows, s, snack
    # make window
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))

    # create snake object
    s = snake((0, 255, 0), (10, 10))

    # create snack
    snack = cube(generateSnack(rows, s), color=(255, 0, 0))

    # ##########################
    # GAME LOOP
    # ##########################
    flag = True
    # part of pygame, manages fps
    clock = pygame.time.Clock()

    while flag:
        # sets time delay so program doesn't run too fast
        pygame.time.delay(50)
        # snake will not be able to move more than 10 frames per second
        clock.tick(10)
        s.move()
        # see if head of snake has hit snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(generateSnack(rows, s), color=(255, 0, 0)) 

        # collision checking
        # loop through snake body cubes, see if head matches any
        for i in range(len(s.body)):
            if s.body[i].pos in list(map(lambda z: z.pos, s.body[i + 1:])):
                # message_box("You Lost", "Restarting...")
                s.reset((10, 10))
                break


        redrawWindow(win)

main()