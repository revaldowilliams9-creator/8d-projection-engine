import math
import random
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import pygame


@dataclass(frozen=True)
class Theme:
    bg: Tuple[int, int, int]
    grid: Tuple[int, int, int]
    text: Tuple[int, int, int]
    ball_a: Tuple[int, int, int]
    ball_b: Tuple[int, int, int]
    intersection: Tuple[int, int, int]
    accent: Tuple[int, int, int]


@dataclass
class SimulationState:
    angle_1: float = 0.0
    angle_2: float = 0.0
    angle_3: float = 0.0
    angle_4: float = 0.0
    center_angle: float = 0.0
    is_paused: bool = False
    projection_mode: str = "Perspective"
    show_wireframe: bool = True
    speed_factor: float = 1.0
    center_speed_factor: float = 1.0
    speed_1: float = 0.006
    speed_2: float = 0.004
    speed_3: float = 0.007
    speed_4: float = 0.003


THEMES: Dict[str, Theme] = {
    "Deep Space": Theme(
        bg=(13, 17, 23),
        grid=(40, 44, 52),
        text=(139, 148, 158),
        ball_a=(0, 191, 255),
        ball_b=(236, 72, 153),
        intersection=(255, 255, 255),
        accent=(88, 166, 255),
    ),
    "Matrix Neon": Theme(
        bg=(5, 15, 5),
        grid=(15, 45, 15),
        text=(50, 180, 50),
        ball_a=(0, 255, 70),
        ball_b=(150, 255, 0),
        intersection=(255, 255, 255),
        accent=(0, 255, 70),
    ),
    "Cyber Synth": Theme(
        bg=(20, 10, 30),
        grid=(50, 20, 70),
        text=(180, 100, 230),
        ball_a=(255, 0, 128),
        ball_b=(0, 255, 200),
        intersection=(255, 255, 255),
        accent=(255, 0, 128),
    ),
    "Monochrome": Theme(
        bg=(20, 20, 20),
        grid=(50, 50, 50),
        text=(150, 150, 150),
        ball_a=(240, 240, 240),
        ball_b=(100, 100, 100),
        intersection=(255, 255, 255),
        accent=(200, 200, 200),
    ),
}


def rotate_8d(point: List[float], angles: Tuple[float, float, float, float]) -> List[float]:
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


class HyperBall:
    def __init__(self, name: str, num_points: int, radius: float, offset: List[float], color: Tuple[int, int, int]):
        self.name = name
        self.radius = radius
        self.offset = offset
        self.color = color
        self.points = self.generate_points(num_points)

    @staticmethod
    def generate_hyperball(num_points: int, radius: float, offset_8d: List[float]) -> List[List[float]]:
        points: List[List[float]] = []
        for _ in range(num_points):
            coords = [random.gauss(0, 0.3) * radius for _ in range(8)]
            point_with_offset = [c + off for c, off in zip(coords, offset_8d)]
            points.append(point_with_offset)
        return points

    def generate_points(self, num_points: int) -> List[List[float]]:
        return self.generate_hyperball(num_points, self.radius, self.offset)

    @staticmethod
    def generate_hyperball(num_points: int, radius: float, offset_8d: List[float]) -> List[List[float]]:
        return HyperBall.generate_points_static(num_points, radius, offset_8d)

    @staticmethod
    def generate_points_static(num_points: int, radius: float, offset_8d: List[float]) -> List[List[float]]:
        points: List[List[float]] = []
        for _ in range(num_points):
            coords = [random.gauss(0, 0.3) * radius for _ in range(8)]
            point_with_offset = [c + off for c, off in zip(coords, offset_8d)]
            points.append(point_with_offset)
        return points


