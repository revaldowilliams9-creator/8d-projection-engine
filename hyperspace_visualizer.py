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

# --- COLORS (Matching your UI image) ---
BG_DARK = (13, 17, 23)        # Deep dark blue/black background
GRID_GRAY = (40, 44, 52)      # Axis line color
TEXT_MUTED = (139, 148, 158)  # Gray text for axes labels
CYAN = (0, 191, 255)          # Hyper-Ball A
MAGENTA = (236, 72, 153)      # Hyper-Ball B
GOLD_GLOW = (255, 191, 0)     # The intersection point

# --- 8D MATHEMATICS ENGINE ---
def rotate_8d(point, angles):
    x1, x2, x3, x4, x5, x6, x7, x8 = point
    a1, a2, a3, a4 = angles

    # Rotate across 4 distinct multi-verse planes over time
    # This smoothly shifts hidden dimensions into the X1 and X2 viewable tracks
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
        # Gaussian distribution creates a dense central core and soft edges like your image
        coords = [random.gauss(0, 0.4) * radius for _ in range(8)]
        # Displace the clusters natively in the upper dimensions
        point_with_offset = [c + off for c, off in zip(coords, offset_8d)]
        points.append(point_with_offset)
    return points

# Setup Hyper-Ball A (Cyan) and B (Magenta) with distinct 8D spatial placements
num_particles = 200
ball_A = generate_hyperball(num_particles, 1.0, [0.8, -0.2, 0.2, -0.1, 0.4, 0, 0, 0])
ball_B = generate_hyperball(num_particles, 1.0, [-0.8, 0.2, -0.2, 0.1, -0.4, 0, 0, 0])

# State Trackers
angle_1, angle_2, angle_3, angle_4 = 0, 0, 0, 0
font = pygame.font.SysFont("Arial", 16)
bold_font = pygame.font.SysFont("Arial", 16, bold=True)

# Main Loop
running = True
while running:
    screen.fill(BG_DARK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Dynamic time-based rotation adjustments to drift the 8D shapes
    angle_1 += 0.006
    angle_2 += 0.004
    angle_3 += 0.007
    angle_4 += 0.003
    current_angles = (angle_1, angle_2, angle_3, angle_4)

    # --- DRAW GRID & AXES ---
    center_x, center_y = WIDTH // 2, HEIGHT // 3 + 50
    # X1 Horizontal Axis
    pygame.draw.line(screen, GRID_GRAY, (100, center_y), (WIDTH - 100, center_y), 1)
    # X2 Vertical Axis
    pygame.draw.line(screen, GRID_GRAY, (center_x, 100), (center_x, HEIGHT - 300), 1)
    
    # Text Labels
    screen.blit(font.render("X1-Axis", True, TEXT_MUTED), (WIDTH - 180, center_y - 25))
    screen.blit(font.render("X2-Axis", True, TEXT_MUTED), (center_x + 15, 110))

    # --- PROJECT AND DRAW THE HYPER-BALLS ---
    projected_positions_A = []
    projected_positions_B = []

    # Draw Hyper-Ball A (Cyan)
    for point in ball_A:
        rotated = rotate_8d(point, current_angles)
        # Slicing perspective onto flat human view coordinates (using rotated X1 and X2 values)
        screen_x = int(center_x + rotated[0] * 180)
        screen_y = int(center_y + rotated[1] * 180)
        projected_positions_A.append((screen_x, screen_y))
        
        if 0 < screen_x < WIDTH and 0 < screen_y < HEIGHT:
            # Alpha/Transparency layer simulation using multiple radii circles
            pygame.draw.circle(screen, (*CYAN, 60), (screen_x, screen_y), 8)
            pygame.draw.circle(screen, CYAN, (screen_x, screen_y), 4)

    # Draw Hyper-Ball B (Magenta)
    for point in ball_B:
        rotated = rotate_8d(point, current_angles)
        screen_x = int(center_x + rotated[0] * 180)
        screen_y = int(center_y + rotated[1] * 180)
        projected_positions_B.append((screen_x, screen_y))
        
        if 0 < screen_x < WIDTH and 0 < screen_y < HEIGHT:
            pygame.draw.circle(screen, (*MAGENTA, 60), (screen_x, screen_y), 8)
            pygame.draw.circle(screen, MAGENTA, (screen_x, screen_y), 4)

    # --- FIND AND DRAW INTERSECTION POINT ---
    # Find the central overlapping point where the two clusters visually merge
    if projected_positions_A and projected_positions_B:
        avg_x_A = sum(p[0] for p in projected_positions_A) // len(projected_positions_A)
        avg_y_A = sum(p[1] for p in projected_positions_A) // len(projected_positions_A)
        avg_x_B = sum(p[0] for p in projected_positions_B) // len(projected_positions_B)
        avg_y_B = sum(p[1] for p in projected_positions_B) // len(projected_positions_B)
        
        # Midpoint of the two cloud bodies
        mid_x = (avg_x_A + avg_x_B) // 2
        mid_y = (avg_y_A + avg_y_B) // 2
        
        # Golden glowing intersection visual
        pygame.draw.circle(screen, (255, 235, 150), (mid_x, mid_y), 14, 1)  # Outer ring
        pygame.draw.circle(screen, GOLD_GLOW, (mid_x, mid_y), 7)            # Inner core

    # --- LOWER DATA DASHBOARD PANEL ---
    panel_y = HEIGHT - 200
    pygame.draw.rect(screen, (22, 27, 34), (50, panel_y, WIDTH - 100, 150), border_radius=10)
    
    # Legend Text labels
    pygame.draw.circle(screen, CYAN, (80, panel_y + 30), 6)
    screen.blit(font.render("Hyper-Ball A (Cyan)", True, CYAN), (95, panel_y + 20))
    
    pygame.draw.circle(screen, MAGENTA, (WIDTH - 250, panel_y + 30), 6)
    screen.blit(font.render("Hyper-Ball B (Magenta)", True, MAGENTA), (WIDTH - 235, panel_y + 20))

    # Mathematical Readout metrics labels
    lbl_dist_8d = font.render("8D Distance", True, TEXT_MUTED)
    val_dist_8d = font.render("2.00 r", True, (255, 255, 255))
    screen.blit(lbl_dist_8d, (120, panel_y + 80))
    screen.blit(val_dist_8d, (140, panel_y + 105))

    lbl_dist_3d = font.render("3D Projected Dist", True, TEXT_MUTED)
    val_dist_3d = font.render(f"{abs(avg_x_A - avg_x_B)/100:.2f} r", True, (255, 255, 255))
    screen.blit(lbl_dist_3d, (420, panel_y + 80))
    screen.blit(val_dist_3d, (465, panel_y + 105))

    lbl_planes = font.render("Active Planes", True, TEXT_MUTED)
    val_planes = font.render("4 Planes", True, (255, 255, 255))
    screen.blit(lbl_planes, (750, panel_y + 80))
    screen.blit(val_planes, (770, panel_y + 105))

    # --- REFRESH DISPLAY ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
