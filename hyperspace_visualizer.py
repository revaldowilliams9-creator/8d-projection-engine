import pygame
import sys
import math
import random
from dataclasses import dataclass
from collections import deque

pygame.init()

W, H = 1000, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Hyperspace Grid View (8D Projected) - Auto-Equilibrium Engine")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 12)
bold_font = pygame.font.SysFont("Arial", 13, bold=True)
tiny_font = pygame.font.SysFont("Arial", 11)

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

# ============ TARGET MODES ============
TARGET_MODES = ["AUTO", "BALL_A", "BALL_B"]

# ============ KEYBOARD HINTS (organized by category) ============
KEYBOARD_HINTS = {
    "Stream": ["[I] Add", "[O] Remove", "[U] Target"],
    "View": ["[▲▼] Speed", "[W/S] Core", "[P] Persp", "[M] Wire"],
    "UI": ["[T] Theme", "[C] Color", "[R] Reset", "[SPACE] Pause"],
    "Nav": ["[Click+Drag] Pan", "[Scroll] Zoom"],
}

# ============ EQUILIBRIUM SYSTEM CONFIG ============
EQUILIBRIUM_CONFIG = {
    "target_min": 100,        # Min particles to maintain
    "target_max": 150,        # Max particles before forced removal
    "inflow_interval": 1.5,   # Auto-inject every 1.5 seconds
    "outflow_check_interval": 2.0,  # Check density every 2 seconds
    "outflow_threshold": 140,  # Trigger removal at this count
    "inflow_particle_count": 18,    # Particles per injection
    "outflow_particle_count": 12,   # Particles per removal
}

# ============ ADD / REMOVE STREAM CLASSES ============
@dataclass
class AddStream:
    """Represents a fresh 8D coordinate stream injected into the cluster."""
    origin: list
    velocity: list
    age: float = 0.0
    lifespan: float = 3.0
    particle_count: int = 15
    color_idx: int = 0

    def update(self, dt):
        self.age += dt

    def is_alive(self):
        return self.age < self.lifespan

    def apply(self, ball):
        for i in range(self.particle_count):
            t = i / max(1, self.particle_count - 1)
            new_point = [
                self.origin[j] + self.velocity[j] * t * 2.0 + random.gauss(0, 0.12)
                for j in range(8)
            ]
            ball.append(new_point)

    def get_alpha(self):
        progress = self.age / self.lifespan
        return max(0.0, 1.0 - (progress ** 2))

@dataclass
class RemoveStream:
    """Represents a removal pulse that strips nearby points from the cluster."""
    origin: list
    velocity: list
    age: float = 0.0
    lifespan: float = 2.0
    particle_count: int = 18
    max_remove: int = 18

    def update(self, dt):
        self.age += dt

    def is_alive(self):
        return self.age < self.lifespan

    def apply(self, ball):
        if not ball:
            return

        scored = []
        for pt in ball:
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pt, self.origin)))
            scored.append((dist, pt))
        scored.sort(key=lambda item: item[0])

        for _, pt in scored[: min(self.max_remove, len(scored))]:
            if pt in ball:
                ball.remove(pt)

    def get_alpha(self):
        progress = self.age / self.lifespan
        return max(0.0, 1.0 - (progress ** 2))

add_streams = deque(maxlen=30)
remove_streams = deque(maxlen=30)

def get_target_ball(mode, ball_a, ball_b):
    """Get the target ball based on injection mode."""
    if mode == 0:  # AUTO
        return ball_a if random.random() > 0.5 else ball_b
    elif mode == 1:  # BALL_A
        return ball_a
    else:  # BALL_B
        return ball_b

def inject_8d_stream(ball_target, num_particles=15, intensity=1.0, auto=False):
    """Create a fresh 8D stream and append it to the active cluster."""
    origin = [random.gauss(0, 0.5) for _ in range(8)]
    velocity = [random.gauss(0, 0.3) * intensity for _ in range(8)]
    stream = AddStream(origin=origin, velocity=velocity, particle_count=num_particles)
    stream.apply(ball_target)
    add_streams.append(stream)
    return stream

def remove_8d_stream(ball_target, num_particles=18, intensity=1.0, auto=False):
    """Create a removal pulse that strips points from the active cluster."""
    origin = [random.gauss(0, 0.7) for _ in range(8)]
    velocity = [random.gauss(0, 0.25) * intensity for _ in range(8)]
    stream = RemoveStream(origin=origin, velocity=velocity, particle_count=num_particles)
    stream.apply(ball_target)
    remove_streams.append(stream)
    return stream

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
        alpha = int(255 * (1 - i / glow_size) * 0.15)
        glow_color = tuple(int(c * (1 - i / glow_size)) for c in color)
        pygame.draw.circle(surface, glow_color, pos, radius + i, 0)

