import pygame
import pygame.mixer
import pygame.time
import pygame.event
import os

pygame.mixer.init()
pygame.init()
pygame.font.init()
pygame.font.get_init()

size = (500, 400)
pygame.display.set_caption("MP3 Player")
screen = pygame.display.set_mode(size)


screen.fill((255,255,255))
f1 = pygame.font.SysFont('serif', 30)
text1 = f1.render('Остановить -- S', True,(0, 180, 0))
 
f2 = pygame.font.SysFont('serif', 30)
text2 = f2.render("Возобновить -- SPACE", False,(0, 180, 0))

f3 = pygame.font.SysFont('serif', 30)
text3 = f3.render("Следующее -- RIGHT", False,(0, 180, 0))

f4 = pygame.font.SysFont('serif', 30)
text4 = f4.render("Предыдущее -- LEFT", False,(0, 180, 0))
 
screen.blit(text1, (10, 50))
screen.blit(text2, (10, 100))
screen.blit(text3, (10, 150))
screen.blit(text4, (10, 200))
pygame.display.update()






music_directory = "Lab07/music/"
music_files = []
for filename in os.listdir(music_directory):
    if filename.endswith(".mp3"):
        music_files.append(os.path.join(music_directory, filename))
music_index = 0


key_bindings = {
    pygame.K_SPACE: "play",
    pygame.K_s: "stop",
    pygame.K_RIGHT: "next",
    pygame.K_LEFT: "previous",
}


clock = pygame.time.Clock()


pygame.mixer.music.load(music_files[music_index])
pygame.mixer.music.play()

while True:

 

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key in key_bindings:
                command = key_bindings[event.key]

                if command == "play":
                    pygame.mixer.music.unpause()

                elif command == "stop":
                    pygame.mixer.music.pause()

                elif command == "next":
                    music_index = (music_index + 1) % len(music_files)
                    pygame.mixer.music.load(music_files[music_index])
                    pygame.mixer.music.play()

                elif command == "previous":
                    music_index = (music_index - 1) % len(music_files)
                    pygame.mixer.music.load(music_files[music_index])
                    pygame.mixer.music.play()

    
    clock.tick(60)  