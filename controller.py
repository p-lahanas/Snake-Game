import pygame

class Input:

    def __init__(self, snake):
        self.snake = snake  

    def key_press(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.snake.set_direction((-1,0))
        elif keys[pygame.K_RIGHT]:
            self.snake.set_direction((1,0))
        elif keys[pygame.K_UP]:
            self.snake.set_direction((0,-1))
        elif keys[pygame.K_DOWN]:
            self.snake.set_direction((0, 1))

    def loading_menu(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if key:
                return True
        return False
