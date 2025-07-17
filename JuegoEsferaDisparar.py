import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Tamaño de la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dispara a las bolas enemigas")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Reloj para controlar los FPS
reloj = pygame.time.Clock()
FPS = 60

# Jugador (bola azul)
jugador_radio = 20
jugador_x = ANCHO // 2
jugador_y = ALTO // 2
velocidad_jugador = 5

# Lista de balas (cada bala será un diccionario con su posición y velocidad)
balas = []

# Lista de enemigos (cada enemigo es un diccionario)
enemigos = []
for _ in range(10):
    enemigo_x = random.randint(0, ANCHO)
    enemigo_y = random.randint(0, ALTO)
    enemigo_dx = random.choice([-2, -1, 1, 2])
    enemigo_dy = random.choice([-2, -1, 1, 2])
    enemigo_radio = 15
    enemigos.append({
        "x": enemigo_x,
        "y": enemigo_y,
        "dx": enemigo_dx,
        "dy": enemigo_dy,
        "radio": enemigo_radio
    })

# Función para dibujar al jugador
def dibujar_jugador():
    pygame.draw.circle(pantalla, AZUL, (jugador_x, jugador_y), jugador_radio)

# Función para dibujar las balas
def dibujar_balas():
    for bala in balas:
        pygame.draw.circle(pantalla, NEGRO, (int(bala["x"]), int(bala["y"])), bala["radio"])

# Función para dibujar los enemigos
def dibujar_enemigos():
    for enemigo in enemigos:
        pygame.draw.circle(pantalla, ROJO, (int(enemigo["x"]), int(enemigo["y"])), enemigo["radio"])

# Mover balas
def mover_balas():
    for bala in balas:
        bala["x"] += bala["dx"]
        bala["y"] += bala["dy"]

# Mover enemigos
def mover_enemigos():
    for enemigo in enemigos:
        enemigo["x"] += enemigo["dx"]
        enemigo["y"] += enemigo["dy"]

        # Rebotan en los bordes
        if enemigo["x"] - enemigo["radio"] <= 0 or enemigo["x"] + enemigo["radio"] >= ANCHO:
            enemigo["dx"] *= -1
        if enemigo["y"] - enemigo["radio"] <= 0 or enemigo["y"] + enemigo["radio"] >= ALTO:
            enemigo["dy"] *= -1

# Verificar colisiones entre balas y enemigos
def verificar_colisiones():
    global enemigos
    enemigos_restantes = []
    for enemigo in enemigos:
        golpeado = False
        for bala in balas:
            distancia = math.hypot(bala["x"] - enemigo["x"], bala["y"] - enemigo["y"])
            if distancia < bala["radio"] + enemigo["radio"]:
                golpeado = True
                break
        if not golpeado:
            enemigos_restantes.append(enemigo)
    enemigos = enemigos_restantes

# Bucle principal del juego
jugando = True
while jugando:
    pantalla.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

        # Disparo con clic izquierdo
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            angulo = math.atan2(mouse_y - jugador_y, mouse_x - jugador_x)
            velocidad_bala = 10
            dx = velocidad_bala * math.cos(angulo)
            dy = velocidad_bala * math.sin(angulo)
            bala = {
                "x": jugador_x,
                "y": jugador_y,
                "dx": dx,
                "dy": dy,
                "radio": 8
            }
            balas.append(bala)

    # Movimiento del jugador con teclas WASD
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        jugador_y -= velocidad_jugador
    if teclas[pygame.K_s]:
        jugador_y += velocidad_jugador
    if teclas[pygame.K_a]:
        jugador_x -= velocidad_jugador
    if teclas[pygame.K_d]:
        jugador_x += velocidad_jugador

    mover_balas()
    mover_enemigos()
    verificar_colisiones()

    dibujar_jugador()
    dibujar_balas()
    dibujar_enemigos()

    # Si no hay enemigos, mostrar mensaje de victoria
    if not enemigos:
        fuente = pygame.font.SysFont(None, 60)
        texto = fuente.render("¡Ganaste!", True, NEGRO)
        pantalla.blit(texto, (ANCHO // 2 - 120, ALTO // 2 - 30))

    pygame.display.update()
    reloj.tick(FPS)

pygame.quit()


