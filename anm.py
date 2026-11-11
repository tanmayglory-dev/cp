
import pygame
import math
import random
import sys

pygame.init()

# ==========================================
# 3D UNIVERSE SIMULATOR
# ==========================================

WIDTH, HEIGHT = 1280, 800
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D UNIVERSE - Cosmic Explorer")

clock = pygame.time.Clock()

# Colors
BLACK = (2, 2, 12)
WHITE = (255, 255, 255)
CYAN = (40, 220, 255)
PURPLE = (150, 60, 255)
GOLD = (255, 190, 60)

font = pygame.font.SysFont("Arial", 18)
big_font = pygame.font.SysFont("Arial", 30, bold=True)

# ==========================================
# CAMERA SETTINGS
# ==========================================

camera_x = 0.35
camera_y = 0.0
zoom = 650
paused = False

# ==========================================
# 3D ROTATION AND PROJECTION
# ==========================================

def project(x, y, z):

    # Rotate around Y axis
    rx = x * math.cos(camera_y) - z * math.sin(camera_y)
    rz = x * math.sin(camera_y) + z * math.cos(camera_y)

    # Rotate around X axis
    ry = y * math.cos(camera_x) - rz * math.sin(camera_x)
    rz = y * math.sin(camera_x) + rz * math.cos(camera_x)

    distance = rz + 1100

    if distance < 50:
        return None

    factor = zoom / distance

    sx = int(CENTER_X + rx * factor)
    sy = int(CENTER_Y + ry * factor)

    return sx, sy, factor, rz


# ==========================================
# BACKGROUND STARS
# ==========================================

background_stars = []

for i in range(700):
    background_stars.append((
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3),
        random.randint(100, 255)
    ))


def draw_background():

    screen.fill(BLACK)

    for x, y, size, brightness in background_stars:

        brightness = int(
            brightness * random.uniform(0.75, 1.0)
        )

        pygame.draw.circle(
            screen,
            (brightness, brightness, brightness),
            (x, y),
            size
        )


# ==========================================
# GALAXY GENERATION
# ==========================================

galaxy = []

for i in range(2800):

    arm = random.randint(0, 4)

    radius = random.uniform(40, 460)

    angle = (
        arm * 2 * math.pi / 5
        + radius * 0.018
        + random.uniform(-0.4, 0.4)
    )

    x = math.cos(angle) * radius
    y = math.sin(angle) * radius

    z = random.gauss(0, 22)

    color_choice = random.choice([
        (100, 140, 255),
        (180, 100, 255),
        (255, 190, 150),
        (100, 220, 255),
        (255, 255, 255)
    ])

    galaxy.append((x, y, z, color_choice))


# ==========================================
# NEBULA PARTICLES
# ==========================================

nebula = []

for i in range(180):

    angle = random.uniform(0, math.pi * 2)
    radius = random.uniform(180, 550)

    x = math.cos(angle) * radius
    y = math.sin(angle) * radius

    z = random.uniform(-100, 100)

    nebula.append((
        x, y, z,
        random.choice([
            (80, 20, 150),
            (20, 70, 160),
            (150, 30, 100),
            (20, 120, 150)
        ])
    ))


# ==========================================
# PLANETS
# ==========================================

planets = [
    {
        "name": "MERCURY",
        "orbit": 150,
        "size": 7,
        "speed": 1.4,
        "color": (170, 160, 150)
    },
    {
        "name": "VENUS",
        "orbit": 220,
        "size": 12,
        "speed": 0.9,
        "color": (255, 180, 90)
    },
    {
        "name": "EARTH",
        "orbit": 310,
        "size": 16,
        "speed": 0.65,
        "color": (50, 130, 255)
    },
    {
        "name": "MARS",
        "orbit": 390,
        "size": 11,
        "speed": 0.45,
        "color": (255, 80, 60)
    },
    {
        "name": "JUPITER",
        "orbit": 500,
        "size": 28,
        "speed": 0.3,
        "color": (220, 160, 110)
    }
]


# ==========================================
# GLOW EFFECT
# ==========================================

def draw_glow(x, y, radius, color):

    for i in range(5, 0, -1):

        r = int(radius * i * 0.8)

        alpha_color = tuple(
            min(255, int(c / (i * 1.4)))
            for c in color
        )

        pygame.draw.circle(
            screen,
            alpha_color,
            (x, y),
            max(1, r)
        )


# ==========================================
# DRAW GALAXY
# ==========================================

def draw_galaxy(rotation):

    visible_stars = []

    for x, y, z, color in galaxy:

        # Slowly rotate galaxy
        angle = rotation * 0.12

        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)

        p = project(rx, ry, z)

        if p:
            sx, sy, factor, depth = p

            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:

                visible_stars.append(
                    (depth, sx, sy, factor, color)
                )

    # Draw distant stars first
    visible_stars.sort(reverse=True)

    for depth, sx, sy, factor, color in visible_stars:

        size = max(1, min(3, int(factor * 2)))

        pygame.draw.circle(
            screen,
            color,
            (sx, sy),
            size
        )


