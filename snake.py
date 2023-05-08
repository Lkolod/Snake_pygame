
import pygame
import os
import random
from pygame.math import Vector2
# trzeba dodac last state i potem warunki ze dopóki self.y czy self.x nie bedzie równy StepIndex go ma sie poruszać tak samo

pygame.font.init()
pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()

SPEED = 15
WIDTH, HEIGHT = 900, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (122,122,122)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption('snake')


class apple():
    
    def __init__(self, x, y):
        self.apple_width = 30
        self.apple_height = 30
        self.x = x
        self.y = y
        self.apple_pos = Vector2(self.x,self.y)

    def draw_apple(self):
        apple_rect = pygame.Rect(self.apple_pos.x * 30 ,self.apple_pos.y * 30,self.apple_width,self.apple_height)
        pygame.draw.rect(screen,WHITE,apple_rect)

    def apple_respawn(self):
        self.apple_width = 30
        self.apple_height = 30
        self.x = random.randint(0,30-1)
        self.y = random.randint(0,20-1)
        self.apple_pos = Vector2(self.x,self.y)
        
class snake():
    
    def __init__(self, x, y):
        
        self.snake_width = 30
        self.snake_height = 30
        self.x = [x,x]
        self.y = [y,y]
        self.move = 30
        self.last_state = 2
        self.current_state = 2
        self.length  = 2
        
    def snake_reset(self):
        
        self.x = [WIDTH/2,WIDTH/2]
        self.y = [HEIGHT/4,HEIGHT/4]
        self.move = 30
        self.last_state = 2
        self.current_state = 2
        self.length  = 2

    def check_keys(self, userImput):
        if userImput[pygame.K_RIGHT]:  # prawo
            self.current_state = 0
            
        if userImput[pygame.K_LEFT]:  # lewo
            self.current_state = 1

        if userImput[pygame.K_DOWN]:  # dół
            self.current_state = 2

        if userImput[pygame.K_UP]:  # góra         
            self.current_state = 3

    def body_update(self):
        for i in range(self.length-1,0,-1):
            self.x[i]  = self.x[i-1] 
            self.y[i]  = self.y[i-1] 

    def go_right(self):
        self.x[0] += self.move

    def go_left(self):
        self.x[0] -= self.move

    def go_down(self):
        self.y[0] += self.move
    
    def go_up(self):
        self.y[0] -= self.move
    
    def head_movement(self):
        self.body_update()
        if self.current_state != self.last_state and self.y[0] % 30 == 0 and self.x[0] % 30 == 0:
            
            if self.current_state == 0 and self.last_state != 1:
                self.go_right()
                self.last_state = self.current_state 
                
            elif self.current_state == 1 and self.last_state != 0:
                self.go_left()
                self.last_state = self.current_state 
                
            elif self.current_state == 2 and self.last_state != 3:
                self.go_down()
                self.last_state = self.current_state 

            elif self.current_state == 3 and self.last_state != 2:
                self.go_up()
                self.last_state = self.current_state 
        
            else:
                if self.last_state == 0:
                    self.go_right()

                elif self.last_state == 1:
                    self.go_left()

                elif self.last_state == 2:
                    self.go_down()

                elif self.last_state == 3:
                    self.go_up()                   
        else:
            
            if self.last_state == 0:
                self.go_right()

            elif self.last_state == 1:
                 self.go_left()

            elif self.last_state == 2:
                self.go_down()

            elif self.last_state == 3:
                self.go_up()
 

    def draw_snake_body(self):
        for i in range(self.length -1):
            pygame.draw.rect(screen, WHITE, pygame.Rect(self.x[i], self.y[i], self.snake_width, self.snake_width))
        
   
    def increase_length(self):
        self.length += 1
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        
    def snake_collision(self):
        
        for tail_x, tail_y in zip(self.x[1:], self.y[1:]):
            if self.x[0] == tail_x and self.y[0] == tail_y:
                return True
        return False
        
        
    
def draw_game(score):
    SCORE = str(score)
    screen.fill((GREY))
    pygame.time.delay(20)
    
    font = pygame.font.SysFont(None, 40)
    text = font.render('player score: ' + SCORE, True, BLACK)
    
    text_rect = text.get_rect(topleft=(10,10))
    screen.blit(text, text_rect)
    
def pause():
    paused =  True
    font = pygame.font.SysFont(None, 64)
    font2 = pygame.font.SysFont(None, 30)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        text_to_quit = ('PRESS Q TO QUIT')
        
        screen.fill(WHITE)          
        
        text = font.render("PAUSED", True, BLACK)
        text2 = font2.render("PRESS Q TO LEAVE", True, BLACK)
        
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        text_rect2 = text2.get_rect(midbottom=(WIDTH//2, HEIGHT//2 + 80))
        
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        pygame.display.update()
        clock.tick(30)
  

        
def main():
    apple_x = random.randint(0,30-1)
    apple_y = random.randint(0,20-1)
    snake_x = WIDTH/2
    snake_y = HEIGHT/4
    APPLE = apple(apple_x,apple_y)   
    SNAKE = snake(snake_x,snake_y)
    player_score = 0
    
    
    run = True
    while run:
        
        userImput = pygame.key.get_pressed()
        clock.tick(SPEED)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()     
                 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                         
        draw_game(player_score)
        SNAKE.check_keys(userImput)
        SNAKE.head_movement()
        APPLE.draw_apple() 
        SNAKE.draw_snake_body()
        
        # condition for eatting applae
        if int(SNAKE.x[0]/30) == APPLE.x and int(SNAKE.y[0]/30) == APPLE.y:           
            SNAKE.increase_length()
            APPLE.apple_respawn()
            player_score += 1
        
        # condition for colision with boarder 
        if SNAKE.x[0] < 0 or SNAKE.x[0] >= WIDTH or SNAKE.y[0] >= HEIGHT or SNAKE.y[0] <0:
            SNAKE.snake_reset()
            APPLE.apple_respawn()
            player_score = 0

        if SNAKE.snake_collision():
            SNAKE.snake_reset()
            APPLE.apple_respawn()
            player_score = 0 

        

            
        pygame.display.update()

if __name__ == '__main__':
    main()
