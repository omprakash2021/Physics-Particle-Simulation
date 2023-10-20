import pygame, math, random
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
    TIMESTEP = 0.1

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
    
    def after_collision_vel(self, particles):
        for other in particles:
            if other == self:
                continue
            distance = math.hypot(self.x - other.x, self.y - other.y)
            if distance <= (self.radius + other.radius):
                m1, m2 = self.mass, other.mass
                v1x_i, v2x_i = self.vel[0], other.vel[0]
                v1y_i, v2y_i = self.vel[1], other.vel[1]

                v1x_f = ((2*m2*v2x_i) + (m1 - m2)*v1x_i)/(m1 + m2)
                v2x_f = ((2*m1*v1x_i) - (m1 - m2)*v2x_i)/(m1 + m2)

                v1y_f = ((2*m2*v2y_i) + (m1 - m2)*v1y_i)/(m1 + m2)
                v2y_f = ((2*m1*v1y_i) - (m1 - m2)*v2y_i)/(m1 + m2)

                self.vel[0], self.vel[1] = v1x_f, v1y_f
                other.vel[0], other.vel[1] = v2x_f, v2y_f

    def border_collision_check(self, brd_x, brd_y, brd_w, brd_h, particles, P0, Pf):
        right_collision = self.x + self.radius
        left_collision = self.x - self.radius
        up_collision = self.y - self.radius
        down_collision = self.y + self.radius
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
            dir_x *= -1
            dir_y *= 1
        if(up_collision <= (brd_y)):
            y = brd_y + self.radius
            x = P0[0] + ((Pf[0] - P0[0])/(Pf[1] - P0[1])) * (y - Pf[1])
            dir_x *= 1
            dir_y *= -1
        if(down_collision >= (brd_h + brd_y)):
            y = brd_y + brd_h - self.radius
            x = P0[0] + ((Pf[0] - P0[0])/(Pf[1] - P0[1])) * (y - Pf[1])
            dir_x *= 1
            dir_y *= -1

        return dir_x, dir_y
            

    def movement(self, brd_x, brd_y, brd_w, brd_h, particles):
        P0 = [self.x, self.y] #initial position

        self.x += self.vel[0] * self.TIMESTEP
        self.y -= self.vel[1] * self.TIMESTEP

        Pf = [self.x, self.y] #final position

        dir_x, dir_y = self.border_collision_check(brd_x, brd_y, brd_w, brd_h, particles, P0, Pf)
        self.vel[0] *= dir_x
        self.vel[1] *= dir_y
        self.after_collision_vel(particles)


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

    particles = []
    # color_list = [RED, GREEN, BLACK, WHITE, VOILET, BLUE, LIGHT_BLUE, YELLOW]
    color_list = [VOILET]

    mass = 100
    length = 200
    density = mass/length #mass per unit length(radius)

    for num in range(1,11):
        angle = random.randint(-180, 180)
        color = random.choice(color_list)
        radius = random.randint(10,35)
        particle_mass = density * radius
        velocity = 100/particle_mass #heavy paritcle will have less velocity
        pos_x = random.randint(border_x + radius, border_x + border_width - radius)
        pos_y = random.randint(border_y + radius, border_y + border_height - radius)
        if len(particles) == 0:
            particle1 = Particle(pos_x, pos_y, particle_mass, radius, velocity, color, angle)
            particles.append(particle1)
        if len(particles) > 0:
            for other in particles:
                dist = math.hypot(other.y - pos_y, other.x - pos_x)
                dist_radius = other.radius + radius
                if dist < dist_radius:
                    break
            else:
                particle2 = Particle(pos_x, pos_y, particle_mass, radius, velocity, color, angle)
                particles.append(particle2)

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