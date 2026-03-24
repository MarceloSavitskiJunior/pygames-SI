import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GRAY
from models.ball import Ball
from models.paddle import Paddle
from models.scoreboard import Scoreboard

_BLINK_PERIOD_MS = 2000
_BLINK_ON_MS = 1000


class Renderer:

    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.font_score = pygame.font.SysFont(None, 48)
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 28)

    def _clear(self) -> None:
        self.surface.fill(BLACK)

    def _draw_center_line(self) -> None:
        segment_h = 20
        gap = 10
        x = SCREEN_WIDTH // 2 - 2
        for y in range(0, SCREEN_HEIGHT, segment_h + gap):
            pygame.draw.rect(self.surface, GRAY, (x, y, 4, segment_h))

    def _draw_scoreboard(self, scoreboard: Scoreboard) -> None:
        text = self.font_score.render(
            f"{scoreboard.player1_score}   {scoreboard.player2_score}",
            True,
            WHITE,
        )
        self.surface.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 30)))

    def draw_game(
        self,
        ball: Ball,
        paddle1: Paddle,
        paddle2: Paddle,
        scoreboard: Scoreboard,
    ) -> None:
        self._clear()
        self._draw_center_line()
        paddle1.draw(self.surface)
        paddle2.draw(self.surface)
        ball.draw(self.surface)
        self._draw_scoreboard(scoreboard)

    def draw_menu(self) -> None:
        self._clear()

        title = self.font_title.render("PONG", True, WHITE)
        self.surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

        controls = self.font_small.render(
            "Player 1: Arrow Keys  |  Player 2: AI", True, GRAY
        )
        self.surface.blit(controls, controls.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if pygame.time.get_ticks() % _BLINK_PERIOD_MS < _BLINK_ON_MS:
            prompt = self.font_small.render("Press SPACE to play", True, WHITE)
            self.surface.blit(
                prompt,
                prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)),
            )

    def draw_victory(self, winner: str) -> None:
        self._clear()

        title = self.font_title.render(f"{winner} wins!", True, WHITE)
        self.surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))

        replay = self.font_medium.render("SPACE — Play again", True, GRAY)
        menu = self.font_medium.render("ESC — Main menu", True, GRAY)
        self.surface.blit(replay, replay.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))
        self.surface.blit(menu, menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)))