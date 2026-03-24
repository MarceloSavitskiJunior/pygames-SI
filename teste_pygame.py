import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DvD do Marcelo")

DARK_BG = (15, 15, 30)
FONT_SIZE = 60
font = pygame.font.SysFont(None, FONT_SIZE)
small_font = pygame.font.SysFont(None, 24)


def random_color():
    return (
        random.randint(80, 255),
        random.randint(80, 255),
        random.randint(80, 255),
    )

def random_velocity(speed=3):
    return speed * random.choice([-1, 1]), speed * random.choice([-1, 1])

class NameObject:
    def __init__(self, name, x, y):
        self.name = name
        self.color = random_color()
        self.surface = font.render(self.name, True, self.color)
        self.rect = self.surface.get_rect(center=(x, y))
        self.vx, self.vy = random_velocity()

    def recolor(self):
        self.color = random_color()
        self.surface = font.render(self.name, True, self.color)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.vx = -abs(self.vx)
            self.recolor()
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.vx = abs(self.vx)
            self.recolor()

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vy = -abs(self.vy)
            self.recolor()
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.vy = abs(self.vy)
            self.recolor()

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

def handle_collisions(objects):
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            a = objects[i]
            b = objects[j]
            if a.rect.colliderect(b.rect):
                a.vx, b.vx = b.vx, a.vx
                a.vy, b.vy = b.vy, a.vy
                a.rect.x += a.vx
                a.rect.y += a.vy
                b.rect.x += b.vx
                b.rect.y += b.vy
                a.recolor()
                b.recolor()

objects = [
    NameObject("Marcelo", WIDTH // 3, HEIGHT // 2),
    NameObject("Rafael", 2 * WIDTH // 3, HEIGHT // 2),
]

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(DARK_BG)

    for obj in objects:
        obj.update()

    handle_collisions(objects)

    for obj in objects:
        obj.draw(screen)

    hud = small_font.render("Game do marcelo", True, (180, 180, 200))
    screen.blit(hud, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()