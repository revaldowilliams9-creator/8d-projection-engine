import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Setup display
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hyperspace Grid View (8D Projected)")
clock = pygame.time.Clock()

# --- THEME MANAGEMENT DICTIONARY ---
THEMES = {
    "Deep Space": {
        "bg": (13, 17, 23),
        "grid": (40, 44, 52),
        "text": (139, 148, 158),
        "ball_A": (0, 191, 255),       # Cyan
        "ball_B": (236, 72, 153),      # Magenta
        "intersection": (255, 191, 0),  # Gold Glow
        "accent": (88, 166, 255)
    },
    "Matrix Neon": {
        "bg": (5, 15, 5),
        "grid": (15, 45, 15),
        "text": (50, 180, 50),
        "ball_A": (0, 255, 70),        # Bright Green
        "ball_B": (150, 255, 0),       # Lime Green
        "intersection": (255, 255, 255),# Pure White
        "accent": (0, 255, 70)
    },
    "Cyber Synth": {
        "bg": (20, 10, 30),
        "grid": (50, 20, 70),
        "text": (180, 100, 230),
        "ball_A": (255, 0, 128),       # Hot Pink
        "ball_B": (0, 255, 200),       # Turquoise
        "intersection": (255, 215, 0),  # Gold
        "accent": (255, 0, 128)
    },
    "Monochrome": {
        "bg": (20, 20, 20),
        "grid": (50, 50, 50),
        "text": (150, 150, 150),
        "ball_A": (240, 240, 240),     # Bright Gray
        "ball_B": (100, 100, 100),     # Dark Gray
        "intersection": (255, 255, 255),# White
        "accent": (200, 200, 200)
    }
}

theme_names = list(THEMES.keys())
current_theme_index = 0
current_theme = THEMES[theme_names[current_theme_index]]

# --- 8D MATHEMATICS ENGINE ---
def rotate_8d(point, angles):
    x1, x2, x3, x4, x5, x6, x7, x8 = point
    a1, a2, a3, a4 = angles

    nx1 = x1 * math.cos(a1) - x5 * math.sin(a1)
    nx5 = x1 * math.sin(a1) + x5 * math.cos(a1)
    
    nx2 = x2 * math.cos(a2) - x6 * math.sin(a2)
    nx6 = x2 * math.sin(a2) + x6 * math.cos(a2)
    
    nx3 = x3 * math.cos(a3) - x7 * math.sin(a3)
    nx7 = x3 * math.sin(a3) + x7 * math.cos(a3)
    
    nx4 = x4 * math.cos(a4) - x8 * math.sin(a4)
    nx8 = x4 * math.sin(a4) + x8 * math.cos(a4)

    return [nx1, nx2, nx3, nx4, nx5, nx6, nx7, nx8]

# --- DATA GENERATION ---
def generate_hyperball(num_points, radius, offset_8d):
    points = []
    for _ in range(num_points):
        coords = [random.gauss(0, 0.4) * radius for _ in range(8)]
        point_with_offset = [c + off for c, off in zip(coords, offset_8d)]
        points.append(point_with_offset)
    return points

num_particles = 200
ball_A = generate_hyperball(num_particles, 1.0, [0.8, -0.2, 0.2, -0.1, 0.4, 0, 0, 0])
ball_B = generate_hyperball(num_particles, 1.0, [-0.8, 0.2, -0.2, 0.1, -0.4, 0, 0, 0])

# State Trackers
angle_1, angle_2, angle_3, angle_4 = 0, 0, 0, 0
is_paused = False
projection_mode = "Perspective"  

# Speed Factor Variables
speed_factor = 1.0  
base_speeds = (0.006, 0.004, 0.007, 0.003)  

font = pygame.font.SysFont("Arial", 16)
bold_font = pygame.font.SysFont("Arial", 16, bold=True)

