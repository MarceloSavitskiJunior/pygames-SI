import sys
from enum import Enum, auto

import pygame

from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    PADDLE_MARGIN, PADDLE_WIDTH,
)
from models.paddle import Paddle
from models.scoreboard import Scoreboard
from models.ai_controller import AIController
from models.renderer import Renderer
from models.ball_manager import BallManager
from sounds.sound import (
    play_sfx,
    play_final_game_sfx,
    play_sound_track,
    play_paddle_sfx,
    stop_soundtrack,
)


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    VICTORY = auto()
    QUIT = auto()


class Game:

    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.ai = AIController()

        self.ball_manager: BallManager | None = None
        self.paddle1: Paddle | None = None
        self.paddle2: Paddle | None = None
        self.scoreboard: Scoreboard | None = None

    def _create_entities(self) -> None:
        self.ball_manager = BallManager()
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

            bm = self.ball_manager

            self._handle_player1_input()
            real_balls = [b for b in bm.balls if b.is_real]
            if real_balls:
                self.ai.update(self.paddle2, real_balls[0])

            bm.check_fragment_timer()

            if bm.update_all():
                play_paddle_sfx()

            if bm.bounce_all_off_paddle(self.paddle1.rect):
                play_paddle_sfx()

            if bm.bounce_all_off_paddle(self.paddle2.rect):
                play_paddle_sfx()

            scored = bm.check_scoring()
            if scored == "player2":
                self.scoreboard.score_player2()
                play_sfx()
                bm.reset(direction=1)
            elif scored == "player1":
                self.scoreboard.score_player1()
                play_sfx()
                bm.reset(direction=-1)

            winner = self.scoreboard.get_winner()
            if winner:
                stop_soundtrack()
                return GameState.VICTORY, winner

            self.renderer.draw_game(
                bm, self.paddle1, self.paddle2, self.scoreboard
            )
            pygame.display.flip()
            self.clock.tick(FPS)

    def _scene_victory(self, winner: str) -> GameState:
        play_final_game_sfx()

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