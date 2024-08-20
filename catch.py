import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
canvas_width = 800
canvas_height = 600
screen = pygame.display.set_mode((canvas_width, canvas_height))
pygame.display.set_caption("Gimme gimme Pizzas!")

# Cargar música de fondo
pygame.mixer.music.load("music/background-music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Cargar efectos de sonido
catch_sound = pygame.mixer.Sound("sound/catch.wav")
dangerous_sound = pygame.mixer.Sound("sound/ouch.wav")
game_over_sound = pygame.mixer.Sound("sound/game_over.mp3")

# Cargar imágenes
bg_image = pygame.image.load("img/bg-pizzeria.jpeg")
bg_image = pygame.transform.scale(bg_image, (canvas_width, canvas_height))

pizza_image = pygame.image.load("img/pizza-img.png")
pizza_image = pygame.transform.scale(pizza_image, (95, 75))

catcher_image = pygame.image.load("img/me-img.png")
catcher_image = pygame.transform.scale(catcher_image, (120, 120))

# Cargar imagen del objeto peligroso
dangerous_image = pygame.image.load("img/basura.png")
dangerous_image = pygame.transform.scale(dangerous_image, (95, 75))

# Variables del juego
initial_speed = 3
pizza_speed = initial_speed
pizza_interval = 1000  # Milisegundos
lives_remaining = 3
score = 0
pizzas = []
dangerous_items = []
font = pygame.font.SysFont('Helvetica', 25, True)

# Posición inicial de la cesta
catcher_rect = catcher_image.get_rect(midbottom=(canvas_width // 2, canvas_height - 30))

# Función para crear nuevas pizzas y objetos peligrosos
def create_pizza():
    x = random.randint(10, canvas_width - 105)
    y = -50
    if random.randint(0, 4) == 0:  # 20% de probabilidad de que sea un objeto peligroso
        rect = dangerous_image.get_rect(topleft=(x, y))
        dangerous_items.append(rect)
    else:
        rect = pizza_image.get_rect(topleft=(x, y))
        pizzas.append(rect)

# Función para mover las pizzas y objetos peligrosos
def move_items():
    global lives_remaining
    for pizza in pizzas[:]:
        pizza.move_ip(0, pizza_speed)
        if pizza.bottom > canvas_height:
            pizzas.remove(pizza)
            lives_remaining -= 1  # Pierde una vida si la pizza cae al fondo

    for item in dangerous_items[:]:
        item.move_ip(0, pizza_speed)
        if item.bottom > canvas_height:
            dangerous_items.remove(item)  # Simplemente desaparece si el objeto peligroso cae al fondo

# Función para detectar colisiones
def check_collisions():
    global score, lives_remaining, pizza_speed
    for pizza in pizzas[:]:
        if catcher_rect.colliderect(pizza):
            pizzas.remove(pizza)
            score += 10  # Incrementar la puntuación al atrapar una pizza
            pizza_speed += 0.2  # Aumentar la velocidad de caída
            catch_sound.play()  # Reproducir sonido de atrapar

    for item in dangerous_items[:]:
        if catcher_rect.colliderect(item):
            dangerous_items.remove(item)
            lives_remaining -= 1  # Pierde una vida al atrapar un objeto peligroso
            dangerous_sound.play()  # Reproducir sonido de objeto peligroso

# Función de Game Over
def game_over():
    pygame.mixer.music.stop()
    game_over_sound.play()  # Reproducir sonido de game over
    screen.fill((0, 0, 0))
    game_over_font = pygame.font.SysFont('Helvetica', 50, True)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    final_score_text = game_over_font.render(f'Final Score: {score}', True, (255, 255, 255))
    screen.blit(game_over_text, (canvas_width // 2 - game_over_text.get_width() // 2, canvas_height // 3))
    screen.blit(final_score_text, (canvas_width // 2 - final_score_text.get_width() // 2, canvas_height // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

# Bucle principal del juego
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, pizza_interval)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            create_pizza()

    # Movimiento de la cesta
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and catcher_rect.left > 0:
        catcher_rect.move_ip(-10, 0)
    if keys[pygame.K_RIGHT] and catcher_rect.right < canvas_width:
        catcher_rect.move_ip(10, 0)

    move_items()
    check_collisions()

    # Dibujar todo
    screen.blit(bg_image, (0, 0))
    screen.blit(catcher_image, catcher_rect)
    for pizza in pizzas:
        screen.blit(pizza_image, pizza)
    for item in dangerous_items:
        screen.blit(dangerous_image, item)

    # Mostrar puntuación y vidas
    score_text = font.render(f'Score: {score}', True, (255, 255, 0))
    lives_text = font.render(f'Lives: {lives_remaining}', True, (255, 255, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (canvas_width - 120, 10))

    pygame.display.flip()
    clock.tick(60)

    if lives_remaining <= 0:
        game_over()

pygame.quit()
