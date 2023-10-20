import pygame, math
pygame.init()

WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Collision")

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
PINK = (255,51,153)
ORANGE = (255,128,0)
YELLOW = (255,255,0)
LIGHT_BLUE = (0,204,204)
VOILET = (153,0,153)

FPS = 60

class Particle:
    SCALE = 0.1 #10 m is 1 pixel
    TIMESTEP = 0.1 # 1/FPS, time between each Frames

    def __init__(self, x, y, mass, radius, vel, color, angle):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius

        self.radian = angle * math.atan2(0,-1) / 180
        self.x_vel = math.cos(self.radian) * vel
        self.y_vel = math.sin(self.radian) * vel
        self.vel = [self.x_vel, self.y_vel]
        self.color = color
        # print("vel:", vel, ", x_vel:", self.x_vel, ", y_vel:", self.y_vel)

    def draw_particle(self, win):
        x = self.x  
        y = self.y 
        pygame.draw.circle(win, self.color, (x,y), self.radius)
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def momentumChanged(self, m1, v1_i, m2, v2_i):
        v1_f = ((2*m2*v2_i) + (m1 - m2)*v1_i)/(m1 + m2)
        v2_f = ((2*m1*v1_i) - (m1 - m2)*v2_i)/(m1 + m2)
        return v1_f, v2_f

    def after_collision_vel(self, particles, P0, Pf):
        for other in particles:
            if other == self:
                continue
            distance = math.hypot(self.x - other.x, self.y - other.y)
            if distance == (self.radius + other.radius):
                m1, m2 = self.mass, other.mass
                v1x_i, v2x_i = self.vel[0], other.vel[0]
                v1y_i, v2y_i = self.vel[1], other.vel[1]

                v1x_f, v2x_f = self.momentumChanged(m1, v1x_i, m2, v2x_i)
                v1y_f, v2y_f = self.momentumChanged(m1, v1y_i, m2, v2y_i)

                self.vel[0], self.vel[1] = v1x_f, v1y_f
                other.vel[0], other.vel[1] = v2x_f, v2y_f

            if distance < (self.radius + other.radius):
                m1 = (Pf[1] - P0[1])/(Pf[0] - P0[0]) #slope of point at final and initial position
                if(m1 == 0):
                    m1, m2 = self.mass, other.mass
                    v1x_i, v2x_i = self.vel[0], other.vel[0]
                    v1y_i, v2y_i = self.vel[1], other.vel[1]

                    v1x_f, v2x_f = self.momentumChanged(m1, v1x_i, m2, v2x_i)
                    v1y_f, v2y_f = self.momentumChanged(m1, v1y_i, m2, v2y_i)

                    self.vel[0], self.vel[1] = v1x_f, v1y_f
                    other.vel[0], other.vel[1] = v2x_f, v2y_f

                    x_c, y_c = other.x, other.y
                    x_i, y_i = P0[0], P0[1]
                    d = self.distance(x_c, y_c, x_i, y_i)
                    d1 = self.radius + other.radius

                    x = (x_i - x_c)*(d1/d) + x_c
                    y = (y_i - y_c)*(d1/d) + y_c
                    self.x, self.y = x, y
                    
                    if(self.radius == 10):
                        print("small")
                    else:
                        print("large")
                    
                    print("v1x_i:", v1x_i, ", v1y_i:", v1y_i)
                    print("v2x_i:", v2x_i, ", v2y_i:", v2y_i)

                    print("v1x_f:", v1x_f, ", v1y_i:", v1y_f)
                    print("v2x_f:", v2x_f, ", v2y_f:", v2y_f)

                    # print("initial_pos=", P0[0], ",", P0[1])
                    # print("initial_dist_to_center=", self.distance(P0[0], P0[1], x_c, y_c))
                    # print("final_pos=", Pf[0], ",", Pf[1])
                    # print("final_dist_to_center=", self.distance(Pf[0], Pf[1], x_c, y_c))
                    # print("changed_pos=", self.x, ",", self.y)
                    # # print("r + R = ", self.radius + other.radius)
                    # print("center_self_to_other = ", self.distance(self.x, self.y, other.x, other.y))
                    print("\n")

                else:
                    m2 = -(1/m1) #perpendicular of the slope m1
                    x_c, y_c = other.x ,other.y #position of other particle
                    #x_p, y_p are the points which are parpendicular by center of particle to the line passing intial and final position of the particle
                    x_p = m1 * (P0[2] - m1*P0[0] - y_c - (-1/m1)*x_c) / (m1**2 - 1)
                    y_p = (-1/m1) * x_p + (y_c + (1/m1)*x_c)
                    
                    d1 = self.distance(x_c, y_c, x_p, y_p) #perpendicular distance from center of the particle 
                    d2 = self.radius + other.radius #hypotaneous distance from where we want our point
                    d3 = math.sqrt(d2**2 - d1**2) 
                    d4 = self.distance(P0[0], P0[1], x_p, y_p) #distance between intian position of particle and parpendicaler point x_p, y_p

                    r = d4 - d3
                    ratio = r/d4 #deviding the line into r:d3, because r + d3 = d4
                    x = (x_p - P0[0])*(ratio) + P0[0]
                    y = (y_p - P0[1])*(ratio) + P0[1]

                    self.x, self.y = x, y

                    m1, m2 = self.mass, other.mass
                    v1x_i, v2x_i = self.vel[0], other.vel[0]
                    v1y_i, v2y_i = self.vel[1], other.vel[1]

                    v1x_f, v2x_f = self.momentumChanged(m1, v1x_i, m2, v2x_i)
                    v1y_f, v2y_f = self.momentumChanged(m1, v1y_i, m2, v2y_i)

                    self.vel[0], self.vel[1] = v1x_f, v1y_f
                    other.vel[0], other.vel[1] = v2x_f, v2y_f

    def border_collision_check(self, brd_x, brd_y, brd_w, brd_h, particles, P0, Pf):
        right_collision = Pf[0] + self.radius
        left_collision = Pf[0] - self.radius
        up_collision = Pf[1] - self.radius
        down_collision = Pf[1] + self.radius
        dir_x, dir_y = 1, 1

        if(right_collision >= (brd_x + brd_w)):
            x = brd_x + brd_w - self.radius
            y = P0[1] + ((Pf[1] - P0[1])/(Pf[0] - P0[0])) * (x - P0[0])
            self.x, self.y = x, y
            dir_x *= -1
            dir_y *= 1
        
        if(left_collision <= (brd_x)):
            x = brd_x + self.radius
            y = P0[1] + ((Pf[1] - P0[1])/(Pf[0] - P0[0])) * (x - P0[0])
            self.x, self.y = x, y
            dir_x *= -1
            dir_y *= 1
        if(up_collision <= (brd_y)):
            y = brd_y + self.radius
            x = P0[0] + ((Pf[0] - P0[0])/(Pf[1] - P0[1])) * (y - Pf[1])
            self.x, self.y = x, y
            dir_x *= 1
            dir_y *= -1
        if(down_collision >= (brd_h + brd_y)):
            y = brd_y + brd_h - self.radius
            x = P0[0] + ((Pf[0] - P0[0])/(Pf[1] - P0[1])) * (y - Pf[1])
            self.x, self.y = x, y
            dir_x *= 1
            dir_y *= -1

        return dir_x, dir_y
            
    def movement(self, brd_x, brd_y, brd_w, brd_h, particles):
        P0 = [self.x, self.y]
        self.x += self.vel[0] * self.TIMESTEP
        self.y -= self.vel[1] * self.TIMESTEP
        Pf = [self.x, self.y]
        dir_x, dir_y = self.border_collision_check(brd_x, brd_y, brd_w, brd_h, particles, P0, Pf)
        self.vel[0] *= dir_x
        self.vel[1] *= dir_y
        self.after_collision_vel(particles, P0, Pf)

def draw_container(win):
    win.fill(ORANGE)
    x1, y1 = (WIDTH * 0.1, HEIGHT * 0.1)
    container_width = WIDTH - x1*2
    container_height = HEIGHT - y1*2
    pygame.draw.rect(win,VOILET,pygame.Rect(x1,y1,container_width,container_height), 3)
    bottom_mid_x = x1 + container_width/2
    bottom_mid_y = y1 + container_height
    return x1, y1, container_width, container_height

def main():
    border_x, border_y, border_width, border_height = draw_container(WIN)
    mass = 100
    radius = 40
    vel = 10
    color = RED
    angle = 0
    particle1 = Particle(border_x + radius, border_y + border_height/2, mass, radius, vel, color, angle)
    particle2 = Particle(border_x + border_width - 10, border_y + border_height/2, 10, 10, 50, LIGHT_BLUE, -180)
    particles = [particle1, particle2]

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        draw_container(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for particle in particles:
            particle.movement(border_x, border_y, border_width, border_height, particles)
            particle.draw_particle(WIN)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()