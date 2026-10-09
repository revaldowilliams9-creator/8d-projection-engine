import pygame
import sys
import math
import random
from dataclasses import dataclass

pygame.init()

W, H = 1000, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Hyperspace Grid View (8D Projected)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)
bold_font = pygame.font.SysFont("Arial", 14, bold=True)

# ============ THEMES ============ 
THEMES = {
    "Deep Space": {"bg": (13, 17, 23), "grid": (40, 44, 52), "text": (139, 148, 158), "a": (0, 191, 255), "b": (236, 72, 153), "glow": 20},
    "Matrix": {"bg": (5, 15, 5), "grid": (15, 45, 15), "text": (50, 180, 50), "a": (0, 255, 70), "b": (150, 255, 0), "glow": 15},
    "Cyber": {"bg": (20, 10, 30), "grid": (50, 20, 70), "text": (180, 100, 230), "a": (255, 0, 128), "b": (0, 255, 200), "glow": 18},
    "Mono": {"bg": (20, 20, 20), "grid": (50, 50, 50), "text": (150, 150, 150), "a": (240, 240, 240), "b": (100, 100, 100), "glow": 10},
    "Sunset": {"bg": (40, 20, 30), "grid": (80, 40, 60), "text": (255, 180, 100), "a": (255, 120, 60), "b": (255, 200, 100), "glow": 16},
    "Arctic": {"bg": (15, 30, 50), "grid": (30, 60, 100), "text": (150, 200, 255), "a": (100, 200, 255), "b": (200, 230, 255), "glow": 22},
    "Forest": {"bg": (20, 35, 20), "grid": (40, 70, 40), "text": (100, 220, 100), "a": (50, 255, 100), "b": (150, 255, 150), "glow": 17},
    "Magenta": {"bg": (30, 15, 35), "grid": (60, 30, 70), "text": (255, 100, 200), "a": (255, 50, 150), "b": (200, 100, 255), "glow": 19},
}

# ============ CORE COLORS ============ 
CORE_COLORS = [
    (255, 255, 255),  # White
    (0, 255, 255),    # Cyan
    (255, 0, 255),    # Magenta
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (255, 0, 0),      # Red
    (0, 0, 255),      # Blue
    (255, 128, 0),    # Orange
]

CORE_NAMES = ["White", "Cyan", "Magenta", "Yellow", "Green", "Red", "Blue", "Orange"]
THEME_NAMES = list(THEMES.keys())

# ============ MATH ENGINE ============ 
def rotate_8d(p, a):
    x1, x2, x3, x4, x5, x6, x7, x8 = p
    a1, a2, a3, a4 = a
    return [
        x1 * math.cos(a1) - x5 * math.sin(a1),
        x2 * math.cos(a2) - x6 * math.sin(a2),
        x3 * math.cos(a3) - x7 * math.sin(a3),
        x4 * math.cos(a4) - x8 * math.sin(a4),
        x1 * math.sin(a1) + x5 * math.cos(a1),
        x2 * math.sin(a2) + x6 * math.cos(a2),
        x3 * math.sin(a3) + x7 * math.cos(a3),
        x4 * math.sin(a4) + x8 * math.cos(a4),
    ]

def gen_ball(n, r, off):
    return [[random.gauss(0, 0.3) * r + o for o in off] for _ in range(n)]

def draw_glow(surface, color, pos, radius, glow_size):
    for i in range(glow_size, 0, -1):
        alpha = int(255 * (1 - i / glow_size) * 0.3)
        glow_color = tuple(int(c * (1 - i / glow_size)) for c in color)
        pygame.draw.circle(surface, glow_color, pos, radius + i, 1)

# ============ STATE MANAGEMENT ============ 
@dataclass
class Config:
    width: int = 1000
    height: int = 800
    fps: int = 60
    num_particles: int = 80
    particle_radius: float = 1.0

config = Config()

ball_a = gen_ball(config.num_particles, config.particle_radius, [0.5, -0.2, 0.2, -0.1, 0, 0, 0, 0])
ball_b = gen_ball(config.num_particles, config.particle_radius, [-0.5, 0.2, -0.2, 0.1, 0, 0, 0, 0])

ang = [0.0, 0.0, 0.0, 0.0]
center_ang = 0.0
theme_idx = 0
core_idx = 0
paused = False
persp = True
wire = True
speed = 1.0
core_speed = 1.0
frame_count = 0

HUD_ITEMS = [
    {"label": "Speed: [▲▼]", "x": 60, "y": 20, "value_y": 40},
    {"label": "Core: [W/S]", "x": 200, "y": 20, "value_y": 40},
    {"label": "Distance", "x": 350, "y": 20, "value_y": 40},
    {"label": "Mode: [P]", "x": 500, "y": 20, "value_y": 40},
    {"label": "Theme: [T]", "x": 650, "y": 20, "value_y": 40},
    {"label": "Core: [C]", "x": 800, "y": 20, "value_y": 40},
]

