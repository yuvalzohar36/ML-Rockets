import pygame
import sys
import random
import math

screen_size = [600, 600]
pygame.init()
black = (100, 100, 100)
clock = pygame.time.Clock()
pygame.font.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))


class Rocket:
    def __init__(self, dna_arg):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.dist = 0
        self.fitness = 1
        self.counter = 0
        if dna_arg is None:
            self.DNA = DNA(None)
        else:
            self.DNA = dna_arg
        self.x = 300
        self.y = 570
        self.x_circle = 290
        self.y_circle = 130
        self.height = 30
        self.width = 10
        self.width_circle = 20
        self.height_circle = 20
        self.acc_x = 0
        self.acc_y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.rect = pygame.draw.rect(screen, self.black, [self.x, self.y, self.width, self.height])
        self.obstacle = pygame.draw.rect(screen, self.black, [(self.x_circle, self.y_circle), (self.width_circle, self.height_circle)])
        self.collide_target_bool = False
        self.collide_bool = False

    def force(self):
        self.acc_x += (self.DNA.genes[self.counter][0])
        self.vel_x += self.acc_x
        self.x += self.vel_x
        self.acc_y -= (self.DNA.genes[self.counter][1])
        self.vel_y -= self.acc_y
        self.y += self.vel_y

    def collide_target(self):
        if self.obstacle.colliderect(self.rect):
            self.collide_target_bool = True

    def collide(self):
        if self.x > 580 or self.x < 0 or self.y > 590 or self.y < 0:
            self.collide_bool = True

    def calc_dist(self):
        self.dist = math.sqrt(((self.x - self.x_circle) ** 2) + ((self.y - self.y_circle) ** 2))
        if self.dist < 25:
            self.collide_target_bool = True

    def calc_fitness(self):
        self.collide_target()
        self.collide()
        self.calc_dist()
        if self.collide_target_bool:
            self.fitness *= 10
        if self.collide_bool:
            self.fitness /= 10

    def show(self):
        self.rect = pygame.draw.rect(screen, self.black, [self.x, self.y, self.width, self.height])
        self.obstacle = pygame.draw.rect(screen, self.black, [(self.x_circle, self.y_circle), (self.width_circle, self.height_circle)])

    def update_counter(self):
        if self.counter == 50:
            self.counter = 0
        self.counter += 1
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(self.counter), False, (0, 0, 0))
        screen.blit(textsurface, (0, 0))

    def update(self):
        self.update_counter()
        if self.collide_target_bool is False and self.collide_bool is False:
            self.force()
            self.collide()
            self.collide_target()


class Pop:
    def __init__(self):
        self.pop_size = 25
        self.all_rockets = []
        self.mating_pool = []
        for i in range(self.pop_size):
            self.all_rockets.append(Rocket(None))

    def evaluate(self):
        maxfit=0
        for i in self.all_rockets:
            i.calc_fitness()
            if i.fitness > maxfit:
                maxfit = i.fitness
        for j in self.all_rockets:
            j.fitness /= maxfit
            #print(j.fitness)
        self.mating_pool = []
        for m in self.all_rockets:
            num = int(m.fitness * 100)
            #print(num)
            for i in range(num):
                self.mating_pool.append(m)
        print(len(self.mating_pool))

    def select(self):
        new_rockets = []
        for i in range(len(self.all_rockets)):
            ParentA = self.mating_pool[random.randint(0, len(self.mating_pool))].DNA
            ParentB = self.mating_pool[random.randint(0, len(self.mating_pool))].DNA
            child = ParentA.cross_over(ParentB)
            child.mutation()
            new_rockets.append(Rocket(child))
        self.all_rockets = new_rockets

    def update(self):
        screen.fill((255, 255, 255))
        for i in self.all_rockets:
            i.show()
            i.update()
        pygame.display.flip()
        clock.tick(10)


class DNA:
    def __init__(self, gen):
        self.lifespan = 200
        if gen is None:
            self.genes = []
            for i in range(self.lifespan):
                self.genes.append([random.randint(-1, 1), random.randint(-1, 1)])
        else:
            self.genes = gen

    def cross_over(self, partner):
        newgenes = []
        mid = random.randint(0, len(self.genes))
        for i in range(len(self.genes)):
            if i > mid:
                newgenes.append(self.genes[i])
            else:
                newgenes.append(partner.genes[i])
        return DNA(newgenes)

    def mutation(self):
        for i in self.genes:
            if random.randint(0,1) < 0.01:
                i = [random.randint(-1, 1), random.randint(-1, 1)]


if __name__ == '__main__':
    while True:
        count = 0
        Dat = Pop()
        while count < 50:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            Dat.update()
            count += 1
        Dat.evaluate()
        Dat.select()
