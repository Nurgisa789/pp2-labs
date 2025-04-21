import pygame, random, sys ,os,time, psycopg2
from pygame.locals import *

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="0123"
)

cur = conn.cursor()

snake_speed = 10

window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((window_x, window_y))

fps = pygame.time.Clock()
snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
level = 1
x = 0
name = ""

def welcome():
    user_name = "Write user name:"
    global name
    FONT_SIZE = 24
    FONT = pygame.font.SysFont("Arial", FONT_SIZE)
    text_box = pygame.Rect(window_x / 2 - 100, window_y / 4 + 50, 200, 40)
    text = ""
    cursor = "|"
    ch = True
    while ch:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    ch = False
                else:
                    text += event.unicode

        name = text
        game_window.fill(white)
        pygame.draw.rect(game_window, black, text_box, 2)

        text_surface = FONT.render(text + cursor, True, black)
        game_window.blit(text_surface, (text_box.x + 5, text_box.y + 5))

        pygame.display.flip()

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)

    score_surface = score_font.render('Score : ' + str(score), True, color)

    score_rect = score_surface.get_rect()

    game_window.blit(score_surface, score_rect)


def show_level(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)

    score_surface = score_font.render('Level : ' + str(level), True, color)

    score_rect = score_surface.get_rect(topright=(650, 0))

    game_window.blit(score_surface, score_rect)

def game_over():
    cur.execute(
        "INSERT INTO user_name (username) VALUES (%s)",
        (name,)
    )
    cur.execute("SELECT id FROM user_name WHERE username = %s", (name,))
    user_id = cur.fetchone()[0]
    cur.execute(
        'INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)',
        (user_id, score, level)
    )
    conn.commit()
    cur.close()
    conn.close()
    my_font = pygame.font.SysFont('times new roman', 50)

    game_over_surface = my_font.render(
        'Score is : ' + str(score) + '  Level :' + str(level), True, red)

    game_over_rect = game_over_surface.get_rect()

    game_over_rect.midtop = (window_x / 2, window_y / 4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(2)

    pygame.quit()

    quit()

welcome()

tm = time.time()

while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += random.randrange(10, 31, 10)
        fruit_spawn = False
    else:
        if time.time() - tm > 5:
            tm = time.time()
            fruit_spawn = False
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True
    game_window.fill(black)

    if score >= x + 40:
        snake_speed += 5
        level += 1
        x += 40

    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'times new roman', 20)
    show_level(1, white, 'times new roman', 20)

    pygame.display.update()

    fps.tick(snake_speed)