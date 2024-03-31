import pygame
import math
import random
import time
pygame.init()

WHITE = (255,255,255)
RED = (255,0,0)
PLAYER_1 = (255,140,0) # orange - player on the left
PLAYER_2 = (255,255,255) # white - player on the right
BACKGROUND = (51,51,51) # grey-ish colour

# Setting up the game window
WIDTH, HEIGHT = 1200, 800 # of window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
FONT = pygame.font.SysFont("comicsans", 16)
TIMESTEP = 0.2 # controls the speed of the ball
MAX_SCORE = 10

# Scores
scores = {
    "Player 1": 0,
    "Player 2": 0
}

def main():
    # object creation
    ball = Ball()
    bat_left = Bat("left")
    bat_right = Bat("right")
    bats = [bat_left,bat_right]

    RUN = True
    clock = pygame.time.Clock()

    while RUN:
        clock.tick(120)
        WIN.fill(BACKGROUND)

        # event handling
        for event in pygame.event.get():
            # quit loop condition
            if event.type == pygame.QUIT:
                RUN = False
                 
            # listening for key presses 
            elif event.type == pygame.KEYDOWN:
                Bat.set_flag(bat_left,bat_right,event)                     

            # listening for key releases
            elif event.type == pygame.KEYUP:
                Bat.remove_flag(bat_left,bat_right,event)

        ball.draw(WIN)
        for bat in bats:
            bat.draw(WIN)
            bat.move()
            ball.move(bat)

        # If ball leaves window on player 1's side
        if ball.x < -20:
            scores["Player 1"] -= 1
            ball.restart()
        # If ball leaves window on player 2's side
        if ball.x > WIDTH + 20:
            scores["Player 2"] -= 1
            ball.restart()

        draw_score()

        # if either player's score reaches the max_score the game shuts down
       # for player in scores:
        #    if scores[player] == MAX_SCORE:
         #       RUN = False

        pygame.display.update() 
    pygame.quit()

def draw_score():
    y_offset = 10
    for player, score in scores.items():
        player_score_text = FONT.render(player + " Score: " + str(score), True, WHITE)
        WIN.blit(player_score_text, (10, y_offset))
        y_offset += 30


class Ball:
    def __init__(self):
        self.radius = 15
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.color = RED
        self.vel = 10 # velocity in pixels
        self.theta = 2 * math.pi * random.random() # angle in radians relative to the x-axis
        self.vel_x = self.vel * math.cos(self.theta)
        self.vel_y = self.vel * math.sin(self.theta)
  
    def draw(self,WIN):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)

    # moves the ball
    def move(self, bat):
        # sets initial motion
        self.x = self.x + self.vel_x*TIMESTEP
        self.y = self.y + self.vel_y*TIMESTEP

        # bounces the ball against top and bottom walls
        if self.y <= 0 or self.y >= HEIGHT:
            self.vel_y = -self.vel_y

        # bounces ball against bats
        if bat.type == "left":
            if (self.x <= bat.width) and (self.y >= bat.y and self.y <= (bat.y + bat.height)):
                self.vel_x = -self.vel_x
                # update player 1 score
                scores["Player 1"] += 1
                # add additional y-vel to ball
                if bat.up and self.vel_y > 0:
                    self.vel_y = -self.vel_y
                if bat.down and self.vel_y < 0:
                    self.vel_y = -self.vel_y  
        elif bat.type == "right":
            if (self.x >= WIDTH-bat.width) and (self.y >= bat.y and self.y <= (bat.y + bat.height)):            
                self.vel_x = -self.vel_x
                # update player 2 score
                scores["Player 2"] += 1
                # add additional y-vel to ball
                if bat.up and self.vel_y > 0:
                    self.vel_y = -self.vel_y
                if bat.down and self.vel_y < 0:
                    self.vel_y = -self.vel_y

    def restart(self):
        time.sleep(2)
        # re-center ball
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.theta = 2 * math.pi * random.random()


class Bat:
    def __init__(self, type):
        self.width = 20
        self.height = 200
        self.up = False
        self.down = False
        self.y = 0
        self.type = type
        if self.type == "left":
            self.x = 0
            self.color = PLAYER_1
        elif self.type == "right":
            self.x = WIDTH - self.width
            self.color = PLAYER_2

    def draw(self,WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.height))

    def set_flag(bat_left, bat_right, event):
        if event.key == pygame.K_w:
            bat_left.up = True
        elif event.key == pygame.K_UP:
            bat_right.up = True                           
        if event.key == pygame.K_s:
            bat_left.down = True
        elif event.key == pygame.K_DOWN:
            bat_right.down = True

    def remove_flag(bat_left, bat_right, event):  
        if event.key == pygame.K_w:
            bat_left.up = False
        elif event.key == pygame.K_UP:
            bat_right.up = False
        if event.key == pygame.K_s:
            bat_left.down = False
        elif event.key == pygame.K_DOWN:
            bat_right.down = False

    def move(self):
        # Moving bats
        if self.up and self.y >= 0:
            self.y -= 15
        if self.down and self.y < HEIGHT - self.height:
            self.y += 15


main()