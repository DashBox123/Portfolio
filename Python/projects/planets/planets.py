import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800 # of window
AU = 1.496e11 # 1 AU in metres
G = 6.67430e-11
SCALE = 250 / AU # 1AU = 10 pixels
max_orbit_points = 700 # This needs to be adjusted dynamically!
TIMESTEP = 3600 * 24 # 1 day in seconds
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
ORANGE = (255,165,0)
FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    def __init__(self,x,y, radius, color, mass):
        self.x = x # in metres
        self.y = y # in metres
        self.radius = radius
        self.color = color
        self.mass = mass
        self.sun = False
        self.distance_to_sun = 0
        self.orbit_path = []
        self.x_vel = 0
        self.y_vel = 0

    def draw(self,win):
        x = self.x * SCALE + WIDTH / 2 # pygame windows have 0,0 in the top left hand corner
        y = self.y * SCALE + HEIGHT / 2 # pygame windows have 0,0 in the top left hand corner
        pygame.draw.circle(WIN, self.color, (x,y), self.radius)
        
        updated_points = []
        for point in self.orbit_path:
            x_orb, y_orb = point
            x_orb = x_orb * SCALE + WIDTH / 2
            y_orb = y_orb * SCALE + HEIGHT / 2
            updated_points.append((x_orb, y_orb))
        
        if len(self.orbit_path) > 2:
            pygame.draw.lines(WIN, self.color, False, updated_points,1)

        if len(updated_points) > max_orbit_points:
            updated_points = updated_points[-max_orbit_points:]
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/AU, 3)}AU", 1, WHITE)
            win.blit(distance_text, (x, y))

    def attraction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt((distance_x ** 2) + (distance_y ** 2))

        if other.sun:
            self.distance_to_sun = distance
        
        force = (G * self.mass * other.mass) / (distance ** 2)
        theta = math.atan2(distance_y,distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += (total_fx * TIMESTEP) / self.mass
        self.y_vel += (total_fy * TIMESTEP) / self.mass

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP

        self.orbit_path.append((self.x,self.y))
        if len(self.orbit_path) > max_orbit_points:
            self.orbit_path = self.orbit_path[-max_orbit_points:]

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.989e30)
    sun.sun = True

    earth = Planet(-1 * AU, 0, 16, BLUE, 5.972e24)
    earth.y_vel = 29.783e3 # in metres/second
    mars = Planet(-1.5 * AU, 0, 12, RED, 6.39e23)
    mars.y_vel = 24.077e3 # in metres/second
    mercury = Planet(-0.4 * AU, 0, 8, RED, 3.285e23)
    mercury.y_vel = -47.4e3 # in metres/second
    venus = Planet(-0.72 * AU, 0, 14, ORANGE, 4.867e24)
    venus.y_vel = -35.02e3 # in metres/second

    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        for event in pygame.event.get():
            # quit loop condition
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()    
            
    pygame.quit()

main()

 