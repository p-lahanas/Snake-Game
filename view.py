import pygame
from model import Snake
from controller import Input

NUM_GRID = 20
SPACE = 100

WIN_LENGTH = 700

WHITE = (255,255,255)
STATIC_BOX = (120,120,120)
HIGHLIGHTED_BOX = (184,184,184)
RED = (255,0,0)
BLACK = (0,0,0)
GREEN = (143,188,143)
HEAD_COLOUR = (137,104,205)
SEGMENT_COLOUR = (255,52,179)


def save_score(name, score):
    with open('High_Scores.txt', 'a') as scores:
        scores.write(str(name) + ' : ' + str(score) +'\n')
 
def highest(scores, names):
    x = scores[0]
    name = names[0]
    index = 0
    for i, score in enumerate(scores):
        if int(score) > int(x):
            x = score
            name = names[i]
            index = i
        
    return x, name, index 

def high_scores():
    names = []
    scoress = []
    high_scores = []
    with open("High_Scores.txt", 'r') as scores:
        lines = scores.readlines()

        for line in lines:
            x = line.split(" : ")
            name = x[0]
            score = x[1].strip()
            names.append(name)
            scoress.append(score)
        i = 0
        x = len(names)
        while i < x:
            score, name, index = highest(scoress, names)
            del scoress[index]
            del names[index]
            
            combined = str(name) + ' : ' + str(score)
            high_scores.append(combined)
            i += 1
            
            
    return high_scores



