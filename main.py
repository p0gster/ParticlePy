import pygame
import numpy as np


class particle:
    def __init__(self,radius,mass,position,velocity):
        self.mass=mass

        self.position=position
        self.velocity=velocity
        self.radius=radius

    def updatepos(self):
        global timestep
        self.position+=self.velocity*timestep

    def impulse(self,impulse):
        self.velocity+=impulse/self.mass

def interact(particle_1,particle_2,gravity=False):
    global timestep, G
    """
    Collides particles if particles in range of each other
    """

    particle_1_to_particle_2=particle_2.position-particle_1.position
    distance=np.linalg.norm(particle_1_to_particle_2)

    if gravity==True:
        impulse_particle_2 = -G*particle_1.mass*particle_2.mass/distance**2 * particle_1_to_particle_2 * timestep
        impulse_particle_1=-impulse_particle_2

        particle_2.impulse(impulse_particle_2)
        particle_1.impulse(impulse_particle_1)


    if distance<(particle_1.radius+particle_2.radius):
        normal=particle_1_to_particle_2/distance

        vel_2_rel_vel_1=particle_2.velocity-particle_1.velocity

        mass_product=particle_1.mass*particle_2.mass
        mass_sum=particle_1.mass+particle_2.mass

        mass_product_per_sum=mass_product/mass_sum

        vel_2_rel_vel_1_normal_comp=np.dot(normal,vel_2_rel_vel_1)

        impulse_particle_2_normal_comp= -2*mass_product_per_sum * vel_2_rel_vel_1_normal_comp

        impulse_particle_2=impulse_particle_2_normal_comp*normal
        impulse_particle_1=-impulse_particle_2

        particle_2.impulse(impulse_particle_2)
        particle_1.impulse(impulse_particle_1)


def interact_particles(particles):
    for particle_num_1 in range(len(particles)):
        particle_a=particles[particle_num_1]

        for particle_num_2 in range(particle_num_1+1,len(particles)):
            particle_b=particles[particle_num_2]

            interact(particle_a,particle_b)




def render(particles,color="blue"):
    for particle in particles:
        pygame.draw.circle(screen, color, particle.position, particle.radius)

def bounce_edge(particle,windowsize):
    x=particle.position[0]
    y=particle.position[1]

    radius=particle.radius

    v_x=particle.velocity[0]
    v_y=particle.velocity[1]

    width=windowsize[0]
    height=windowsize[1]

    if width-x<radius or x<radius:
        v_x= -v_x
    if height-y<radius or y<radius:
        v_y = -v_y

    particle.velocity[0]=v_x
    particle.velocity[1]=v_y

def bounce_edge_particles(particles,windowsize):
    for particle in particles:
        bounce_edge(particle,windowsize)

def update_positions(particles):
    for particle in particles:
        particle.updatepos()

def gen_1():
    particles = [particle(50, 10, np.array([250.0, 250.0]), np.array([20.0, 0])),
                 particle(50, 10, np.array([800.0, 325]), np.array([-20.0, 0]))]

    return particles

def gen_2():
    particles = []
    for x in range(5):
        particles += [particle(30, 10, np.array([250.0, 250.0 + 80 * x]), np.array([80.0, -80.0])*2)]

    for x in range(5):
        particles += [particle(30, 10, np.array([800.0, 250.0 + 80 * x]), np.array([-80.0, 80.0])*2)]

    return particles

speed_per_dist=0.5
color="blue"
windowsize = ( 1500, 800)
change_radius_per_press=5
timestep=0.02
G=10

screen = pygame.display.set_mode(windowsize)

particles=[]

radius=50
density=1/np.sqrt(5*np.pi)


particles=gen_2()

velocity_line=False
virtual_particle=False
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type != pygame.MOUSEWHEEL:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_1 = np.array(pygame.mouse.get_pos()).astype(float)
                velocity_line=True

            if event.type == pygame.MOUSEBUTTONUP:
                velocity_line=False

                pos_2 = np.array(pygame.mouse.get_pos()).astype(float)
                particles+=[ particle(radius, np.pi*radius**2*density, pos_1, (pos_2-pos_1)*speed_per_dist) ]

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                particles=[]

            if event.key == pygame.K_q:
                virtual_particle= not(virtual_particle)

            if event.key == pygame.K_r:
                radius += change_radius_per_press

            if event.key == pygame.K_e:
                radius -= change_radius_per_press



    if velocity_line==True:
        mouse_pos=np.array(pygame.mouse.get_pos()).astype(float)
        pygame.draw.line(screen,"white",pos_1,mouse_pos)

    if virtual_particle==True:
        pygame.draw.circle(screen, color, np.array(pygame.mouse.get_pos()).astype(float), radius)

    bounce_edge_particles(particles,windowsize)
    interact_particles(particles)
    update_positions(particles)
    render(particles)

    pygame.display.update()
    pygame.time.delay(10)
    screen.fill((0, 0, 0))