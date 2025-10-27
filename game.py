import pgzrun
from pygame import Rect

# --- CONFIGURAÇÕES ---
WIDTH = 1000
HEIGHT = 700
TITLE = "Fishing Adventure"

# --- ESTADOS ---
game_state = "menu"
sound_on = True
game_started_message = ""

# --- BACKGROUNDS ---
background_menu = Actor("background_menu")
background_game = Actor("background_game")

# --- MENU ---
buttons = {
    "start": Rect((400, 270), (200, 60)),
    "sound": Rect((400, 350), (200, 60)),
    "exit": Rect((400, 430), (200, 60))
}

# --- CONFIGURAÇÕES DO JOGO ---
gravity = 0.5
jump_strength = -10
speed = 5
camera_x = 0
score = 0

platforms = [
    Rect((0, 650), (1200, 50)),
    Rect((300, 550), (150, 20)),
    Rect((500, 480), (150, 20)),
    Rect((750, 450), (150, 20)),
]

# --- CLASSES ---
class Hero(Actor):
    def __init__(self, pos):
        super().__init__("hero_idle", pos)
        self.velocity_y = 0
        self.walk_images = ["hero_walk1", "hero_walk2"]
        self.frame = 0
        self.frame_timer = 0
        self.is_jumping = False

    def update(self):
        moving = False
        on_ground = False

        # Movimentos
        if keyboard.left and self.x > 50:
            self.x -= speed
            self.flip_x = True
            moving = True
        if keyboard.right:
            self.x += speed
            self.flip_x = False
            moving = True

        # Gravidade
        self.velocity_y += gravity
        self.y += self.velocity_y

        # Colisão com plataformas
        for plat in platforms:
            plat_screen = plat.move(-camera_x, 0)
            if self.colliderect(plat_screen) and self.velocity_y >= 0:
                self.bottom = plat_screen.top
                self.velocity_y = 0
                on_ground = True
                self.is_jumping = False

        # Pular
        if keyboard.space and on_ground:
            if sound_on: sounds.jump.play() 
            self.velocity_y = jump_strength
            self.image = "hero_jump"
            self.is_jumping = True

        # Animação
        if moving and not self.is_jumping:
            self.frame_timer += 1
            if self.frame_timer >= 10:
                self.frame_timer = 0
                self.frame = (self.frame + 1) % len(self.walk_images)
                self.image = self.walk_images[self.frame]
        elif not moving and not self.is_jumping:
            self.image = "hero_idle"


class Enemy:
    def __init__(self, images, pos, patrol_range=50, speed=2):
        self.images = images
        self.actor = Actor(images[0], pos)
        self.frame = 0
        self.frame_timer = 0
        self.start_x, self.start_y = pos
        self.direction = 1
        self.patrol_range = patrol_range
        self.speed = speed

    def update(self):
        global camera_x
        # Animação simples
        self.frame_timer += 1
        if self.frame_timer % 15 == 0:
            self.frame = (self.frame + 1) % len(self.images)
            self.actor.image = self.images[self.frame]

        # Movimento de patrulha limitado
        new_x = self.actor.x + self.direction * self.speed
        if new_x > self.start_x + self.patrol_range:
            self.direction = -1
            new_x = self.start_x + self.patrol_range
        elif new_x < self.start_x - self.patrol_range:
            self.direction = 1
            new_x = self.start_x - self.patrol_range

        self.actor.x = new_x
        self.actor.pos = (self.actor.x - camera_x, self.start_y)

    def check_collision(self, hero):
        return hero.colliderect(self.actor)


class Coin:
    def __init__(self, pos):
        self.actor = Actor("coin", pos)
        self.base_x, self.base_y = pos
        self.collected = False

    def update(self):
        if not self.collected:
            self.actor.pos = (self.base_x - camera_x, self.base_y)
        else:
            self.actor.pos = (-100, -100) 

    def check_collision(self, hero):
        return hero.colliderect(self.actor)


# --- INSTÂNCIAS ---
hero = Hero((100, 300))

enemies = [
    Enemy(["claw1", "claw2"], (315, 620)),
    Enemy(["claw1", "claw2"], (565, 620)),
    Enemy(["claw1", "claw2"], (815, 620)),
]

coins = [
    Coin((280, 420)),
    Coin((600, 350)),
    Coin((900, 300)),
]

# --- FUNÇÃO DE RESET ---
def reset_game():
    global camera_x, score, game_state
    hero.pos = (100, 300)
    hero.velocity_y = 0
    hero.is_jumping = False
    score = 0
    camera_x = 0
    for coin in coins:
        coin.collected = False
    game_state = "playing"


# --- DESENHO ---
def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_playing()
    elif game_state == "won":
        screen.draw.text("VOCÊ VENCEU!", center=(WIDTH // 2, HEIGHT // 2),
                         fontsize=80, color="yellow")


def draw_menu():
    background_menu.draw()
    for name, rect in buttons.items():
        screen.draw.filled_rect(rect, (0, 0, 100))
        screen.draw.rect(rect, "white")
        if name == "start":
            text = "Start Game"
        elif name == "sound":
            text = f"Sound: {'On' if sound_on else 'Off'}"
        elif name == "exit":
            text = "Exit"
        screen.draw.text(text, center=rect.center, fontsize=35, color="white")


def draw_playing():
    background_game.draw()

    for plat in platforms:
        screen.draw.filled_rect(plat.move(-camera_x, 0), (139, 69, 19))

    for enemy in enemies:
        enemy.actor.draw()

    for coin in coins:
        coin.actor.draw()

    hero.draw()
    screen.draw.text(f"Score: {score}", topright=(WIDTH - 20, 20), fontsize=35, color="white")
    if game_started_message:
        screen.draw.text(game_started_message, center=(WIDTH // 2, 50), fontsize=40, color="yellow")


# --- CLIQUE DO MOUSE ---
def on_mouse_down(pos):
    global game_state, sound_on, game_started_message
    if game_state == "menu":
        if buttons["start"].collidepoint(pos):
            if sound_on: sounds.click.play()
            game_state = "playing"
            game_started_message = "Use as setas para mover e espaço para pular."
        elif buttons["sound"].collidepoint(pos):
            if sound_on: sounds.click.play()
            sound_on = not sound_on
            if sound_on:
                music.unpause()
            else:
                music.pause()
        elif buttons["exit"].collidepoint(pos):
            if sound_on: sounds.click.play()
            exit()


# --- ATUALIZAÇÃO ---
def update():
    global camera_x, score, game_state, game_started_message
    if game_state != "playing":
        return

    hero.update()

    for enemy in enemies:
        enemy.update()
        if enemy.check_collision(hero):
            if sound_on: sounds.hit.play() 
            reset_game()
            game_started_message = " "
            return

    for coin in coins:
        coin.update()
        # Modificado para tocar o som apenas uma vez
        if coin.check_collision(hero) and not coin.collected:
            if sound_on: sounds.coin.play() 
            coin.collected = True
            score += 10

    # Verifica vitória
    if score >= 30:
        game_state = "won"
        game_started_message = "Você venceu!"
        if sound_on:
            sounds.win.play()

    camera_x = hero.x - WIDTH // 2
    if camera_x < 0:
        camera_x = 0


# --- MÚSICA ---
music.play("bg_music")
music.set_volume(0.5)
if not sound_on:
    music.pause()


pgzrun.go()