class Window:

    
    def __init__(self):
        pygame.display.init()   
        pygame.font.init()
        self.grid_width = (WIN_LENGTH - (2*SPACE)) / NUM_GRID
        self.score_font = pygame.font.SysFont("comicsans", 50)
        self.title_font = pygame.font.SysFont("comicsans", 70)
        self.button_font = pygame.font.SysFont("Arial", 30)
        self.window = pygame.display.set_mode((WIN_LENGTH, WIN_LENGTH))
        pygame.display.set_caption("Snake Game")
        
        self.writing = False
        self.snake = Snake(NUM_GRID)
        self.input = Input(self.snake)
        self.name = ""
        self.submit = False

    def loading_screen(self):
        text = self.score_font.render("Press any key to begin...", 1, WHITE)
        self.window.blit(text, (WIN_LENGTH-text.get_width()-150,WIN_LENGTH//2))
        return self.input.loading_menu()



    def draw_grid(self):
        i = 0
        j = 0
        x = SPACE
        y = SPACE
        grid_length = self.grid_width *NUM_GRID 
        
        while j<=NUM_GRID:
                pygame.draw.line(self.window, WHITE, (x,y), (x+grid_length,y))
                y+= self.grid_width
                j+=1
        y = SPACE
        while i <= NUM_GRID:
            
            pygame.draw.line(self.window, WHITE, (x,y), (x,y+grid_length))
            x += self.grid_width
            i+=1

    def coor_to_rect(self, x, y):
        x += (SPACE+1 + ((self.grid_width-1)*x))
        y += (SPACE+1 + ((self.grid_width-1)*y))

        return x,y

    def draw_snake(self, snake):
        x,y = self.coor_to_rect(snake.x,snake.y)
        fruitx, fruity = self.coor_to_rect(snake.fruit.x, snake.fruit.y)
        for segment in snake.tail:
            segx, segy = self.coor_to_rect(segment[0],segment[1])
            pygame.draw.rect(self.window, SEGMENT_COLOUR, (segx, segy,self.grid_width-1, self.grid_width-1))
        if x < WIN_LENGTH-SPACE and y < WIN_LENGTH - SPACE and x > 0+SPACE and y>0+SPACE:
            pygame.draw.rect(self.window, HEAD_COLOUR, (x,y,self.grid_width-1, self.grid_width-1))
        pygame.draw.rect(self.window, GREEN, (fruitx,fruity,self.grid_width-1, self.grid_width-1))

    def update(self):
        text = self.score_font.render("Score: " + str(self.snake.score), 1, WHITE)
        

        self.window.fill(BLACK)
        self.draw_grid()
        self.input.key_press()
        self.draw_snake(self.snake)
        self.window.blit(text, (0, 10))
        return self.snake.update()
        

    def high_score_menu(self):
        self.window.fill(BLACK)
        scores_text = self.title_font.render("High Scores:", 1, WHITE)
        self.window.blit(scores_text,(WIN_LENGTH/2 - scores_text.get_width()/2,10) )
        high_scores_str = high_scores()
        high_scores_str = high_scores_str[0:5]
        i = 80
        for score in high_scores_str:
            score_text = self.score_font.render(score, 1, WHITE)
            self.window.blit(score_text, (WIN_LENGTH/2 - score_text.get_width()/2,i))
            i += 50
        
        
        
        x,y = pygame.mouse.get_pos()
        
        pygame.draw.rect(self.window, WHITE, (WIN_LENGTH/2-225, WIN_LENGTH/2+200, 300,50))
        pygame.draw.rect(self.window, STATIC_BOX, (WIN_LENGTH/4-45, WIN_LENGTH/2+100, 180,50))
        pygame.draw.rect(self.window, STATIC_BOX, (WIN_LENGTH/4 + 200, WIN_LENGTH/2+100, 180,50))
        pygame.draw.rect(self.window, STATIC_BOX, (WIN_LENGTH/2+75,WIN_LENGTH/2+200, 150,50))
        

        if x > WIN_LENGTH/2-225 and x < WIN_LENGTH/2+75 and y>WIN_LENGTH/2+200 and y < WIN_LENGTH/2+250:
            pygame.draw.rect(self.window, HIGHLIGHTED_BOX, (WIN_LENGTH/2-225, WIN_LENGTH/2+200, 300,50))
            if pygame.mouse.get_pressed()[0]:
                self.writing = True

        elif x > WIN_LENGTH/2+75 and x < WIN_LENGTH/2+375 and y>WIN_LENGTH/2+200 and y < WIN_LENGTH/2+250:
            pygame.draw.rect(self.window, HIGHLIGHTED_BOX, (WIN_LENGTH/2+75,WIN_LENGTH/2+200, 150,50))
            if pygame.mouse.get_pressed()[0] and not self.submit:
                save_score(self.name, self.snake.score)
                self.name = ""
                self.submit = True

        elif x > WIN_LENGTH/4-45 and x < WIN_LENGTH/4+135 and y>WIN_LENGTH/2+100 and y < WIN_LENGTH/2+150:
            pygame.draw.rect(self.window, HIGHLIGHTED_BOX, (WIN_LENGTH/4-45, WIN_LENGTH/2+100, 180,50))  
            if pygame.mouse.get_pressed()[0]:
                self.snake.x = NUM_GRID/2
                self.snake.y = NUM_GRID/2
                self.snake.direction = (1,0)
                return True, False

        elif x > WIN_LENGTH/4+200 and x < WIN_LENGTH/4+380 and y>WIN_LENGTH/2+100 and y < WIN_LENGTH/2+150:
            pygame.draw.rect(self.window, HIGHLIGHTED_BOX, (WIN_LENGTH/4+200, WIN_LENGTH/2+100, 180,50)) 
            if pygame.mouse.get_pressed()[0]:
                return False, True

        if self.writing:
            pygame.draw.rect(self.window, HIGHLIGHTED_BOX, (WIN_LENGTH/2-225, WIN_LENGTH/2+200, 300,50))
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        if len(self.name) < 12:
                            self.name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:len(self.name)-1]
                    elif event.key == pygame.K_RETURN:
                        save_score(self.name, self.snake.score)
                        

            name = self.score_font.render(self.name, 1, WHITE)
            self.window.blit(name, (WIN_LENGTH/2-200, WIN_LENGTH/2+210, 300,50))

        text1 = self.score_font.render("Play Again", 1, WHITE)
        self.window.blit(text1, (WIN_LENGTH/4-43,WIN_LENGTH/2+112))
        text2 = self.score_font.render("Quit", 1, WHITE)
        self.window.blit(text2, (WIN_LENGTH/4+250,WIN_LENGTH/2+112))
        text3 = self.score_font.render("Submit", 1, WHITE)
        self.window.blit(text3, (WIN_LENGTH/2+78, WIN_LENGTH/2+210))
       
        return True, True
        


