# 🌌 Object-Oriented 8D Hyperspace Projection Engine

An advanced, production-grade real-time graphics visualization engine written in **Python** using an architectural **Object-Oriented Programming (OOP)** layout built on top of **Pygame Community Edition**. 

This project isolates higher-dimensional mathematics, data containment models, and state controllers to compute, rotate, and project complex 8-dimensional geometric dataset point clouds down to an interactive 2D user matrix window.

---

## 🛠️ Software Architecture Breakdown

The program transitions out of a standard script into a fully containerized, modular class architecture:

* **`SimulationState` (Data Container):** A decoupled data model class managing global time tracking variables, speed constraints, rotational increments, and boolean control configurations.
* **`Theme` (Data Container):** A frozen dataclass model managing independent RGB color configurations to isolate graphics logic from background state changes.
* **`HyperBall` (Geometry Class):** Controls high-dimensional structural shape setups. It handles random Gaussian core point distribution algorithms and retains isolated positional tracking data.
* **`HyperspaceVisualizer` (Core Pipeline Engine):** The master coordinator application containing individual system routines for event polling, state updates, coordinate tracking, and screen rendering passes.

---

## 🚀 Engine Core Features

* **Planar Hyperspace Interlock Engine:** Calculates simultaneous matrix transformations across 4 unique 8-dimensional axes (X₁ through X₈) using a centralized trigonometric computation module.
* **Dual Projection Rendering Streams:** Dynamically switches mathematical pipelines between a strict, linear **Orthographic Slice** map and a depth-scaled **Perspective Distortion** layout.
* **Decoupled Intersection Core Entity:** Isolates the mathematical center overlapping path of the shapes into a distinct **Pure White Core Sphere** that navigates on its own loop track.
* **Structural Mesh Wireframes:** Interweaves low-alpha wire segments sequentially through neighboring particle junctions to draw an analytical mesh grid cage.
* **Telemetry Control HUD Dashboard:** Displays metrics tracking rendering profiles, visual presets, real-time pixel distances, and separate particle speed tracks.

---

## 🎮 Interface & Interactive Command Keybinds

Manage the projection tracking configurations in real time using interactive keyboard controls:

| Hardware Key Input | UI Dashboard Action |
| :--- | :--- |
| **`SPACEBAR`** | **Master Simulation Pause** (Freezes or resumes spatial coordinate timeline steps). |
| **`P`** | **Toggle Projection Style** (Instantly flips graphic math between *Perspective* and *Orthographic* modes). |
| **`UP / DOWN ARROWS`** | **Adjust Cloud Velocity** (Throttles the acceleration speed factor of the parent point clouds). |
| **`W / S`** | **Adjust Center Core Velocity** (Independently accelerates or brakes the orbit speed track of the inner white sphere). |
| **`M`** | **Toggle Wireframe Matrix** (Draws or hides the analytical line grids between nearest node vertices). |
| **`T`** | **Cycle System Themes** (Morphs colors through *Deep Space*, *Matrix*, *Synthwave*, or *Mono* presets). |
| **`ESC`** | **Graceful System Terminate** (Clears open memory threads and safely terminates window execution loops). |

---

## ⚙️ Quick Start Compilation Instructions

### 1. Framework Installation
Verify your terminal has the modern, high-efficiency community framework extension built to compile stable loops under active Python runtimes:
```bash
pip install pygame-ce
```

### 2. Launch the Application
Run the centralized engine wrapper execution entry point script from your development directory terminal:
```bash
python hyperspace_visualizer.py
```
