
import pygame
import random
from pygame.locals import * 

pygame.init()
screen = pygame.display.set_mode((900, 700))
screen.fill((255, 255, 255))


pygame.display.set_caption('Paint(2.0)')

draw_on = False
last_pos = (0, 0)


radius = 5


WHITE=(255,255,255)
RED=(255,0,0)
YELLOW=(255,255,0)
GREEN=(102,204,0)
BLUE=(51,51,255)
BLACK=(0,0,0)
PINK=(255,0,255)
color = BLACK

pygame.draw.rect(screen,RED,(0,50,20,20))
pygame.draw.rect(screen,YELLOW,(0,70,20,20))
pygame.draw.rect(screen,GREEN,(20,50,20,20))
pygame.draw.rect(screen,BLUE,(20,70,20,20))
pygame.draw.rect(screen,BLACK,(0,90,20,20))
pygame.draw.rect(screen,PINK,(20,90,20,20))
erasor = pygame.transform.scale(pygame.image.load("erasor.jpg"), (40, 40))
screen.blit(erasor, [0,110])
triangle = pygame.transform.scale(pygame.image.load("Triangle.jpg"), (40, 40))
screen.blit(triangle, [0,150])
square = pygame.transform.scale(pygame.image.load("Square1.jpg"), (40, 40))
screen.blit(square, [0,190])
rectangle = pygame.transform.scale(pygame.image.load("Rectangle1.jpg"), (40, 40))
screen.blit(rectangle, [0,230])
circle = pygame.transform.scale(pygame.image.load("Circle.jpg"), (40, 40))
screen.blit(circle, [0,270])


def roundline(canvas, color, start, end, radius=1) :
    Xaxis = end[0] - start[0]
    Yaxis = end[1] - start[1]
    dist = max(abs(Xaxis), abs(Yaxis))
    for i in range(dist) :
        x = int(start[0] + float(i) / dist * Xaxis)
        y = int(start[1] + float(i) / dist * Yaxis)
        pygame.draw.circle(canvas, color, (x, y), radius)


try :
    
    while True :
        e = pygame.event.wait()

        if e.type == pygame.QUIT :
            raise StopIteration

        if e.type == pygame.MOUSEBUTTONDOWN :
            spot = pygame.mouse.get_pos()
            # Selecting Color Code
            if spot[0] < 20 and spot[1] < 70 and spot[1] > 50:
                color= RED
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 70 and spot[1] > 50:
                color= GREEN
            elif spot[0] < 20 and spot[1] < 90 and spot[1] > 70:
                color= YELLOW
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 90 and spot[1] > 70:
                color= BLUE
            elif spot[0] < 20 and spot[1] < 110 and spot[1] > 90:
                color= BLACK
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 110 and spot[1] > 90:
                color= PINK
            elif spot[0] < 40 and spot[1] < 150 and spot[1] > 110:
                color = WHITE
            
                
            if spot[0] > 60:
                pygame.draw.circle(screen, color, e.pos, radius)
            draw_on = True

        if e.type == pygame.MOUSEBUTTONUP :
            draw_on = False

        if e.type == pygame.MOUSEMOTION:
            spot = pygame.mouse.get_pos()
            if draw_on and spot[0] > 60:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos
        if e.type == pygame.KEYDOWN:
            spot = pygame.mouse.get_pos()
            if e.key == pygame.K_s: 
                pygame.draw.rect(screen, color, (spot[0], spot[1], 50, 50), 2)
            elif e.key == pygame.K_r: 
                pygame.draw.polygon(screen, color, [(spot[0], spot[1]), (spot[0] + 50, spot[1] + 50), (spot[0], spot[1] + 50)], 2)
            elif e.key == pygame.K_e: 
                pygame.draw.polygon(screen, color, [(spot[0], spot[1]), (spot[0] + 50, spot[1]), (spot[0] + 25, spot[1] - 43)], 2)
            elif e.key == pygame.K_h: 
                pygame.draw.polygon(screen, color, [(spot[0], spot[1]), (spot[0] + 25, spot[1] + 50), (spot[0] + 50, spot[1]), (spot[0] + 25, spot[1] - 50)], 2)
        pygame.display.flip()

except StopIteration:
    pass




pygame.quit()
