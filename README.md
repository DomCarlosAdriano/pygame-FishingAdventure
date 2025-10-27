# 🎣 Fishing Adventure

**Fishing Adventure** é um jogo de plataforma 2D desenvolvido em Python utilizando a **biblioteca Pygame Zero**. Criei este jogo como parte de um desafio técnico, no qual tive apenas 48 horas para completá-lo. Apesar de não conhecer a biblioteca previamente, consegui finalizar o projeto dentro do prazo, atendendo a todos os requisitos técnicos solicitados.

O jogo é **propositalmente simples**, criado para demonstrar minha habilidade com Python e Pygame Zero, sem a necessidade de ser complexo ou revolucionário. Nele, o jogador controla um herói que deve coletar moedas, evitar inimigos e saltar sobre plataformas para alcançar a vitória.

---

## 📌 Funcionalidades

- **Menu Interativo**
  - Iniciar o jogo
  - Ativar/desativar som
  - Sair do jogo
- **Controle do Herói**
  - Movimentação lateral: setas esquerda/direita
  - Pulo: barra de espaço
  - Animação de caminhada e pulo
- **Inimigos**
  - Movimentação de patrulha horizontal limitada
  - Colisão reinicia o jogo
- **Moedas**
  - Coletáveis, cada moeda vale 10 pontos
  - Som ao coletar
- **Plataformas**
  - Diferentes alturas para desafios
  - Colisão com plataformas permite saltos
- **Pontuação**
  - Vitória ao atingir 30 pontos
- **Sons e Música**
  - Música de fundo
  - Sons de pulo, coleta, hit e vitória
  - Botão no menu para ligar/desligar som
- **Câmera**
  - Segue o herói horizontalmente
  - Limite no início da tela

---

## 🎮 Como Jogar

1. Abra o jogo com Python e Pygame Zero:
   ```bash
   pgzrun game.py

### No menu:
- **Start Game**: inicia o jogo
- **Sound**: liga/desliga o som
- **Exit**: fecha o jogo

### Durante o jogo:
- **Setas esquerda/direita**: mover o herói
- **Barra de espaço**: pular
- **Colete moedas** para aumentar a pontuação
- **Evite inimigos**: colisão reinicia o jogo
- **Objetivo**: atingir 30 pontos para vencer

---

## 🛠️ Estrutura do Código

- **main.py**: arquivo principal com toda a lógica do jogo

### Classes:
- **Hero**: personagem principal
- **Enemy**: inimigos patrulhando
- **Coin**: moedas colecionáveis

### Funções Principais:
- `update()`: atualiza movimentos, colisões e pontuação
- `draw()`: desenha todos os elementos na tela
- `on_mouse_down(pos)`: interações do menu
- `reset_game()`: reinicia o jogo

### Variáveis Globais:
- `game_state`: estado do jogo (`menu`, `playing`, `won`)
- `score`: pontuação do jogador
- `camera_x`: posição da câmera
- `sound_on`: controle de som

---

## 🎨 Assets

### Imagens:
- `hero_idle`, `hero_walk1`, `hero_walk2`, `hero_jump`
- `claw1`, `claw2` (inimigos)
- `coin`
- `background_menu`, `background_game`

### Sons:
- `jump`, `coin`, `hit`, `win`, `click`

### Música:
- `bg_music` (loop de fundo)

> Todos os arquivos devem estar nas pastas `images/` e `music/`.

---

## 🖥️ Requisitos

- Python 3.x
- Pygame Zero

Instalação do Pygame Zero:
```bash
pip install pgzero
