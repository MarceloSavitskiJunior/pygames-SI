import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS, BALL_INITIAL_SPEED, WHITE
)

class Ball:
    def __init__(self) -> None:
        self.radius = BALL_RADIUS
        self.x: float = 0.0
        self.y: float = 0.0
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.reset(direction=1)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def reset(self, direction: int = 1) -> None:
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel_x = BALL_INITIAL_SPEED * direction
        self.vel_y = BALL_INITIAL_SPEED

    def update(self) -> None:
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
            self.vel_y = -self.vel_y
            self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))

    def bounce_off_paddle(self, paddle_rect: pygame.Rect) -> None:
        if not self.rect.colliderect(paddle_rect):
            return

        if paddle_rect.centerx < SCREEN_WIDTH // 2 and self.vel_x < 0:
            self.vel_x = -self.vel_x
        elif paddle_rect.centerx > SCREEN_WIDTH // 2 and self.vel_x > 0:
            self.vel_x = -self.vel_x

    def out_of_bounds_left(self) -> bool:
        return self.x + self.radius < 0

    def out_of_bounds_right(self) -> bool:
        return self.x - self.radius > SCREEN_WIDTH

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)