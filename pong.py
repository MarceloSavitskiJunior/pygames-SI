import pygame
import sys
import random

pygame.init()
small_font = pygame.font.SysFont(None, 24)

PRETO=(0, 0, 0)
BRANCO=(255, 255, 255)

LARGURA=800
ALTURA=600

player_1_score = 0
player_2_score = 0

tela=pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
clock=pygame.time.Clock()

raquete_largura=10
raquete_altura=90
tamanho_bola=10

player1_x=15
player1_y=ALTURA//2 - raquete_altura//2

player2_x=LARGURA - 15 - raquete_largura
player2_y=ALTURA//2 - raquete_altura//2

bola_x = LARGURA // 2 - tamanho_bola // 2
bola_y = ALTURA // 2 - tamanho_bola // 2

bola_vx = 5
bola_vy = random.random()

bola_x += bola_vx
bola_y += bola_vy

rodando = False
def menu_principal():
    global rodando
    rodando_menu = True
    while rodando_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando_menu = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                rodando_menu = False

        tela.fill(PRETO)
        tempo = pygame.time.get_ticks()
        if tempo % 2000 < 1000:
            text_blynk = small_font.render("Presione ENTER para jogar", True, BRANCO)
            text_blynk_rect = text_blynk.get_rect(center=(LARGURA // 2, ALTURA // 2))
            tela.blit(text_blynk, text_blynk_rect)
        pygame.display.flip()
        clock.tick(60)

menu_principal()

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tela.fill(PRETO)

    bola_x += bola_vx
    bola_y += bola_vy

    pygame.draw.rect(tela, BRANCO, (
        player1_x, 
        player1_y, 
        raquete_largura, 
        raquete_altura
        ))

    pygame.draw.rect(tela, BRANCO, (
        player2_x, 
        player2_y, 
        raquete_largura, 
        raquete_altura
        ))
    hud = small_font.render(f"{player_1_score} ---------------- {player_2_score}", True, (180, 180, 200))
    tela.blit(hud, (10, 10))

    pygame.draw.circle(tela, BRANCO, (bola_x, bola_y), tamanho_bola)

    if (bola_y <= 0 + tamanho_bola //2 or bola_y >= ALTURA - tamanho_bola //2):
        bola_vy *= -1
    if (bola_x >= LARGURA):
        player_1_score += 1
        bola_x = LARGURA // 2 - tamanho_bola // 2
        bola_y = ALTURA // 2 - tamanho_bola // 2
        bola_vx = -bola_vx
    elif (bola_x <= 0):
        player_2_score += 1
        bola_x = LARGURA // 2 - tamanho_bola // 2
        bola_y = ALTURA // 2 - tamanho_bola // 2
        bola_vx = -bola_vx

    if (bola_x <= player1_x + raquete_largura and player1_y <= bola_y <= player1_y + raquete_altura):
        bola_vx = -bola_vx
        if (bola_y < player1_y + raquete_altura // 3):
            bola_vy -= 2
        elif (bola_y > player1_y + 2 * raquete_altura // 3):
            bola_vy += 2
    if (bola_x >= player2_x - tamanho_bola and player2_y <= bola_y <= player2_y + raquete_altura):
        bola_vx = -bola_vx
        if (bola_y < player1_y + raquete_altura // 3):
            bola_vy -= 2
        elif (bola_y > player1_y + 2 * raquete_altura // 3):
            bola_vy += 2

    player2_y += (bola_y - (player2_y + raquete_altura // 2)) * 0.2

    if (pygame.key.get_pressed()[pygame.K_w] and player1_y > 0):
        player1_y -= 10
    if (pygame.key.get_pressed()[pygame.K_s] and player1_y < ALTURA - raquete_altura):
        player1_y += 10
    if (pygame.key.get_pressed()[pygame.K_UP] and player2_y > 0):
        player2_y -= 10
    if (pygame.key.get_pressed()[pygame.K_DOWN] and player2_y < ALTURA - raquete_altura):
        player2_y += 10

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()