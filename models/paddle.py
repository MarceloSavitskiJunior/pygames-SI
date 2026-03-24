import pygame
from settings import SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED, WHITE

class Paddle:

    def __init__(self, x: int) -> None:
        self.x = x
        self.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move_up(self) -> None:
        self.y = max(0, self.y - self.speed)

    def move_down(self) -> None:
        self.y = min(SCREEN_HEIGHT - self.height, self.y + self.speed)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, WHITE, self.rect)