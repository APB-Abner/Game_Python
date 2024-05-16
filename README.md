# Corrida de Fórmula E - Jogo em Python

Este projeto é um jogo de corrida estilo Subway Surfers em desenvolvimento usando Python com a biblioteca Pygame. O jogador controla um carro de Fórmula E que deve evitar obstáculos e coletar pads para ativar um boost de velocidade.

## Funcionalidades

- **Controle do Carro:** O jogador pode mover o carro para a esquerda e para a direita usando as teclas de seta.
- **Obstáculos Aleatórios:** Obstáculos são gerados de forma procedural e aleatória na pista.
- **Colisão:** O jogo detecta colisões entre o carro e os obstáculos, resultando no fim do jogo.
- **Boost de Velocidade:** O jogador pode coletar pads para ativar um boost de velocidade por um tempo limitado.
- **Aumento de Dificuldade:** A velocidade dos obstáculos aumenta em 15% a cada 20 segundos.
- **Rolagem Infinita:** A pista de corrida rola infinitamente, proporcionando uma experiência de jogo contínua.

## Como Jogar

1. **Movimentação:**
   - Use a tecla `←` (seta esquerda) para mover o carro para a esquerda.
   - Use a tecla `→` (seta direita) para mover o carro para a direita.

2. **Coletar Pads:**
   - Colete pads que aparecem na pista para acumular boosts.

3. **Ativar Boost:**
   - Pressione a barra de espaço (`SPACE`) para ativar o boost de velocidade após coletar três pads.

## Estrutura do Código

### game_loop()

A função principal que gerencia o loop do jogo. Contém a lógica para desenhar e atualizar a tela, gerenciar entradas do jogador, movimentar obstáculos e pads, e verificar colisões.

### car(x, y)

Desenha o carro na posição especificada `(x, y)`.

### obstacles(obst_x, obst_y, obstacle_image)

Desenha um obstáculo na posição especificada `(obst_x, obst_y)` usando a imagem fornecida.

### pad(x, y)

Desenha um pad na posição especificada `(x, y)`.

### is_collision(car_x, car_y, obst_x, obst_y, obst_width, obst_height)

Verifica se há uma colisão entre o carro e um obstáculo ou pad.

### draw_background(y1, y2)

Desenha duas instâncias da imagem de fundo para criar o efeito de rolagem infinita.

## Requisitos

- Python 3.x
- Pygame

## Instalação

1. Clone este repositório:
   ```sh
   git clone https://github.com/APB-Abner/Game_Python.git
   ```
2. Navegue até o diretório do projeto:
   ```sh
   cd Game_Python
   ```
3. Instale as dependências:
   ```sh
   pip install pygame
   ```

## Como Executar

1. Execute o script do jogo:
   ```sh
   python teste_game.py
   ```

