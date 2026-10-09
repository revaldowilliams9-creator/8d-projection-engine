# 🌌 High-Performance 8D Hyperspace Projection Engine (Final Draft)

An optimized, feature-rich real-time graphics visualization pipeline built with **Python** and **Pygame Community Edition**. This simulation takes random Gaussian particle distributions in an 8-dimensional hyperspace (X₁ through X₈), processes them via coupled trigonometric rotation matrices, and projects the output onto an interactive, stylized 2D telemetry dashboard viewport.

This draft brings massive performance optimization, custom state configuration wrapping, and advanced screen-space visual aesthetics like alpha-blended radial glow profiles.

---

## ✨ New Upgrades in this Build

* **Dynamic Radial Glow Engine (`draw_glow`):** Features an advanced multi-layered rendering function that draws clean, soft atmospheric glare around vertices and the intersection core.
* **Interactive Core Color Switching (`[C]`):** Loops instantly through 8 high-contrast core illumination profiles (`White`, `Cyan`, `Magenta`, `Yellow`, `Green`, `Red`, `Blue`, `Orange`).
* **8 Presets Extended Theme Suite:** Shifts background and spatial vector grid designs across an expanded preset list: *Deep Space*, *Matrix*, *Cyber*, *Mono*, *Sunset*, *Arctic*, *Forest*, and *Magenta*.
* **Streamlined State Config Handling:** Wraps environment constants, particle parameters, and display constraints safely inside a sleek `Config` data architecture.
* **Modular HUD Iteration Array:** Drives the bottom panel readouts through a layout matrix, eliminating data string performance stutter.

---

## 🎮 Interface & Interactive Hotkeys

Take full command of your hyperspace environment using interactive hardware inputs:

| Key Binding | Engine Telemetry Operation |
| :--- | :--- |
| **`SPACEBAR`** | **Master Simulation Pause** (Freezes or resumes spatial coordinate timeline steps). |
| **`P`** | **Toggle Projection Method** (Switches rendering math between *Perspective* and *Orthographic* modes). |
| **`UP / DOWN ARROWS`** | **Adjust Cloud Velocity** (Speeds up or slows down the outer particle clusters). |
| **`W / S`** | **Adjust Center Core Velocity** (Independently steps the orbital speed track of the inner white sphere). |
| **`C`** | **Cycle Core Color Profile** (Switches the visual spectrum preset of the independent middle ball). |
| **`T`** | **Cycle Environmental Themes** (Instantly morphs colors and background grid aesthetics). |
| **`M`** | **Toggle Wireframe Matrix** (Draws or hides connecting mesh vectors between particle vertices). |
| **`ESC`** | **System Terminate** (Gracefully clears memory streams and exits the application window). |

---

## 📐 Math Projection Pipeline Overview

Human vision is restricted to three geometric dimensions. To visual structural activity in an 8-dimensional coordinate structure, this script employs **Time (T)** as a processing vehicle:

1. **Trigonometric Rotation:** High-dimensional positions roll across 4 coupled rotation tracks inside native hyperspace (`angle_1` to `angle_4`).
2. **Dimension Reduction Slicing:** Higher indexes are systematically reduced to compute spatial depth perspective, guarded against division-by-zero bounds errors (Z-depth calculation).
3. **Flat Plane Projection:** Mapped values are dynamically amplified and translated onto the physical horizontal X₁ and vertical X₂ screen space coordinates.

---

## ⚙️ Quick Start Installation

### 1. Framework Installation
Make sure you are utilizing the high-performance community package variant capable of rendering smooth loops on modern Python environments:
```bash
pip install pygame-ce
```

### 2. Execution Entry Point
Run your centralized animation pipeline script straight from your integrated workspace terminal:
```bash
python hyperspace_visualizer.py
```
