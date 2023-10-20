import pygame 
import math
import random
pygame.init()

WIDTH, HEIGHT = 900,700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Physics")

RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255,165,0)
PINK = (255,192,203)
BLUE = (0,0,255)
GREEN = (0,255,0)
FONT = pygame.font.SysFont("pluto", 35)
FPS = 60

class Particle:
    g = 9.8
    SCALE = 1/1
    TIMESTEP = 0.1 #10 sec each frame

    def __init__(self, x, y, color, radius, vel, angle):
        self.radius = radius
        self.color = color
        self.origin_x = x
        self.origin_y = y
        self.range = 0

        self.u = vel
        self.angle = angle
        # self.radian = self.angle * math.atan2(0,-1)/180
        # self.x_vel = self.u * math.cos(self.radian)
        # self.y_vel = self.u * math.sin(self.radian)

        # self.radian = self.angle * math.atan2(0,-1)/180
        self.x_vel = self.u * math.cos(self.angle)
        self.y_vel = self.u * math.sin(self.angle)
        self.traject = []
        self.x = x
        self.y = y
    
    def draw_particle(self, win):
        x = self.x * self.SCALE
        y = self.y * self.SCALE
        
        pygame.draw.circle(win, self.color, (x,y), self.radius)
        if(len(self.traject) > 2):
            if(len(self.traject) > 30 or self.range == 1):
                self.traject.pop(0)
            pygame.draw.lines(win,PINK,False,self.traject,2)
    def movement(self):
        if(self.y <= self.origin_y):
            self.x = self.x + self.x_vel * self.TIMESTEP
            self.y_vel = self.y_vel - self.g * self.TIMESTEP
            self.y = self.y - self.y_vel * self.TIMESTEP
            self.traject.append((self.x, self.y))
        else:
            self.range = 1

def get_color():
    colors = [RED, BLUE, GREEN, BLACK, WHITE, PINK]
    color = random.choice(colors)
    return color

def get_vel():
    vel = [100, 110, 120, 130, 150, 180, 190, 200]
    return random.choice(vel)

def mouse_angle(slope, origin_x, origin_y):
    
    if(slope[0] == 0 and slope[1] == 0):
        angle45 = math.atan2(0,-1)/4
        return math.sin(angle45), math.cos(angle45), angle45

    x_len = slope[0] - origin_x
    y_len = origin_y - slope[1]

    angle = math.atan2(y_len, x_len)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return sin_angle, cos_angle, angle

def Coord_sys(x, y, win):

    pygame.draw.line(win, BLACK, [x*0.05,y*0.9], [x*0.9, y*0.9], 2) #x axis
    pygame.draw.line(win, BLACK, [x*0.1,y*0.95], [x*0.1, y*0.05], 2) #y axis

    origin_x, origin_y = x*0.1, y*0.9

    x_text = FONT.render("X",1,BLACK)
    y_text = FONT.render("y",1,BLACK)

    (mx, my) = pygame.mouse.get_pos()
    sin, cos, angle = mouse_angle((mx,my), origin_x, origin_y)
    line_len = 100

    x_coord = round(line_len*cos + origin_x, 2)
    y_coord = round(origin_y - line_len*sin, 2)

    pygame.draw.line(win, BLUE, [origin_x, origin_y], [x_coord, y_coord], 2) #projecting line


    win.blit(x_text, (x*0.9, y*0.9 - x_text.get_height()/2 + 2)) #x axis label
    win.blit(y_text, (x*0.1 - y_text.get_width()/2 + 3, y*0.05 - (y_text.get_height()/2) - 15 )) #y axis label
    
    angle_text = FONT.render("angle:"+str(round(angle*180/math.atan2(0,-1),2)), 1, BLACK)
    line_end_text = FONT.render("line:"+str(x_coord) + ", " + str(y_coord), 1, BLACK)
    mouse_coord_text = FONT.render("mouse:"+str(mx) + ", " + str(my), 1, BLACK)
    origin_text = FONT.render("origin:"+str(origin_x) +", "+ str(origin_y), 1, BLACK)

    win.blit(angle_text, (0.7*WIDTH, 0.1*HEIGHT))
    win.blit(line_end_text, (0.7*WIDTH, 0.2*HEIGHT))
    win.blit(mouse_coord_text, (0.7*WIDTH, 0.3*HEIGHT))
    win.blit(origin_text, (0.7*WIDTH, 0.4*HEIGHT))
    return origin_x, origin_y, angle



def main():
    # particle1 = Particle(WIDTH*0.1, HEIGHT*0.9, RED, 10, 100, 70)

    particles = []
    clock = pygame.time.Clock()
    run = True 

    while run:
        clock.tick(FPS)
        WIN.fill(ORANGE)
        x, y, angle = Coord_sys(WIDTH, HEIGHT, WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    print("angle:", angle)
                    particle1 = Particle(x,y,get_color(), 10, get_vel(), angle)
                    particles.append(particle1)
        for particle in particles:
            particle.movement()
            particle.draw_particle(WIN)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()