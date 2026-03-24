import sys
from enum import Enum, auto

import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    PADDLE_MARGIN, PADDLE_WIDTH,
)
from models.ball import Ball
from models.paddle import Paddle
from models.scoreboard import Scoreboard
from models.ai_controller import AIController
from models.renderer import Renderer
from sounds.sound import play_sfx, play_final_game_sfx, play_sound_track, play_paddle_sfx, stop_soundtrack

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    VICTORY = auto()
    QUIT = auto()


class Game:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.ai = AIController()

        self.ball: Ball | None = None
        self.paddle1: Paddle | None = None
        self.paddle2: Paddle | None = None
        self.scoreboard: Scoreboard | None = None

    def _create_entities(self) -> None:
        self.ball = Ball()
        self.paddle1 = Paddle(x=PADDLE_MARGIN)
        self.paddle2 = Paddle(x=SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH)
        self.scoreboard = Scoreboard()

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def _quit(self) -> None:
        pygame.quit()
        sys.exit()

    def _handle_player1_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.paddle1.move_up()
        if keys[pygame.K_DOWN]:
            self.paddle1.move_down()

    def _scene_menu(self) -> GameState:
        while True:
            if not self._handle_events():
                return GameState.QUIT

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return GameState.PLAYING

            self.renderer.draw_menu()
            pygame.display.flip()
            self.clock.tick(FPS)

    def _scene_game(self) -> tuple[GameState, str]:
        self._create_entities()
        play_sound_track()

        while True:
            if not self._handle_events():
                return GameState.QUIT, ""

            self._handle_player1_input()
            self.ai.update(self.paddle2, self.ball)

            self.ball.update()
            self.ball.bounce_off_paddle(self.paddle1.rect)
            self.ball.bounce_off_paddle(self.paddle2.rect)

            if self.ball.out_of_bounds_left():
                self.scoreboard.score_player2()
                play_sfx()
                self.ball.reset(direction=1)

            if self.ball.out_of_bounds_right():
                self.scoreboard.score_player1()
                play_sfx()
                self.ball.reset(direction=-1)

            winner = self.scoreboard.get_winner()
            if winner:
                return GameState.VICTORY, winner

            self.renderer.draw_game(
                self.ball, self.paddle1, self.paddle2, self.scoreboard
            )
            pygame.display.flip()
            self.clock.tick(FPS)

    def _scene_victory(self, winner: str) -> GameState:
        play_final_game_sfx()  # toca uma vez aqui

        while True:
            if not self._handle_events():
                return GameState.QUIT

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return GameState.PLAYING
            if keys[pygame.K_ESCAPE]:
                return GameState.MENU

            self.renderer.draw_victory(winner)
            pygame.display.flip()
            self.clock.tick(FPS)

    def run(self) -> None:
        state = GameState.MENU

        while state != GameState.QUIT:
            if state == GameState.MENU:
                state = self._scene_menu()

            elif state == GameState.PLAYING:
                state, winner = self._scene_game()
                if state == GameState.VICTORY:
                    state = self._scene_victory(winner)

        self._quit()