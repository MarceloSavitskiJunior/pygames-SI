import pygame

pygame.mixer.init()

_sound_score = pygame.mixer.Sound("sounds/olhamensagem.mp3")
_sound_final = pygame.mixer.Sound("sounds/a-risada-do-kiko.mp3")
_sound_track = pygame.mixer.Sound("sounds/cala-boca-e-escuta-o-som-do-meu-corsa.mp3")
_sound_paddle = pygame.mixer.Sound("sounds/discord-notification.mp3")

def play_sfx() -> None:
  pygame.mixer.music.set_volume(0.5)
  _sound_score.play()

def play_paddle_sfx() -> None:
  pygame.mixer.music.set_volume(0.5)
  _sound_paddle.play()

def play_final_game_sfx() -> None:
    _sound_final.play()

def play_sound_track() -> None:
  pygame.mixer.music.load("sounds/cala-boca-e-escuta-o-som-do-meu-corsa.mp3")
  pygame.mixer.music.set_volume(0.5)
  pygame.mixer.music.play(-1)

def stop_soundtrack():
  pygame.mixer.music.stop()