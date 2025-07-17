import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Juego de disparos a esferas")

# Colores que usaremos
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Reloj para controlar los FPS
clock = pygame.time.Clock()
FPS = 60

# Jugador (una bola azul)
player_radius = 20
player_x = screen_width // 2
player_y = screen_height // 2
player_speed = 5

# Lista para guardar los disparos
bullets = []  # Cada bala será un diccionario con x, y, dx, dy y radio

# Lista para guardar los objetivos (esferas enemigas)
targets = []  # Cada objetivo será un diccionario con x, y, dx, dy y radio

# Crear objetivos al inicio
for _ in range(10):
    # Posición aleatoria lejos del centro (jugador)
    while True:
        target_x = random.randint(0, screen_width)
        target_y = random.randint(0, screen_height)
        distance = math.hypot(target_x - player_x, target_y - player_y)
        if distance > 150:
            break
    target_dx = random.choice([-2, -1, 1, 2])
    target_dy = random.choice([-2, -1, 1, 2])
    target_radius = 15
    targets.append({"x": target_x, "y": target_y, "dx": target_dx, "dy": target_dy, "radius": target_radius})

# Función para dibujar al jugador
def draw_player():
    pygame.draw.circle(screen, BLUE, (player_x, player_y), player_radius)

# Función para dibujar los objetivos
def draw_targets():
    for target in targets:
        pygame.draw.circle(screen, RED, (int(target["x"]), int(target["y"])), target["radius"])

# Función para dibujar los disparos
def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, BLACK, (int(bullet["x"]), int(bullet["y"])), bullet["radius"])

# Función para mover los disparos
def move_bullets():
    for bullet in bullets:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]

# Función para mover los objetivos
def move_targets():
    for target in targets:
        target["x"] += target["dx"]
        target["y"] += target["dy"]

        # Hacer que reboten si tocan los bordes
        if target["x"] - target["radius"] <= 0 or target["x"] + target["radius"] >= screen_width:
            target["dx"] *= -1
        if target["y"] - target["radius"] <= 0 or target["y"] + target["radius"] >= screen_height:
            target["dy"] *= -1

# Función para verificar colisiones entre balas y objetivos
def check_collisions():
    global targets
    new_targets = []
    for target in targets:
        hit = False
        for bullet in bullets:
            dist = math.hypot(bullet["x"] - target["x"], bullet["y"] - target["y"])
            if dist < bullet["radius"] + target["radius"]:
                hit = True
                break
        if not hit:
            new_targets.append(target)
    return new_targets

# Bucle principal del juego
running = True
while running:
    screen.fill(WHITE)  # Poner fondo blanco

    # Detectar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Disparo con clic izquierdo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
            bullet_speed = 10
            bullet_dx = bullet_speed * math.cos(angle)
            bullet_dy = bullet_speed * math.sin(angle)
            bullets.append({"x": player_x, "y": player_y, "dx": bullet_dx, "dy": bullet_dy, "radius": 8})

    # Movimiento con teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    # Actualizar posiciones
    move_bullets()
    move_targets()

    # Verificar colisiones
    targets = check_collisions()

    # Dibujar todo
    draw_player()
    draw_bullets()
    draw_targets()

    # Verificar si ganaste
    if not targets:
        font = pygame.font.SysFont(None, 60)
        text = font.render("¡Ganaste!", True, BLACK)
        screen.blit(text, (screen_width // 2 - 100, screen_height // 2 - 30))

    # Mostrar pantalla actualizada
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()



