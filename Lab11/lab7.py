import pygame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("color shape")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

button_font = pygame.font.Font(None, 30)
buttons = {
    "Triangle": pygame.Rect(20, 20, 100, 40),
    "Circle": pygame.Rect(140, 20, 100, 40),
    "Square": pygame.Rect(260, 20, 100, 40),
    "Red": pygame.Rect(380, 20, 60, 40),
    "Green": pygame.Rect(450, 20, 60, 40),
    "Blue": pygame.Rect(520, 20, 60, 40)
}

selected_shape = None
selected_color = RED

running = True
while running:
    screen.fill(WHITE)
    
    for text, rect in buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), rect)
        label = button_font.render(text, True, (0, 0, 0))
        screen.blit(label, (rect.x + 10, rect.y + 10))
    
    if selected_shape == "Triangle":
        pygame.draw.polygon(screen, selected_color, [(300, 100), (250, 200), (350, 200)])
    elif selected_shape == "Circle":
        pygame.draw.circle(screen, selected_color, (300, 150), 50)
    elif selected_shape == "Square":
        pygame.draw.rect(screen, selected_color, (250, 100, 100, 100))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for text, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    if text in ["Triangle", "Circle", "Square"]:
                        selected_shape = text
                    elif text == "Red":
                        selected_color = RED
                    elif text == "Green":
                        selected_color = GREEN
                    elif text == "Blue":
                        selected_color = BLUE
    
    pygame.display.flip()

pygame.quit()