# ==========================================
# DRAW NEBULA
# ==========================================

def draw_nebula(rotation):

    for x, y, z, color in nebula:

        angle = rotation * 0.05

        rx = x * math.cos(angle) - y * math.sin(angle)
        ry = x * math.sin(angle) + y * math.cos(angle)

        p = project(rx, ry, z)

        if p:

            sx, sy, factor, depth = p

            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:

                pygame.draw.circle(
                    screen,
                    color,
                    (sx, sy),
                    max(1, int(7 * factor))
                )


# ==========================================
# DRAW BLACK HOLE
# ==========================================

def draw_black_hole(rotation):

    # Accretion disk
    for radius in range(95, 190, 12):

        points = []

        for i in range(100):

            angle = i * math.pi * 2 / 100

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius * 0.35
            z = math.sin(angle) * 20

            p = project(x, y, z)

            if p:
                points.append((p[0], p[1]))

        if len(points) > 2:

            color = random.choice([
                (255, 90, 20),
                (255, 160, 40),
                (180, 50, 255),
                (255, 220, 100)
            ])

            pygame.draw.lines(
                screen,
                color,
                True,
                points,
                2
            )

    center = project(0, 0, 0)

    if center:

        sx, sy = center[0], center[1]

        draw_glow(sx, sy, 38, (120, 40, 255))

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (sx, sy),
            28
        )

        pygame.draw.circle(
            screen,
            (70, 20, 130),
            (sx, sy),
            30,
            2
        )


# ==========================================
# DRAW PLANETS
# ==========================================

def draw_planets(time):

    for planet in planets:

        angle = time * planet["speed"]

        radius = planet["orbit"]

        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = math.sin(angle * 0.5) * 30

        p = project(x, y, z)

        if not p:
            continue

        sx, sy, factor, depth = p

        size = max(2, int(planet["size"] * factor))

        if not (0 <= sx < WIDTH and 0 <= sy < HEIGHT):
            continue

        color = planet["color"]

        draw_glow(sx, sy, size, color)

        pygame.draw.circle(
            screen,
            color,
            (sx, sy),
            size
        )

        # Planet highlight
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (sx - size // 3, sy - size // 3),
            max(1, size // 4)
        )

        # Planet label
        if size > 4:

            label = font.render(
                planet["name"],
                True,
                WHITE
            )

            screen.blit(
                label,
                (sx + size + 8, sy - 10)
            )


# ==========================================
# MAIN ANIMATION LOOP
# ==========================================

time = 0
running = True

while running:

    dt = clock.tick(60) / 1000

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:

                camera_x = 0.35
                camera_y = 0
                zoom = 650

            if event.key == pygame.K_UP:
                camera_x -= 0.08

            if event.key == pygame.K_DOWN:
                camera_x += 0.08

            if event.key == pygame.K_LEFT:
                camera_y -= 0.08

            if event.key == pygame.K_RIGHT:
                camera_y += 0.08

            if event.key == pygame.K_EQUALS:
                zoom += 50

            if event.key == pygame.K_MINUS:
                zoom = max(200, zoom - 50)

    if not paused:
        time += dt

    # DRAW EVERYTHING

    draw_background()

    draw_nebula(time)

    draw_galaxy(time)

    draw_black_hole(time)

    draw_planets(time)

    # TITLE
    title = big_font.render(
        "THE UNIVERSE",
        True,
        CYAN
    )

    screen.blit(title, (30, 25))

    subtitle = font.render(
        "3D COSMIC EXPLORER",
        True,
        WHITE
    )

    screen.blit(subtitle, (32, 65))

    # CONTROLS
    controls = [
        "ARROWS  : Rotate Camera",
        "+ / -   : Zoom In / Out",
        "SPACE   : Pause / Resume",
        "R       : Reset Camera",
        "ESC     : Exit"
    ]

    for i, line in enumerate(controls):

        text = font.render(
            line,
            True,
            (150, 200, 255)
        )

        screen.blit(
            text,
            (30, HEIGHT - 145 + i * 23)
        )

    # FPS
    fps = clock.get_fps()

    fps_text = font.render(
        f"FPS: {int(fps)}",
        True,
        (100, 255, 120)
    )

    screen.blit(
        fps_text,
        (WIDTH - 120, 30)
    )

    if paused:

        pause_text = big_font.render(
            "PAUSED",
            True,
            GOLD
        )

        screen.blit(
            pause_text,
            (CENTER_X - 55, HEIGHT - 70)
        )

    pygame.display.flip()


pygame.quit()
sys.exit()
