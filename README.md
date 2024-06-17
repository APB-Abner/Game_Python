# Corrida de Fórmula E - Jogo em Python

Este é um jogo de corrida desenvolvido em Python usando a biblioteca Pygame. O jogador controla um carro que deve evitar obstáculos, coletar pads de aceleração e lidar com obstáculos que reduzem a velocidade.

## Índice

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Estrutura do Código](#estrutura-do-código)
  - [Classes](#classes)
  - [Funções Auxiliares](#funções-auxiliares)
  - [Arquivos](#arquivos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Como Jogar](#como-jogar)
  - [Controles](#controles)
  - [Menus](#menus)
    - [Menu de Pausa](#menu-de-pausa)
    - [Menu de Opções](#menu-de-opções)
- [Contribuições](#contribuições)
- [Autores](#autores)
- [Licença](#licença)

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

## Requisitos

- Python 3.x
- Pygame

## Estrutura do Código

O código está organizado em vários arquivos para facilitar a manutenção e a legibilidade. Aqui está uma visão geral dos principais arquivos e classes:

### Classes

#### `GameLogic`

A classe `GameLogic` contém a lógica principal do jogo. Ela gerencia a posição do carro, a posição e movimento dos obstáculos e pads, a velocidade do jogo, e as colisões. Também gerencia o menu de pausa e opções.

- **Atributos:**
  - `car_x`, `car_y`: Posição do carro.
  - `obst_startx`, `obst_starty`: Posição inicial dos obstáculos.
  - `pad_startx`, `pad_starty`: Posição inicial dos pads.
  - `speed_basic`, `speed_boost`, `speed_slow`: Velocidades diferentes para o jogo.
  - `distance`: Distância percorrida pelo carro.

- **Métodos:**
  - **`__init__()`**: Inicializa as variáveis do jogo, como a posição do carro, velocidade, posições e velocidades dos obstáculos e pads, e inicializa a animação e spritesheet.
  - **`main_loop(screen)`**: Loop principal do jogo. Gerencia os eventos, atualiza as posições dos objetos, verifica colisões, e renderiza a tela.
  - **`reset()`**: Reseta o estado do jogo para as configurações iniciais.
  - **`reset_obstacle()`**: Reseta a posição e escala de um obstáculo.
  - **`reset_pad()`**: Reseta a posição e escala de um pad.
  - **`reset_slow_obstacle()`**: Reseta a posição e escala de um obstáculo de redução de velocidade.
  - **`render(screen, boost_active)`**: Renderiza os elementos do jogo na tela.
  - **`collision_check(x1, y1, car, x2, y2, obstacle, scale)`**: Verifica a colisão entre o carro e um obstáculo ou pad.
  - **`pause_menu(screen)`**: Exibe o menu de pausa e gerencia a lógica de pausa.
  - **`options_menu(screen)`**: Exibe o menu de opções e gerencia as configurações do jogo, como resolução, volume, e linguagem.
  - **`draw_transparent_background(screen, alpha)`**: Desenha um fundo transparente na tela.
  - **`draw_text(text, font, color, surface, x, y)`**: Desenha texto na tela.

#### `Renderer`

Responsável por desenhar elementos na tela, incluindo o carro, obstáculos, pads e animações.

#### `Animation`

Gerencia a animação da pista, criando um efeito de rolagem infinita.

#### `Menu`

A classe `Menu` gerencia a interface do menu principal do jogo, incluindo as opções de iniciar o jogo e sair.

- **Métodos:**
  - **`__init__()`**: Inicializa as variáveis de volume e estado das opções.
  - **`draw_transparent_background(screen, alpha)`**: Desenha um fundo transparente na tela do menu.
  - **`draw_text(text, font, color, surface, x, y)`**: Desenha texto na tela do menu.
  - **`main_menu(screen, name_player)`**: Gerencia o loop do menu principal, exibindo botões e respondendo a eventos do usuário.

### Funções Auxiliares

Além da `GameLogic` e `Menu`, o código utiliza várias funções e classes de módulos importados para desenhar botões, gerenciar gráficos, e gerenciar pontuações.

- **Módulo `buttons`**: Contém funções para desenhar botões e gerenciar as opções do jogo.
- **Módulo `graphics`**: Contém funções para renderizar gráficos, textos, animações, e gerenciar a interface de usuário.
- **Módulo `sprite`**: Contém definições de sprites para o carro, obstáculos, e pads.
- **Módulo `score_manager`**: Contém funções para salvar e recuperar pontuações.
  - `save_score(score)`: Salva a pontuação atual em um arquivo JSON.
  - `get_high_score()`: Retorna a maior pontuação salva.
  - `display_scores(screen)`: Exibe as 5 melhores pontuações na tela.

### Arquivos

- `main.py`: Arquivo principal que inicia o jogo.
- `config.py`: Contém constantes e configurações globais, como dimensões da tela, limites da pista e cores.
- `buttons.py`: Funções para desenhar e gerenciar botões.
- `graphics.py`: Contém classes e funções relacionadas ao renderização, animações e exibição de textos.
- `sprite.py`: Contém a inicialização de sprites e máscaras para colisão.
- `score_manager.py`: Gerenciamento de pontuações.
- `game_logic.py`: Contém a lógica principal do jogo, incluindo o loop do jogo, controle do carro, movimentação de obstáculos, detecção de colisões e gerenciamento de pontuações.

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

## Uso

Para iniciar o jogo, execute o arquivo principal:

```bash
python main.py
```

## Como Jogar

### Controles

1. **Movimentação:**
   - Use a tecla `←` (seta esquerda) para mover o carro para a esquerda.
   - Use a tecla `→` (seta direita) para mover o carro para a direita.

2. **Coletar Pads:**
   - Colete pads que aparecem na pista para acumular boosts.

3. **Ativar Boost:**
   - Pressione a barra de espaço (`SPACE`) para ativar o boost de velocidade (requer 3 pads coletados).

4. **Pausar Jogo:**
   - Pressione a tecla `P` ou `ESC` para pausar o jogo.

5. **Reiniciar após Colisão:**
   - Pressione `R` para reiniciar o jogo após uma colisão.
   - Pressione `Q` para sair do jogo após uma colisão.

### Menus

#### Menu de Pausa

No menu de pausa, você pode:

- **Continuar:** Continuar jogando
- **Opções:** Abrir o menu de opções
- **Sair:** Sair do jogo

#### Menu de Opções

No menu de opções ainda não é possível fazer nada!

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

1. Faça um fork do projeto
2. Crie sua feature branch (`git checkout -b minha-nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça um push para a branch (`git push origin minha-nova-feature`)
5. Abra um pull request

## Autores

- **Abner de Paiva Barbosa**: RM 558468
- **Beatriz Vieira de Novais**: RM 554746
- **Fernando Luiz Silva Antonio**: RM 555201
- **Mariana Neugebauer Dourado**: RM 550494
- **Thomas de Almeida Reichmann**: RM 554812

## Licença

Este projeto está licenciado sob a licença MIT.
