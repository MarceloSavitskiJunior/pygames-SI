# Efeito do DvD

Simulação estilo "DVD screensaver" onde os nomes **Marcelo** e **Rafael** ficam ricocheteando pelas bordas da tela e se repelem ao colidir.

## Requisitos

- Python 3.x
- pygame

```bash
pip install pygame
```

## Como rodar

```bash
python3 teste-pygame.py
```

Pressione **ESC** ou feche a janela para sair.

---

## Estrutura do código

### Configuração inicial

```python
WIDTH = 800
HEIGHT = 600
FONT_SIZE = 60
```

A tela tem 800×600 pixels. O tamanho da fonte afeta diretamente o tamanho dos retângulos de colisão, então mudar esse valor altera o comportamento físico também.

---

### `random_color()`

Retorna uma tupla RGB com valores aleatórios entre 80 e 255. O mínimo de 80 evita cores muito escuras que seriam difíceis de ver no fundo escuro.

---

### `random_velocity(speed=3)`

Retorna uma velocidade `(vx, vy)` onde cada componente é `+speed` ou `-speed`, escolhido aleatoriamente. Isso garante que os objetos sempre comecem em movimento diagonal.

---

### Classe `NameObject`

Representa um nome na tela. Cada instância carrega:

- `name` — o texto exibido
- `color` — cor atual do texto
- `surface` — a superfície pygame renderizada com o texto
- `rect` — o retângulo de posição e tamanho, usado para movimento e colisão
- `vx`, `vy` — velocidade nos eixos X e Y

**`recolor()`** — gera uma nova cor aleatória e re-renderiza o texto. É chamado toda vez que o objeto bate em algo.

**`update()`** — move o objeto somando a velocidade à posição a cada frame. Depois verifica se alguma borda foi ultrapassada e corrige:

- Se saiu pela direita → empurra de volta e inverte `vx` para negativo
- Se saiu pela esquerda → empurra de volta e torna `vx` positivo
- Mesma lógica para cima e baixo com `vy`

Em cada colisão com parede, `recolor()` é chamado.

**`draw(surface)`** — desenha o texto na posição atual usando `blit`.

---

### `handle_collisions(objects)`

Percorre todos os pares possíveis de objetos. Se dois retângulos se sobrepõem (`colliderect`), as velocidades são trocadas entre eles — simulando uma colisão elástica simples. Depois de trocar, cada objeto dá um passo na nova direção para separá-los e evitar que fiquem "grudados". Ambos também trocam de cor.

---

### Loop principal

```python
while running:
    clock.tick(60)        # limita a 60 FPS
    screen.fill(DARK_BG)  # limpa a tela
    for obj in objects:
        obj.update()      # move e verifica paredes
    handle_collisions(objects)
    for obj in objects:
        obj.draw(screen)  # desenha
    pygame.display.flip() # atualiza a tela
```

Os dois objetos são criados em posições opostas da tela antes do loop:

```python
objects = [
    NameObject("Marcelo", WIDTH // 3, HEIGHT // 2),
    NameObject("Rafael",  2 * WIDTH // 3, HEIGHT // 2),
]
```

---