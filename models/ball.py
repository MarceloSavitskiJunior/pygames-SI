import random
import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BALL_RADIUS, BALL_INITIAL_SPEED, BALL_MAX_SPEED, BALL_SPEED_INCREMENT,
    WHITE,
)

class Ball:

    def __init__(
        self,
        direction: int = 1,
        color: tuple[int, int, int] = WHITE,
        is_real: bool = True,
    ) -> None:
        self.radius = BALL_RADIUS
        self.color = color
        self.is_real = is_real
        self.x: float = 0.0
        self.y: float = 0.0
        self.vel_x: float = 0.0
        self.vel_y: float = 0.0
        self.reset(direction=direction)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def _random_vel_y(self) -> float:
        speed = random.uniform(2.0, BALL_MAX_SPEED * 0.6)
        return speed * random.choice([-1, 1])

    def reset(self, direction: int = 1) -> None:
        self.x = float(SCREEN_WIDTH // 2)
        self.y = float(SCREEN_HEIGHT // 2)
        self.vel_x = BALL_INITIAL_SPEED * direction
        self.vel_y = self._random_vel_y()

    def spawn_at(self, x: float, y: float, direction: int) -> None:
        self.x = x
        self.y = y
        self.vel_x = BALL_INITIAL_SPEED * direction
        self.vel_y = self._random_vel_y()

    def update(self) -> bool:
        self.x += self.vel_x
        self.y += self.vel_y

        bounced = False

        if self.y - self.radius <= 0:
            self.y = float(self.radius)
            self.vel_y = abs(self._random_vel_y())
            bounced = True
        elif self.y + self.radius >= SCREEN_HEIGHT:
            self.y = float(SCREEN_HEIGHT - self.radius)
            self.vel_y = -abs(self._random_vel_y())
            bounced = True

        return bounced

    def bounce_off_paddle(self, paddle_rect: pygame.Rect) -> bool:
        if not self.rect.colliderect(paddle_rect):
            return False

        hit = False

        if paddle_rect.centerx < SCREEN_WIDTH // 2 and self.vel_x < 0:
            speed = min(abs(self.vel_x) + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
            self.vel_x = speed
            self.vel_y = self._random_vel_y()
            hit = True
        elif paddle_rect.centerx > SCREEN_WIDTH // 2 and self.vel_x > 0:
            speed = min(abs(self.vel_x) + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
            self.vel_x = -speed
            self.vel_y = self._random_vel_y()
            hit = True

        return hit

    def out_of_bounds_left(self) -> bool:
        return self.x + self.radius < 0

    def out_of_bounds_right(self) -> bool:
        return self.x - self.radius > SCREEN_WIDTH

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)