# Corrida de Fórmula E - Jogo em Python

Este projeto é um jogo de corrida estilo Subway Surfers em desenvolvimento usando Python com a biblioteca Pygame. O jogador controla um carro de Fórmula E que deve evitar obstáculos e coletar pads para ativar um boost de velocidade.

## Funcionalidades

- **Controle do Carro:** O jogador pode mover o carro para a esquerda e para a direita usando as teclas de seta.
- **Obstáculos Aleatórios:** Obstáculos são gerados de forma procedural e aleatória na pista.
- **Colisão:** O jogo detecta colisões entre o carro e os obstáculos, resultando no fim do jogo.
- **Boost de Velocidade:** O jogador pode coletar pads para ativar um boost de velocidade por um tempo limitado.
- **Aumento de Dificuldade:** A velocidade dos obstáculos aumenta em 15% a cada 20 segundos.
- **Rolagem Infinita:** A pista de corrida rola infinitamente, proporcionando uma experiência de jogo contínua.
- **Pontuações Salvas:** As pontuações são salvas em um arquivo para que o jogador possa ver seu progresso e recordes.
- **Menu de Pausa:** O jogo pode ser pausado, e o jogador pode ver suas pontuações durante a pausa.
- **Início com Atraso:** O jogo começa com um atraso de 3 segundos para que os obstáculos não apareçam imediatamente.

## Como Jogar

1. **Movimentação:**
   - Use a tecla `←` (seta esquerda) para mover o carro para a esquerda.
   - Use a tecla `→` (seta direita) para mover o carro para a direita.

2. **Coletar Pads:**
   - Colete pads que aparecem na pista para acumular boosts.

3. **Ativar Boost:**
   - Pressione a barra de espaço (`SPACE`) para ativar o boost de velocidade após coletar três pads.

4. **Pausar Jogo:**
   - Pressione a tecla `P` para pausar o jogo.

5. **Reiniciar após Colisão:**
   - Pressione `R` para reiniciar o jogo após uma colisão.
   - Pressione `Q` para sair do jogo após uma colisão.

## Estrutura do Código

O código está organizado em vários arquivos para facilitar a manutenção e a legibilidade. Aqui está uma visão geral dos principais arquivos e classes:

### Arquivos

- `game_logic.py`: Contém a lógica principal do jogo, incluindo o loop do jogo, controle do carro, movimentação de obstáculos, detecção de colisões e gerenciamento de pontuações.
- `config.py`: Contém constantes e configurações globais, como dimensões da tela, limites da pista e cores.
- `graphics.py`: Contém classes e funções relacionadas ao renderização, animações e exibição de textos.
- `sprite.py`: Contém a inicialização de sprites e máscaras para colisão.

### Classes

#### `GameLogic`
Responsável por gerenciar o estado do jogo, detectar colisões, atualizar a posição do carro e dos obstáculos, e lidar com eventos do jogador.

- **Atributos:**
  - `car_x`, `car_y`: Posição do carro.
  - `obst_startx`, `obst_starty`: Posição inicial dos obstáculos.
  - `pad_startx`, `pad_starty`: Posição inicial dos pads.
  - `speed_basic`, `speed_boost`, `speed_slow`: Velocidades diferentes para o jogo.
  - `distance`: Distância percorrida pelo carro.

- **Métodos:**
  - `__init__()`: Inicializa o estado do jogo.
  - `main_loop()`: Loop principal do jogo.
  - `reset()`: Reseta o estado do jogo após uma colisão.
  - `crash()`: Exibe a tela de "Game Over".
  - `render()`: Renderiza os elementos na tela.
  - `collision_check()`: Verifica colisões entre o carro e os obstáculos/pads.

#### `Renderer`
Responsável por desenhar elementos na tela, incluindo o carro, obstáculos, pads e animações.

#### `Animation`
Gerencia a animação da pista, criando um efeito de rolagem infinita.

### Funções Auxiliares

- `save_score(score)`: Salva a pontuação atual em um arquivo JSON.
- `get_high_score()`: Retorna a maior pontuação salva.
- `display_scores(screen)`: Exibe as 5 melhores pontuações na tela.

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