# Main Loop
running = True
while running:
    # Use active theme background color
    screen.fill(current_theme["bg"])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                is_paused = not is_paused  
            elif event.key == pygame.K_p:
                projection_mode = "Orthographic" if projection_mode == "Perspective" else "Perspective"
            elif event.key == pygame.K_UP:
                speed_factor = min(5.0, speed_factor + 0.2)  
            elif event.key == pygame.K_DOWN:
                speed_factor = max(0.0, speed_factor - 0.2)  
            
            # --- THEME SWITCHER LOGIC ---
            elif event.key == pygame.K_t:
                current_theme_index = (current_theme_index + 1) % len(theme_names)
                current_theme = THEMES[theme_names[current_theme_index]]

    # Step rotations through time if not paused, multiplied by our speed factor
    if not is_paused:
        angle_1 += base_speeds[0] * speed_factor
        angle_2 += base_speeds[1] * speed_factor
        angle_3 += base_speeds[2] * speed_factor
        angle_4 += base_speeds[3] * speed_factor
    
    current_angles = (angle_1, angle_2, angle_3, angle_4)

    # --- DRAW GRID & AXES ---
    center_x, center_y = WIDTH // 2, HEIGHT // 3 + 50
    pygame.draw.line(screen, current_theme["grid"], (100, center_y), (WIDTH - 100, center_y), 1)
    pygame.draw.line(screen, current_theme["grid"], (center_x, 100), (center_x, HEIGHT - 300), 1)
    
    screen.blit(font.render("X1-Axis", True, current_theme["text"]), (WIDTH - 180, center_y - 25))
    screen.blit(font.render("X2-Axis", True, current_theme["text"]), (center_x + 15, 110))

    # UI Pause / Play indicator icon layout
    if is_paused:
        pygame.draw.rect(screen, (200, 50, 50), (WIDTH - 60, 30, 6, 18))
        pygame.draw.rect(screen, (200, 50, 50), (WIDTH - 48, 30, 6, 18))
    else:
        pygame.draw.polygon(screen, (50, 200, 50), [(WIDTH - 55, 30), (WIDTH - 55, 48), (WIDTH - 40, 39)])

    projected_positions_A = []
    projected_positions_B = []

    # Map Point Cloud Matrix using active theme colors
    for ball, storage, color_key in [(ball_A, projected_positions_A, "ball_A"), (ball_B, projected_positions_B, "ball_B")]:
        color = current_theme[color_key]
        for point in ball:
            rotated = rotate_8d(point, current_angles)
            
            if projection_mode == "Perspective":
                factor = 1 / (2.5 - rotated[4])  # Using depth coordinate slice
                x_val = rotated[0] * factor
                y_val = rotated[1] * factor
            else:
                x_val = rotated[0]
                y_val = rotated[1]

            screen_x = int(center_x + x_val * 200)
            screen_y = int(center_y + y_val * 200)
            storage.append((screen_x, screen_y))
            
            if 0 < screen_x < WIDTH and 0 < screen_y < HEIGHT:
                # Custom surfaces handles alpha layering cleanly
                s = pygame.Surface((16, 16), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, 40), (8, 8), 8)
                pygame.draw.circle(s, color, (8, 8), 3)
                screen.blit(s, (screen_x - 8, screen_y - 8))

    # --- DRAW INTERSECTION POINT ---
    if projected_positions_A and projected_positions_B:
        avg_x_A = sum(p[0] for p in projected_positions_A) // len(projected_positions_A)
        avg_y_A = sum(p[1] for p in projected_positions_A) // len(projected_positions_A)
        avg_x_B = sum(p[0] for p in projected_positions_B) // len(projected_positions_B)
        avg_y_B = sum(p[1] for p in projected_positions_B) // len(projected_positions_B)
        
        mid_x = (avg_x_A + avg_x_B) // 2
        mid_y = (avg_y_A + avg_y_B) // 2
        
        pygame.draw.circle(screen, current_theme["intersection"], (mid_x, mid_y), 14, 1)
        pygame.draw.circle(screen, current_theme["intersection"], (mid_x, mid_y), 6)

    # --- LOWER DATA DASHBOARD PANEL ---
    panel_y = HEIGHT - 200
    # Create slightly lighter panel background relative to theme background
    panel_bg = tuple(min(255, c + 15) for c in current_theme["bg"])
    pygame.draw.rect(screen, panel_bg, (50, panel_y, WIDTH - 100, 150), border_radius=10)
    pygame.draw.rect(screen, current_theme["grid"], (50, panel_y, WIDTH - 100, 150), width=1, border_radius=10)
    
    # Legend
    pygame.draw.circle(screen, current_theme["ball_A"], (80, panel_y + 30), 6)
    screen.blit(font.render("Hyper-Ball A", True, current_theme["ball_A"]), (95, panel_y + 20))
    pygame.draw.circle(screen, current_theme["ball_B"], (WIDTH - 200, panel_y + 30), 6)
    screen.blit(font.render("Hyper-Ball B", True, current_theme["ball_B"]), (WIDTH - 185, panel_y + 20))

    # Readouts
    screen.blit(font.render("8D Distance", True, current_theme["text"]), (75, panel_y + 80))
    screen.blit(bold_font.render("2.00 r", True, (255, 255, 255)), (95, panel_y + 105))

    screen.blit(font.render("3D Projected Dist", True, current_theme["text"]), (235, panel_y + 80))
    screen.blit(bold_font.render(f"{abs(avg_x_A - avg_x_B)/100:.2f} r", True, (255, 255, 255)), (270, panel_y + 105))

    screen.blit(font.render("Hyperspace Speed", True, current_theme["text"]), (430, panel_y + 80))
    speed_color = (100, 255, 100) if speed_factor > 1.0 else (255, 100, 100) if speed_factor == 0.0 else (255, 255, 255)
    screen.blit(bold_font.render(f"{speed_factor:.1f}x", True, speed_color), (465, panel_y + 105))

    screen.blit(font.render("Projection Style", True, current_theme["text"]), (625, panel_y + 80))
    screen.blit(bold_font.render(f"{projection_mode}", True, current_theme["accent"]), (625, panel_y + 105))

    # --- NEW VISUAL THEME UI READOUT ---
    screen.blit(font.render("Visual Theme", True, current_theme["text"]), (810, panel_y + 80))
    screen.blit(bold_font.render(f"[T] {theme_names[current_theme_index]}", True, (255, 255, 255)), (810, panel_y + 105))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
