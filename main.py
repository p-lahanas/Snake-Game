import pygame
from view import Window



window = Window()


game_over = False
clock = pygame.time.Clock()
start = False
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            quit()

    if start:
        if game_over:
            state = window.high_score_menu()
            run, game_over = state
            
            pygame.display.update()
            clock.tick(1000)
        else:
            game_over = window.update()
            pygame.display.update()
            clock.tick(120)

    else:
        start = window.loading_screen()
        pygame.display.update()

    

