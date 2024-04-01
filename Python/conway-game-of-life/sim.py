# Rules
# 1. A live cell with < 2 live neighbours dies (underpop)
# 2. A live cell with 2 - 3 live neighbours remains alive (survival)
# 3. A live cell with > 3 live neighbours dies (overpop)
# 4. A dead cell with = 3 live neighbours becomes alive (reproduction)
# Definitions
# 1. Each cell is surrounded by 8 other cells

import pygame
import random
import itertools
pygame.init()

# colours
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

# screen constants
WIDTH, HEIGHT = 1000, 1000
CELL_SIZE = 20
COL_NUM = WIDTH // CELL_SIZE
ROW_NUM = HEIGHT // CELL_SIZE
BAR_HEIGHT = 0
FPS = 60
FONT = pygame.font.SysFont("comicsans", 16)

# initialise pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def main():
    RUN = True
    PLAY = False
    count = 0
    update_freq = 30
    
    # set stores positions as tuples of live cells
    lives = set()
    while RUN:
        clock.tick(FPS)

        if PLAY:
            count += 1

        if count == update_freq:
            count = 0
            update_grid(lives)

        pygame.display.set_caption("Playing" if PLAY else "Pause")

        # event handling
        for event in pygame.event.get():
            # quit loop condition
            if event.type == pygame.QUIT:
                RUN = False

            if pygame.mouse.get_pressed():
                update_cell(lives)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PLAY = not PLAY
                if event.key == pygame.K_c:
                    lives.clear()
                    PLAY = False
                    count = 0
                if event.key == pygame.K_r:
                    lives.clear()
                    lives.update(gen(random.randrange(10, 20) * COL_NUM))
        
        window.fill(GREY)
        draw_grid(lives)

        pygame.display.update()

    # closes window once while loop is finished
    pygame.quit()

def update_cell(lives):
    x, y = pygame.mouse.get_pos()
    col = y // CELL_SIZE
    row = x // CELL_SIZE
    pos = (row, col)
    if pos in lives and pygame.mouse.get_pressed()[2]: # right mouse button clicked
        lives.remove(pos)
    elif pos not in lives and pygame.mouse.get_pressed()[0]: # left mouse button
        lives.add(pos)

def draw_grid(lives):
    # draw live cells
    for (row, col) in lives:
        cell_origin = (row*CELL_SIZE, col*CELL_SIZE)
        pygame.draw.rect(window, YELLOW, (*cell_origin , CELL_SIZE, CELL_SIZE))

    # draw gridlines
    for row, col in zip(range(ROW_NUM), range(COL_NUM)):
        # horizontal lines
        if row * CELL_SIZE <= HEIGHT - BAR_HEIGHT:
            pygame.draw.line(window, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE))
        # vertical lines
        pygame.draw.line(window, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT - BAR_HEIGHT))

def draw_bar():
    pass

def gen(number):
    return set((random.randrange(0, COL_NUM), random.randrange(0, ROW_NUM)) for _ in range(number))

def update_grid(lives):
    # set to contain cells that are new-born
    new_cells = set()
    # set to contain cells that are dead
    dead_cells = set()

    for cell in lives:
        # makes new set that only contains those neighbours that are alive
        live_neighbours = set(x for x in get_neighbours(cell) if x in lives)
        # makes new set that only contains those neighbours that are dead
        dead_neighbours = set(x for x in get_neighbours(cell) if x not in lives)

        # if this live cell does not have 2-3 live neighbours it dies
        if len(live_neighbours) not in [2, 3]:
            dead_cells.add(cell)

        # we loop over it's dead neighbours
        for neighbour in dead_neighbours:
            # get the live neighbours of this dead neighbour
            live_neighbours_2 = set(x for x in get_neighbours(neighbour) if x in lives)
            # add this dead neighbour to the newborn cells set if it has 3 live neighbours
            if len(live_neighbours_2) == 3:
                new_cells.add(neighbour)

    lives |= new_cells # new cells
    lives -= dead_cells # dead cells

def get_neighbours(cell):
    x, y = cell
    neighbours = []
    for dx, dy in itertools.product([-1, 0, 1], repeat = 2):
        if ((dx == 0 and dy == 0) or
        not (0 <= x + dx < COL_NUM) or
        not (0 <= y + dy < ROW_NUM)):
            continue
        else:
            neighbours.append((x + dx, y + dy))

    return neighbours

main()

