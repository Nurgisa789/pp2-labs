import pygame, random, sys, os, time, psycopg2
from pygame.locals import *

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="0123"
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS user_name (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_name(id),
    score INTEGER,
    level INTEGER
);
""")
conn.commit()

snake_speed = 10
window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
pygame.display.set_caption('Snake Game with DB')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0
level = 1
username = ""
snake_speed_base = 10

walls = {
    2: [(200, 200, 100, 10), (400, 300, 10, 100)],
    3: [(100, 100, 500, 10), (100, 370, 500, 10)],
}

def draw_walls():
    if level in walls:
        for wall in walls[level]:
            pygame.draw.rect(game_window, blue, pygame.Rect(*wall))

def check_wall_collision():
    if level in walls:
        for wall in walls[level]:
            wall_rect = pygame.Rect(*wall)
            if wall_rect.collidepoint(snake_position):
                return True
    return False

def get_user():
    global username, level
    FONT = pygame.font.SysFont("Arial", 24)
    text_box = pygame.Rect(window_x / 2 - 100, window_y / 4 + 50, 200, 40)
    text = ""
    cursor = "|"
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        username = text
        game_window.fill(white)
        pygame.draw.rect(game_window, black, text_box, 2)
        surface = FONT.render(text + cursor, True, black)
        game_window.blit(surface, (text_box.x + 5, text_box.y + 5))
        pygame.display.flip()

    cur.execute("INSERT INTO user_name (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    cur.execute("SELECT id FROM user_name WHERE username = %s", (username,))
    user_id = cur.fetchone()[0]

    cur.execute("SELECT MAX(level) FROM user_score WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    if row and row[0]:
        level = row[0]

get_user()

def save_progress():
    cur.execute("SELECT id FROM user_name WHERE username = %s", (username,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    conn.commit()

def game_over():
    save_progress()
    font = pygame.font.SysFont('times new roman', 50)
    surface = font.render(f'Score: {score}  Level: {level}', True, red)
    rect = surface.get_rect(center=(window_x / 2, window_y / 2))
    game_window.blit(surface, rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

timer = time.time()
speed_increment = 40
next_level_threshold = speed_increment
paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: change_to = 'UP'
            if event.key == pygame.K_DOWN: change_to = 'DOWN'
            if event.key == pygame.K_LEFT: change_to = 'LEFT'
            if event.key == pygame.K_RIGHT: change_to = 'RIGHT'
            if event.key == pygame.K_p:  # Pause shortcut
                paused = not paused
                if paused:
                    save_progress()

    if paused:
        continue

    if change_to == 'UP' and direction != 'DOWN': direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP': direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT': direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT': direction = 'RIGHT'

    if direction == 'UP': snake_position[1] -= 10
    if direction == 'DOWN': snake_position[1] += 10
    if direction == 'LEFT': snake_position[0] -= 10
    if direction == 'RIGHT': snake_position[0] += 10

    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += random.choice([10, 20, 30])
        fruit_spawn = False
    else:
        if time.time() - timer > 5:
            timer = time.time()
            fruit_spawn = False
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, window_x // 10) * 10, random.randrange(1, window_y // 10) * 10]
        fruit_spawn = True

    if score >= next_level_threshold:
        snake_speed += 5
        level += 1
        next_level_threshold += speed_increment

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    draw_walls()

    if (snake_position[0] < 0 or snake_position[0] > window_x - 10 or
        snake_position[1] < 0 or snake_position[1] > window_y - 10 or
        check_wall_collision()):
        game_over()

    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    font = pygame.font.SysFont('times new roman', 20)
    game_window.blit(font.render(f'Score: {score}', True, white), (10, 0))
    game_window.blit(font.render(f'Level: {level}', True, white), (600, 0))

    pygame.display.update()
    fps.tick(snake_speed)