class HyperspaceVisualizer:
    def __init__(self, width: int = 1000, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hyperspace Grid View (8D Projected)")
        self.clock = pygame.time.Clock()

        self.theme_names = list(THEMES.keys())
        self.current_theme_index = 0
        self.current_theme = THEMES[self.theme_names[self.current_theme_index]]

        self.state = SimulationState()

        self.font = pygame.font.SysFont("Arial", 16)
        self.bold_font = pygame.font.SysFont("Arial", 16, bold=True)

        self.ball_a = HyperBall(
            "A",
            num_points=80,
            radius=1.0,
            offset=[0.5, -0.2, 0.2, -0.1, 0, 0, 0, 0],
            color=self.current_theme.ball_a
        )
        self.ball_b = HyperBall(
            "B",
            num_points=80,
            radius=1.0,
            offset=[-0.5, 0.2, -0.2, 0.1, 0, 0, 0, 0],
            color=self.current_theme.ball_b
        )

        self.running = True

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.state.is_paused = not self.state.is_paused
                elif event.key == pygame.K_p:
                    self.state.projection_mode = (
                        "Orthographic" if self.state.projection_mode == "Perspective" else "Perspective"
                    )
                elif event.key == pygame.K_UP:
                    self.state.speed_factor = min(5.0, self.state.speed_factor + 0.2)
                elif event.key == pygame.K_DOWN:
                    self.state.speed_factor = max(0.0, self.state.speed_factor - 0.2)
                elif event.key == pygame.K_t:
                    self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_names)
                    self.current_theme = THEMES[self.theme_names[self.current_theme_index]]
                    self.ball_a.color = self.current_theme.ball_a
                    self.ball_b.color = self.current_theme.ball_b
                elif event.key == pygame.K_m:
                    self.state.show_wireframe = not self.state.show_wireframe
                elif event.key == pygame.K_w:
                    self.state.center_speed_factor = min(5.0, self.state.center_speed_factor + 0.2)
                elif event.key == pygame.K_s:
                    self.state.center_speed_factor = max(0.0, self.state.center_speed_factor - 0.2)

    def update(self, dt: float) -> None:
        if not self.state.is_paused:
            self.state.angle_1 += self.state.speed_1 * self.state.speed_factor * dt * 60
            self.state.angle_2 += self.state.speed_2 * self.state.speed_factor * dt * 60
            self.state.angle_3 += self.state.speed_3 * self.state.speed_factor * dt * 60
            self.state.angle_4 += self.state.speed_4 * self.state.speed_factor * dt * 60
            self.state.center_angle += 0.02 * self.state.center_speed_factor * dt * 60

    def project_point(self, rotated: List[float], center_x: int, center_y: int) -> Tuple[int, int]:
        if self.state.projection_mode == "Perspective":
            z_depth = max(0.1, 3.0 - rotated[2])
            factor = 2.0 / z_depth
            x_val = rotated[0] * factor
            y_val = rotated[1] * factor
        else:
            x_val = rotated[0]
            y_val = rotated[1]

        screen_x = int(center_x + x_val * 250)
        screen_y = int(center_y + y_val * 250)
        return screen_x, screen_y

    def draw_axes(self, center_x: int, center_y: int) -> None:
        pygame.draw.line(self.screen, self.current_theme.grid, (100, center_y), (self.width - 100, center_y), 1)
        pygame.draw.line(self.screen, self.current_theme.grid, (center_x, 100), (center_x, self.height - 300), 1)

        self.screen.blit(self.font.render("X1-Axis", True, self.current_theme.text), (self.width - 180, center_y - 25))
        self.screen.blit(self.font.render("X2-Axis", True, self.current_theme.text), (center_x + 15, 110))

    def draw_pause_indicator(self) -> None:
        if self.state.is_paused:
            pygame.draw.rect(self.screen, (200, 50, 50), (self.width - 60, 30, 6, 18))
            pygame.draw.rect(self.screen, (200, 50, 50), (self.width - 48, 30, 6, 18))
        else:
            pygame.draw.polygon(self.screen, (50, 200, 50), [(self.width - 55, 30), (self.width - 55, 48), (self.width - 40, 39)])

    def draw_ball(self, ball: HyperBall, center_x: int, center_y: int, projected_positions: List[Tuple[int, int]]) -> None:
        color = ball.color

        for point in ball.points:
            rotated = rotate_8d(point, (
                self.state.angle_1,
                self.state.angle_2,
                self.state.angle_3,
                self.state.angle_4,
            ))
            projected_positions.append(self.project_point(rotated, center_x, center_y))

        if self.state.show_wireframe and len(projected_positions) > 1:
            for i in range(len(projected_positions)):
                pt1 = projected_positions[i]
                pt2 = projected_positions[(i + 1) % len(projected_positions)]
                if (
                    0 < pt1[0] < self.width
                    and 0 < pt1[1] < self.height
                    and 0 < pt2[0] < self.width
                    and 0 < pt2[1] < self.height
                ):
                    pygame.draw.line(self.screen, color, pt1, pt2, 1)

        for pt in projected_positions:
            if 0 < pt[0] < self.width and 0 < pt[1] < self.height:
                pygame.draw.circle(self.screen, color, pt, 3)

    def draw_center_core(self, projected_a: List[Tuple[int, int]], projected_b: List[Tuple[int, int]]) -> int:
        if projected_a and projected_b:
            avg_x_a = sum(p[0] for p in projected_a) // len(projected_a)
            avg_y_a = sum(p[1] for p in projected_a) // len(projected_a)
            avg_x_b = sum(p[0] for p in projected_b) // len(projected_b)
            avg_y_b = sum(p[1] for p in projected_b) // len(projected_b)

            base_mid_x = (avg_x_a + avg_x_b) // 2
            base_mid_y = (avg_y_a + avg_y_b) // 2

            shift_x = int(math.sin(self.state.center_angle) * 60)
            shift_y = int(math.cos(self.state.center_angle) * 60)

            final_mid_x = base_mid_x + shift_x
            final_mid_y = base_mid_y + shift_y

            if 0 < final_mid_x < self.width and 0 < final_mid_y < self.height:
                pygame.draw.circle(self.screen, (255, 255, 255), (final_mid_x, final_mid_y), 16, 1)
                pygame.draw.circle(self.screen, (255, 255, 255), (final_mid_x, final_mid_y), 7)

            proj_dist = int(math.hypot(avg_x_a - avg_x_b, avg_y_a - avg_y_b))
            return proj_dist

        return 0

    def draw_lower_panel(self, proj_dist: int) -> None:
        panel_y = self.height - 200
        panel_bg = tuple(min(255, c + 15) for c in self.current_theme.bg)
        pygame.draw.rect(self.screen, panel_bg, (50, panel_y, self.width - 100, 150), border_radius=10)
        pygame.draw.rect(self.screen, self.current_theme.grid, (50, panel_y, self.width - 100, 150), width=1, border_radius=10)

        center_x = self.width // 2
        pygame.draw.circle(self.screen, self.current_theme.ball_a, (80, panel_y + 30), 6)
        self.screen.blit(self.font.render("Hyper-Ball A", True, self.current_theme.ball_a), (95, panel_y + 20))

        pygame.draw.circle(self.screen, (255, 255, 255), (center_x - 70, panel_y + 30), 6)
        self.screen.blit(self.font.render("Intersection Core (White)", True, (255, 255, 255)), (center_x - 55, panel_y + 20))

        pygame.draw.circle(self.screen, self.current_theme.ball_b, (self.width - 200, panel_y + 30), 6)
        self.screen.blit(self.font.render("Hyper-Ball B", True, self.current_theme.ball_b), (self.width - 185, panel_y + 20))

        self.screen.blit(self.font.render("Clouds Speed", True, self.current_theme.text), (60, panel_y + 80))
        speed_color = (
            (100, 255, 100) if self.state.speed_factor > 1.0
            else (255, 100, 100) if self.state.speed_factor == 0.0
            else (255, 255, 255)
        )
        self.screen.blit(self.bold_font.render(f"[▲▼] {self.state.speed_factor:.1f}x", True, speed_color), (60, panel_y + 105))

        self.screen.blit(self.font.render("Center Core Speed", True, self.current_theme.text), (230, panel_y + 80))
        c_speed_color = (
            (100, 255, 100) if self.state.center_speed_factor > 1.0
            else (255, 100, 100) if self.state.center_speed_factor == 0.0
            else (255, 255, 255)
        )
        self.screen.blit(self.bold_font.render(f"[W/S] {self.state.center_speed_factor:.1f}x", True, c_speed_color), (250, panel_y + 105))

        self.screen.blit(self.font.render("3D Projected Dist", True, self.current_theme.text), (420, panel_y + 80))
        self.screen.blit(self.bold_font.render(f"{proj_dist} px", True, self.current_theme.text), (440, panel_y + 105))

        self.screen.blit(self.font.render("Projection", True, self.current_theme.text), (580, panel_y + 80))
        mode_color = (100, 255, 100) if self.state.projection_mode == "Perspective" else (255, 255, 255)
        self.screen.blit(self.bold_font.render(f"[P] {self.state.projection_mode}", True, mode_color), (600, panel_y + 105))

        self.screen.blit(self.font.render("Theme", True, self.current_theme.text), (730, panel_y + 80))
        self.screen.blit(
            self.bold_font.render(f"[T] {self.theme_names[self.current_theme_index]}", True, self.current_theme.accent),
            (750, panel_y + 105),
        )

        hints = "[SPACE] Pause   [M] Wireframe   [W/S] Core Speed   [P] Projection   [T] Theme   [ESC] Quit"
        self.screen.blit(self.font.render(hints, True, self.current_theme.text), (60, panel_y + 135))

    def render(self) -> None:
        self.screen.fill(self.current_theme.bg)
        center_x, center_y = self.width // 2, self.height // 3 + 50

        self.draw_axes(center_x, center_y)
        self.draw_pause_indicator()

        projected_a: List[Tuple[int, int]] = []
        projected_b: List[Tuple[int, int]] = []

        self.draw_ball(self.ball_a, center_x, center_y, projected_a)
        self.draw_ball(self.ball_b, center_x, center_y, projected_b)

        proj_dist = self.draw_center_core(projected_a, projected_b)
        self.draw_lower_panel(proj_dist)

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = HyperspaceVisualizer()
    app.run()
