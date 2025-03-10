import pygame
import time
import math


pygame.init()


size = (700, 700)
pygame.display.set_caption("Mickey Mouse Clock")


mickey_image = pygame.image.load("Lab07/images/mickeyclock.jpeg")


center_x = size[0] // 2
center_y = size[1] // 2
radius = min(center_x, center_y) - 50


screen = pygame.display.set_mode(size)


font = pygame.font.SysFont(None, 48)
color = (255, 255, 255)


while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

   
    current_time = time.localtime()

    
    seconds_angle = math.radians(current_time.tm_sec * 6 - 90)
    minutes_angle = math.radians(current_time.tm_min * 6 - 90)

    
    seconds_hand = pygame.transform.rotate(mickey_image, math.degrees(seconds_angle))
    minutes_hand = pygame.transform.rotate(mickey_image, math.degrees(minutes_angle))

    
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, color, (center_x, center_y), radius, 5)

    
    screen.blit(seconds_hand, (center_x - seconds_hand.get_width() // 2, center_y - seconds_hand.get_height() // 2))
    screen.blit(minutes_hand, (center_x - minutes_hand.get_width() // 2, center_y - minutes_hand.get_height() // 2))

    
    clock_text = font.render(time.strftime("%I:%M:%S %p"), True, (0,0,0))
    screen.blit(clock_text, (size[0] // 2 - clock_text.get_width() // 2, size[1] // 2 + radius + 10))

    
    pygame.display.flip()

   
    time.sleep(1)