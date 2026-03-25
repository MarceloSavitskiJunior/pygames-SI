import random
import time

import pygame

from models.ball import Ball
from settings import WHITE, SCREEN_WIDTH

FRAGMENT_INTERVAL: float = 5.0
FRAGMENT_COUNT: int = 4

_DECOY_COLOURS: list[tuple[int, int, int]] = [
    (255, 80,  80),
    (80,  200, 80),
    (80,  160, 255),
    (255, 220, 50),
    (220, 80,  255),
    (255, 140, 0),
    (0,   220, 200),
    (255, 105, 180),
]


def _random_decoy_color(exclude: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    available = [c for c in _DECOY_COLOURS if c not in exclude]
    if not available:
        available = _DECOY_COLOURS
    return random.choice(available)


class BallManager:

    def __init__(self) -> None:
        self._balls: list[Ball] = []
        self._last_fragment_time: float = time.time()
        self._fragment_ready: bool = False
        self._launch_direction: int = 1
        self._spawn_real_ball()

    @property
    def balls(self) -> list[Ball]:
        return self._balls

    def _spawn_real_ball(self, direction: int = 1) -> Ball:
        ball = Ball(direction=direction, color=WHITE, is_real=True)
        self._balls.append(ball)
        return ball

    def _fragment(self, real_ball: Ball) -> None:
        used_colors: list[tuple[int, int, int]] = [WHITE]
        decoys_to_add = FRAGMENT_COUNT - 1

        for _ in range(decoys_to_add):
            color = _random_decoy_color(used_colors)
            used_colors.append(color)
            direction = 1 if real_ball.vel_x > 0 else -1
            decoy = Ball(direction=direction, color=color, is_real=False)
            decoy.spawn_at(real_ball.x, real_ball.y, direction)
            self._balls.append(decoy)

    def check_fragment_timer(self) -> None:
        if not self._fragment_ready:
            if time.time() - self._last_fragment_time >= FRAGMENT_INTERVAL:
                self._fragment_ready = True

    def update_all(self) -> bool:
        bounced = False
        for ball in self._balls:
            if ball.update():
                bounced = True
        return bounced

    def bounce_all_off_paddle(self, paddle_rect: pygame.Rect) -> bool:
        hit_any = False

        for ball in list(self._balls):
            if ball.bounce_off_paddle(paddle_rect):
                hit_any = True
                if ball.is_real and self._fragment_ready:
                    self._fragment(ball)
                    self._fragment_ready = False
                    self._last_fragment_time = time.time()

        return hit_any

    def check_scoring(self) -> str | None:
        scored: str | None = None
        to_remove: list[Ball] = []

        for ball in self._balls:
            if ball.out_of_bounds_left():
                if ball.is_real:
                    scored = "player2"
                to_remove.append(ball)

            elif ball.out_of_bounds_right():
                if ball.is_real:
                    scored = "player1"
                to_remove.append(ball)

        for ball in to_remove:
            self._balls.remove(ball)

        return scored

    def reset(self, direction: int = 1) -> None:
        self._balls.clear()
        self._fragment_ready = False
        self._last_fragment_time = time.time()
        self._spawn_real_ball(direction=direction)

    def draw_all(self, surface: pygame.Surface) -> None:
        for ball in self._balls:
            ball.draw(surface)