running = True
while running:
    frame_count += 1
    dt = clock.tick(config.fps) / 1000.0

    theme = THEMES[THEME_NAMES[theme_idx]]
    core_col = CORE_COLORS[core_idx]
    screen.fill(theme["bg"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_p:
                persp = not persp
            elif event.key == pygame.K_UP:
                speed = min(5.0, speed + 0.2)
            elif event.key == pygame.K_DOWN:
                speed = max(0.0, speed - 0.2)
            elif event.key == pygame.K_t:
                theme_idx = (theme_idx + 1) % len(THEME_NAMES)
            elif event.key == pygame.K_m:
                wire = not wire
            elif event.key == pygame.K_w:
                core_speed = min(5.0, core_speed + 0.2)
            elif event.key == pygame.K_s:
                core_speed = max(0.0, core_speed - 0.2)
            elif event.key == pygame.K_c:
                core_idx = (core_idx + 1) % len(CORE_COLORS)

    if not paused:
        ang[0] += 0.006 * speed
        ang[1] += 0.004 * speed
        ang[2] += 0.007 * speed
        ang[3] += 0.003 * speed
        center_ang += 0.02 * core_speed

    cx, cy = config.width // 2, config.height // 3 + 50
    pygame.draw.line(screen, theme["grid"], (100, cy), (config.width - 100, cy), 1)
    pygame.draw.line(screen, theme["grid"], (cx, 100), (cx, config.height - 300), 1)
    screen.blit(font.render("X1", True, theme["text"]), (config.width - 120, cy - 15))
    screen.blit(font.render("X2", True, theme["text"]), (cx + 20, 120))

    if paused:
        pygame.draw.rect(screen, (200, 50, 50), (config.width - 60, 30, 6, 18))
        pygame.draw.rect(screen, (200, 50, 50), (config.width - 48, 30, 6, 18))
    else:
        pygame.draw.polygon(screen, (50, 200, 50), [(config.width - 55, 30), (config.width - 55, 48), (config.width - 40, 39)])

    proj_a, proj_b = [], []
    for ball, pos_list, col in [(ball_a, proj_a, theme["a"]), (ball_b, proj_b, theme["b"])]:
        for pt in ball:
            rot = rotate_8d(pt, tuple(ang))
            z = max(0.1, 3.0 - rot[2]) if persp else 1.0
            factor = 2.0 / z if persp else 1.0
            x = rot[0] * factor
            y = rot[1] * factor
            pos_list.append((int(cx + x * 250), int(cy + y * 250)))

        if wire and len(pos_list) > 1:
            for i in range(len(pos_list)):
                p1 = pos_list[i]
                p2 = pos_list[(i + 1) % len(pos_list)]
                if all(0 < v < (config.width if j == 0 else config.height)
                       for j, v in [(0, p1[0]), (1, p1[1]), (0, p2[0]), (1, p2[1])]):
                    pygame.draw.line(screen, col, p1, p2, 1)

        for p in pos_list:
            if 0 < p[0] < config.width and 0 < p[1] < config.height:
                draw_glow(screen, col, p, 2, theme["glow"])
                pygame.draw.circle(screen, col, p, 3)

    dist = 0
    if proj_a and proj_b:
        avg_a = (sum(p[0] for p in proj_a) // len(proj_a), sum(p[1] for p in proj_a) // len(proj_a))
        avg_b = (sum(p[0] for p in proj_b) // len(proj_b), sum(p[1] for p in proj_b) // len(proj_b))
        mid = ((avg_a[0] + avg_b[0]) // 2, (avg_a[1] + avg_b[1]) // 2)
        shift = (int(math.sin(center_ang) * 60), int(math.cos(center_ang) * 60))
        final = (mid[0] + shift[0], mid[1] + shift[1])

        if 0 < final[0] < config.width and 0 < final[1] < config.height:
            draw_glow(screen, core_col, final, 7, theme["glow"] + 5)
            pygame.draw.circle(screen, core_col, final, 16, 2)
            pygame.draw.circle(screen, core_col, final, 7)

        dist = int(math.hypot(avg_a[0] - avg_b[0], avg_a[1] - avg_b[1]))

    panel_y = config.height - 200
    panel_bg = tuple(min(255, c + 15) for c in theme["bg"])
    pygame.draw.rect(screen, panel_bg, (50, panel_y, config.width - 100, 150), border_radius=10)
    pygame.draw.rect(screen, theme["grid"], (50, panel_y, config.width - 100, 150), width=1, border_radius=10)

    hud_values = [
        f"{speed:.1f}x",
        f"{core_speed:.1f}x",
        f"{dist} px",
        "Persp" if persp else "Ortho",
        THEME_NAMES[theme_idx],
        CORE_NAMES[core_idx],
    ]

    hud_colors = [
        (100, 255, 100) if speed > 1.0 else (255, 255, 255),
        (100, 255, 100) if core_speed > 1.0 else (255, 255, 255),
        theme["text"],
        (100, 255, 100) if persp else (255, 255, 255),
        theme["text"],
        core_col,
    ]

    for idx, item in enumerate(HUD_ITEMS):
        screen.blit(font.render(item["label"], True, theme["text"]), (item["x"], panel_y + item["y"]))
        screen.blit(bold_font.render(hud_values[idx], True, hud_colors[idx]), (item["x"], panel_y + item["value_y"]))

    fps_text = f"FPS: {int(clock.get_fps())}"
    screen.blit(font.render(fps_text, True, theme["text"]), (config.width - 120, panel_y + 120))

    hints = "[SPACE] Pause   [M] Wire   [C] Core   [P] Proj   [T] Theme   [ESC] Quit"
    screen.blit(font.render(hints, True, theme["text"]), (60, panel_y + 110))

    pygame.display.flip()

pygame.quit()
sys.exit()