# ============ CAMERA CLASS ============
@dataclass
class Camera:
    x: float = 0.0      # Pan X
    y: float = 0.0      # Pan Y
    zoom: float = 1.0   # Zoom level

    def pan(self, dx, dy):
        """Move camera by delta"""
        self.x += dx
        self.y += dy

    def zoom_in(self, factor=0.1):
        """Zoom in by factor"""
        self.zoom = min(5.0, self.zoom + factor)

    def zoom_out(self, factor=0.1):
        """Zoom out by factor"""
        self.zoom = max(0.1, self.zoom - factor)

    def reset(self):
        """Reset camera to default"""
        self.x = 0.0
        self.y = 0.0
        self.zoom = 1.0

    def apply(self, pos, center_x, center_y, scale=250):
        """Apply camera transform to a screen position"""
        sx = int(center_x + (pos[0] * self.zoom * scale) + self.x)
        sy = int(center_y + (pos[1] * self.zoom * scale) + self.y)
        return (sx, sy)

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
camera = Camera()
mouse_dragging = False
last_mouse_pos = (0, 0)
injection_mode = 0  # 0=AUTO, 1=BALL_A, 2=BALL_B
injection_cooldown = 0.0
removal_cooldown = 0.0

# ============ EQUILIBRIUM TIMERS ============
inflow_timer = 0.0
outflow_timer = 0.0
auto_equilibrium_enabled = True

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
    injection_cooldown = max(0, injection_cooldown - dt)
    removal_cooldown = max(0, removal_cooldown - dt)

    # ============ AUTO-EQUILIBRIUM SYSTEM ============
    if auto_equilibrium_enabled and not paused:
        inflow_timer += dt
        outflow_timer += dt
        
        total_particles = len(ball_a) + len(ball_b)
        
        # NATURAL INFLOW: Auto-inject fresh particles every N seconds
        if inflow_timer >= EQUILIBRIUM_CONFIG["inflow_interval"]:
            if total_particles < EQUILIBRIUM_CONFIG["target_max"]:
                target = ball_a if random.random() > 0.5 else ball_b
                inject_8d_stream(
                    target,
                    num_particles=EQUILIBRIUM_CONFIG["inflow_particle_count"],
                    intensity=0.8,
                    auto=True
                )
            inflow_timer = 0.0
        
        # NATURAL OUTFLOW: Auto-remove particles if density exceeds threshold
        if outflow_timer >= EQUILIBRIUM_CONFIG["outflow_check_interval"]:
            if total_particles > EQUILIBRIUM_CONFIG["outflow_threshold"]:
                target = ball_a if len(ball_a) > len(ball_b) else ball_b
                remove_8d_stream(
                    target,
                    num_particles=EQUILIBRIUM_CONFIG["outflow_particle_count"],
                    intensity=0.9,
                    auto=True
                )
            outflow_timer = 0.0

    theme = THEMES[THEME_NAMES[theme_idx]]
    core_col = CORE_COLORS[core_idx]
    screen.fill(theme["bg"])

    # ---- MOUSE INPUT ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click = pan
                mouse_dragging = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 4:  # Scroll up = zoom in
                camera.zoom_in(0.15)
            elif event.button == 5:  # Scroll down = zoom out
                camera.zoom_out(0.15)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_dragging:
                current_pos = pygame.mouse.get_pos()
                dx = (current_pos[0] - last_mouse_pos[0]) * 0.5
                dy = (current_pos[1] - last_mouse_pos[1]) * 0.5
                camera.pan(dx, dy)
                last_mouse_pos = current_pos
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
            elif event.key == pygame.K_r:  # Reset camera
                camera.reset()
            elif event.key == pygame.K_u:  # Toggle injection target mode
                injection_mode = (injection_mode + 1) % len(TARGET_MODES)
            elif event.key == pygame.K_a:  # Toggle auto-equilibrium
                auto_equilibrium_enabled = not auto_equilibrium_enabled
            elif event.key == pygame.K_i:  # Add a fresh 8D stream (manual)
                if injection_cooldown <= 0:
                    target = get_target_ball(injection_mode, ball_a, ball_b)
                    inject_8d_stream(target, num_particles=20, intensity=1.2)
                    injection_cooldown = 0.35
            elif event.key == pygame.K_o:  # Remove an 8D stream (manual)
                if removal_cooldown <= 0:
                    target = get_target_ball(injection_mode, ball_a, ball_b)
                    remove_8d_stream(target, num_particles=18, intensity=1.0)
                    removal_cooldown = 0.40

    # Update active streams
    for stream in list(add_streams):
        stream.update(dt)
        if not stream.is_alive():
            add_streams.remove(stream)

    for stream in list(remove_streams):
        stream.update(dt)
        if not stream.is_alive():
            remove_streams.remove(stream)

    if not paused:
        ang[0] += 0.006 * speed
        ang[1] += 0.004 * speed
        ang[2] += 0.007 * speed
        ang[3] += 0.003 * speed
        center_ang += 0.02 * core_speed

    cx, cy = config.width // 2, config.height // 3 + 50

    # Draw grid with camera transform
    grid_x1 = int(100 + camera.x)
    grid_x2 = int(config.width - 100 + camera.x)
    grid_y1 = int(cy + camera.y)
    grid_y2 = int(cy + camera.y)

    pygame.draw.line(screen, theme["grid"], (grid_x1, grid_y1), (grid_x2, grid_y2), 1)
    pygame.draw.line(screen, theme["grid"], (int(cx + camera.x), int(100 + camera.y)), (int(cx + camera.x), int(config.height - 300 + camera.y)), 1)
    screen.blit(font.render("X1", True, theme["text"]), (int(config.width - 120 + camera.x), int(cy - 15 + camera.y)))
    screen.blit(font.render("X2", True, theme["text"]), (int(cx + 20 + camera.x), int(120 + camera.y)))

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
            screen_pos = camera.apply((x, y), cx, cy)
            pos_list.append(screen_pos)

        if wire and len(pos_list) > 1:
            for i in range(len(pos_list)):
                p1 = pos_list[i]
                p2 = pos_list[(i + 1) % len(pos_list)]
                if all(0 < v < (config.width if j == 0 else config.height)
                       for j, v in [(0, p1[0]), (1, p1[1]), (0, p2[0]), (1, p2[1])]):
                    pygame.draw.line(screen, col, p1, p2, 1)

        for p in pos_list:
            if 0 < p[0] < config.width and 0 < p[1] < config.height:
                draw_glow(screen, col, p, 2, 5)
                pygame.draw.circle(screen, col, p, 2)

    dist = 0
    if proj_a and proj_b:
        avg_a = (sum(p[0] for p in proj_a) // len(proj_a), sum(p[1] for p in proj_a) // len(proj_a))
        avg_b = (sum(p[0] for p in proj_b) // len(proj_b), sum(p[1] for p in proj_b) // len(proj_b))
        mid = ((avg_a[0] + avg_b[0]) // 2, (avg_a[1] + avg_b[1]) // 2)
        shift = (int(math.sin(center_ang) * 60), int(math.cos(center_ang) * 60))
        final = (mid[0] + shift[0], mid[1] + shift[1])

        if 0 < final[0] < config.width and 0 < final[1] < config.height:
            draw_glow(screen, core_col, final, 7, 8)
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

    # Display injection target mode
    target_color = (100, 255, 100) if injection_mode > 0 else (255, 200, 100)
    target_label = f"Target: {TARGET_MODES[injection_mode]}"
    screen.blit(font.render(target_label, True, target_color), (920, panel_y + 20))

    # Display particle count and equilibrium status
    total_particles = len(ball_a) + len(ball_b)
    eq_status = "✓ AUTO" if auto_equilibrium_enabled else "✗ MANUAL"
    eq_color = (100, 200, 100) if auto_equilibrium_enabled else (255, 100, 100)
    screen.blit(font.render(f"Particles: {total_particles} | Eq: {eq_status}", True, eq_color), (920, panel_y + 40))

    fps_text = f"FPS: {int(clock.get_fps())} | Zoom: {camera.zoom:.1f}x | Add: {len(add_streams)} | Remove: {len(remove_streams)}"
    screen.blit(font.render(fps_text, True, theme["text"]), (config.width - 330, panel_y + 120))

    # ========== CLEAN KEYBOARD HINTS SECTION ==========
    hints_y = panel_y + 108
    hint_x_start = 60
    
    for category_idx, (category, hints) in enumerate(KEYBOARD_HINTS.items()):
        # Category title
        cat_color = (100, 200, 255) if category == "Stream" else (200, 200, 100) if category == "View" else (150, 150, 200)
        screen.blit(tiny_font.render(category.upper(), True, cat_color), (hint_x_start + category_idx * 230, hints_y - 12))
        
        # Hints in this category (single line)
        hints_text = "  ".join(hints)
        screen.blit(tiny_font.render(hints_text, True, theme["text"]), (hint_x_start + category_idx * 230, hints_y))

    # Add equilibrium hint
    screen.blit(tiny_font.render("[A] EQ", True, (150, 200, 150)), (hint_x_start, hints_y + 15))

    pygame.display.flip()

pygame.quit()
sys.exit()
