import pygame
import sys
import math
import random

pygame.init()
W, H = 1000, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Hyperspace Grid View (8D Projected)")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

THEMES = {
    "Deep Space": {"bg": (13, 17, 23), "grid": (40, 44, 52), "text": (139, 148, 158), "a": (0, 191, 255), "b": (236, 72, 153)},
    "Matrix": {"bg": (5, 15, 5), "grid": (15, 45, 15), "text": (50, 180, 50), "a": (0, 255, 70), "b": (150, 255, 0)},
    "Cyber": {"bg": (20, 10, 30), "grid": (50, 20, 70), "text": (180, 100, 230), "a": (255, 0, 128), "b": (0, 255, 200)},
    "Mono": {"bg": (20, 20, 20), "grid": (50, 50, 50), "text": (150, 150, 150), "a": (240, 240, 240), "b": (100, 100, 100)},
}

def rotate_8d(p, a):
    x1, x2, x3, x4, x5, x6, x7, x8 = p
    a1, a2, a3, a4 = a
    return [
        x1*math.cos(a1)-x5*math.sin(a1), x2*math.cos(a2)-x6*math.sin(a2),
        x3*math.cos(a3)-x7*math.sin(a3), x4*math.cos(a4)-x8*math.sin(a4),
        x1*math.sin(a1)+x5*math.cos(a1), x2*math.sin(a2)+x6*math.cos(a2),
        x3*math.sin(a3)+x7*math.cos(a3), x4*math.sin(a4)+x8*math.cos(a4),
    ]

def gen_ball(n, r, off):
    return [[random.gauss(0, 0.3)*r+o for o in off] for _ in range(n)]

ball_a = gen_ball(80, 1.0, [0.5, -0.2, 0.2, -0.1, 0, 0, 0, 0])
ball_b = gen_ball(80, 1.0, [-0.5, 0.2, -0.2, 0.1, 0, 0, 0, 0])

ang = [0, 0, 0, 0]
center_ang, t_idx = 0, 0
paused, persp, wire = False, True, True
spd, c_spd = 1.0, 1.0

running = True
while running:
    screen.fill(THEMES[list(THEMES)[t_idx]]["bg"])
    theme = THEMES[list(THEMES)[t_idx]]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            elif event.key == pygame.K_SPACE: paused = not paused
            elif event.key == pygame.K_p: persp = not persp
            elif event.key == pygame.K_UP: spd = min(5, spd + 0.2)
            elif event.key == pygame.K_DOWN: spd = max(0, spd - 0.2)
            elif event.key == pygame.K_t: t_idx = (t_idx + 1) % len(THEMES)
            elif event.key == pygame.K_m: wire = not wire
            elif event.key == pygame.K_w: c_spd = min(5, c_spd + 0.2)
            elif event.key == pygame.K_s: c_spd = max(0, c_spd - 0.2)
    
    if not paused:
        ang[0] += 0.006 * spd
        ang[1] += 0.004 * spd
        ang[2] += 0.007 * spd
        ang[3] += 0.003 * spd
        center_ang += 0.02 * c_spd
    
    cx, cy = W // 2, H // 3 + 50
    pygame.draw.line(screen, theme["grid"], (100, cy), (W - 100, cy), 1)
    pygame.draw.line(screen, theme["grid"], (cx, 100), (cx, H - 300), 1)
    screen.blit(font.render("X1-Axis", True, theme["text"]), (W - 180, cy - 25))
    screen.blit(font.render("X2-Axis", True, theme["text"]), (cx + 15, 110))
    
    if paused:
        pygame.draw.rect(screen, (200, 50, 50), (W - 60, 30, 6, 18))
        pygame.draw.rect(screen, (200, 50, 50), (W - 48, 30, 6, 18))
    else:
        pygame.draw.polygon(screen, (50, 200, 50), [(W - 55, 30), (W - 55, 48), (W - 40, 39)])
    
    proj_a, proj_b = [], []
    
    for ball, pos, col in [(ball_a, proj_a, theme["a"]), (ball_b, proj_b, theme["b"])]:
        for pt in ball:
            rot = rotate_8d(pt, tuple(ang))
            z = max(0.1, 3.0 - rot[2]) if persp else 1
            x, y = rot[0] * (2/z if persp else 1), rot[1] * (2/z if persp else 1)
            pos.append((int(cx + x * 250), int(cy + y * 250)))
        
        if wire:
            for i in range(len(pos)):
                p1, p2 = pos[i], pos[(i + 1) % len(pos)]
                if all(0 < p < (W if j == 0 else H) for j, p in [(0, p1[0]), (1, p1[1]), (0, p2[0]), (1, p2[1])]):
                    pygame.draw.line(screen, col, p1, p2, 1)
        
        for p in pos:
            if 0 < p[0] < W and 0 < p[1] < H:
                pygame.draw.circle(screen, col, p, 3)
    
    if proj_a and proj_b:
        avg_a = (sum(p[0] for p in proj_a) // len(proj_a), sum(p[1] for p in proj_a) // len(proj_a))
        avg_b = (sum(p[0] for p in proj_b) // len(proj_b), sum(p[1] for p in proj_b) // len(proj_b))
        mid = ((avg_a[0] + avg_b[0]) // 2, (avg_a[1] + avg_b[1]) // 2)
        shift = (int(math.sin(center_ang) * 60), int(math.cos(center_ang) * 60))
        final = (mid[0] + shift[0], mid[1] + shift[1])
        
        if 0 < final[0] < W and 0 < final[1] < H:
            pygame.draw.circle(screen, (255, 255, 255), final, 16, 1)
            pygame.draw.circle(screen, (255, 255, 255), final, 7)
        
        dist = int(math.hypot(avg_a[0] - avg_b[0], avg_a[1] - avg_b[1]))
    else:
        dist = 0
    
    py = H - 200
    pygame.draw.rect(screen, theme["bg"], (50, py, W - 100, 150))
    pygame.draw.rect(screen, theme["grid"], (50, py, W - 100, 150), 1)
    
    screen.blit(font.render("Speed: [▲▼]", True, theme["text"]), (60, py + 20))
    screen.blit(font.render(f"{spd:.1f}x", True, (100, 255, 100) if spd > 1 else (255, 255, 255)), (60, py + 40))
    screen.blit(font.render("Core: [W/S]", True, theme["text"]), (200, py + 20))
    screen.blit(font.render(f"{c_spd:.1f}x", True, (100, 255, 100) if c_spd > 1 else (255, 255, 255)), (200, py + 40))
    screen.blit(font.render("Distance", True, theme["text"]), (350, py + 20))
    screen.blit(font.render(f"{dist} px", True, theme["text"]), (350, py + 40))
    screen.blit(font.render("Mode: [P]", True, theme["text"]), (500, py + 20))
    screen.blit(font.render("Persp" if persp else "Ortho", True, (100, 255, 100) if persp else (255, 255, 255)), (500, py + 40))
    screen.blit(font.render("Theme: [T]", True, theme["text"]), (650, py + 20))
    screen.blit(font.render(list(THEMES)[t_idx], True, theme["text"]), (650, py + 40))
    screen.blit(font.render("[SPACE] Pause [M] Wire [ESC] Quit", True, theme["text"]), (60, py + 110))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
