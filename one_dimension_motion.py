import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("One Dimension Motion")

WHITE = (255,255,255)
ORANGE = (255,165,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
FONT = pygame.font.SysFont("lato", 40)
FPS = 60

class particle:
    g = 9.8
    TIMESTEP = 0.1

    def __init__(self, x, y, radius, vel):
        self.x = x
        self.y = y
        self.radius = radius
        self.y_vel = vel

    def draw_particle(self,win):
        pygame.draw.circle(win, RED, (self.x, self.y), self.radius)
        # print("self.y_vel:",self.y_vel, ", y:", self.y)
    
    def movement(self):
        self.y_vel = self.y_vel - self.g * self.TIMESTEP
        self.y = self.y - self.y_vel * self.TIMESTEP

def mouse_angle(mx, my, origin_x, origin_y):
    
    if(mx == 0 and my == 0):
        angle45 = math.atan2(0,-1)/4
        return math.sin(angle45), math.cos(angle45), angle45*180/math.atan2(0,-1)

    x_len  = mx - origin_x
    y_len = origin_y - my

    angle = math.atan2(y_len, x_len)
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return sin_angle, cos_angle, angle*180/math.atan2(0,-1)

def draw_coordSys(win):
    pygame.draw.line(win, BLACK, [0.1*WIDTH, 0.9*HEIGHT], [0.9*WIDTH, 0.9*HEIGHT], 2) #x axis
    pygame.draw.line(win, BLACK, [0.15*WIDTH, 0.95*HEIGHT], [0.15*WIDTH, 0.1*HEIGHT], 2) #y axis

    origin_x, origin_y = 0.15*WIDTH, 0.9*HEIGHT
    x_text = FONT.render("X", 1, BLACK)
    y_text = FONT.render("Y", 1, BLACK)

    mx, my = pygame.mouse.get_pos()
    sin, cos, angle = mouse_angle(mx,my, origin_x, origin_y)
    line_len = 100

    x_coord = round(line_len*cos + origin_x, 2)
    y_coord = round(origin_y - line_len*sin, 2)

    pygame.draw.line(win, BLUE, [0.15*WIDTH, 0.9*HEIGHT], [x_coord, y_coord], 2)
   
    win.blit(x_text, (0.9*WIDTH + 2, 0.9*HEIGHT - x_text.get_height()/2 + 2))
    win.blit(y_text, (0.15*WIDTH - y_text.get_width()/2, 0.1*HEIGHT - y_text.get_height()))

    # angle_text = FONT.render("angle:"+str(round(angle,2)), 1, BLACK)
    # line_end_text = FONT.render("line:"+str(x_coord) + ", " + str(y_coord), 1, BLACK)
    # mouse_coord_text = FONT.render("mouse:"+str(mx) + ", " + str(my), 1, BLACK)
    # origin_text = FONT.render("origin:"+str(0.15*WIDTH) +", "+ str(0.9*HEIGHT), 1, BLACK)

    # win.blit(angle_text, (0.7*WIDTH, 0.1*HEIGHT))
    # win.blit(line_end_text, (0.7*WIDTH, 0.2*HEIGHT))
    # win.blit(mouse_coord_text, (0.7*WIDTH, 0.3*HEIGHT))
    # win.blit(origin_text, (0.7*WIDTH, 0.4*HEIGHT))

def main():
    particles = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(ORANGE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    pass
        for ball in particles:
            ball.movement()
            ball.draw_particle(WIN)
        draw_coordSys(WIN)
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()
