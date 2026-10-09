# 🌌 High-Performance 8D Hyperspace Projection Engine & Stream Sandbox

A high-efficiency, interactive real-time graphics visualization pipeline and viewport simulator built with **Python** and **Pygame Community Edition**. This framework generates random Gaussian particle coordinate distributions across an 8-dimensional hyperspace matrix (X₁ through X₈), subjects them to multi-planar rotation math, and projects the dataset onto an interactive 2D telemetry dashboard containing soft screen-space alpha glow rings.

This edition introduces **dynamic data stream injection matrices**, allowing you to dynamically add, strip, or target coordinate structures inside the live running hyperspace environment.

---

## 🚀 Next-Gen Data Stream Architecture

* **Dynamic In-Stream Injector (`AddStream`):** Features an interactive coordinate generator that introduces a fresh cluster stream (+20 new 8D particles) into the system timeline, complete with a parabolic alpha fade lifespan.
* **Localized Particle Stripper (`RemoveStream`):** Spawns an algorithmic removal pulse that dynamically calculates Euclidean distance checks natively across 8 dimensions to strip out the 18 nearest vertices from an active ball cluster.
* **Target Isolation Controller (`[U]`):** Binds system targeting to alternate between `AUTO` (randomizing stream targets), forcing updates exclusively on `BALL_A`, or forcing updates on `BALL_B`.
* **Double-Ended Queue Buffers (`deque`):** Tracks streaming profiles safely inside memory-capped arrays (`maxlen=30`) to avoid hardware performance degradation or coordinate overflow loops.
* **Categorized HUD Hint Controller:** Restructures the control layout by dividing commands cleanly into custom sub-categories (*Stream*, *View*, *UI*, and *Navigation*) printed across grouped telemetry channels.

---

## 🎮 Sandbox Mouse & Hardware Interlocks

Take absolute control over the high-dimensional viewing space using physical inputs:

### 🖱️ Mouse Telemetry Mapping
* **`LEFT CLICK + DRAG`** ➔ **Pan Viewport Camera:** Shifts the display frame along the X₁/X₂ grid axes.
* **`SCROLL WHEEL UP`** ➔ **Zoom In System Scale:** Magnifies rendering scale up to a clear 5.0x bounds cap.
* **`SCROLL WHEEL DOWN`** ➔ **Zoom Out System Scale:** Condenses scale limits down to a minimum 0.1x overview profile.

### ⌨️ Categorized Key Bindings

| Input Class | Hotkey | Operational Sandbox Command |
| :--- | :--- | :--- |
| **STREAM** | **`I`** | **Inject Node Stream:** Pumps a fresh 20-particle 8D vector tracking stream into the active target ball (0.35s cooldown). |
| | **`O`** | **Removal Pulse:** Triggers a stripping pulse to erase up to 18 nearby particles from the target ball (0.40s cooldown). |
| | **`U`** | **Cycle Target Mode:** Shifts the active target pathing loop between `AUTO`, `BALL_A`, and `BALL_B`. |
| **VIEW** | **`UP / DOWN`** | **Adjust Cloud Warp:** Accel-brakes the spinning rotation factor of parent particle clouds. |
| | **`W / S`** | **Adjust Core Velocity:** Accel-brakes only the independent central white intersection core. |
| | **`P`** | **Toggle Projection Style:** Flips math pipelines between *Perspective* (Z-depth) and *Orthographic* (Flat) slice arrays. |
| | **`M`** | **Toggle Wireframe Matrix:** Draws or hides connecting mesh vectors between neighbor nodes. |
| **UI** | **`T`** | **Cycle Environmental Theme:** Morphs display colors across 8 built-in neon profiles. |
| | **`C`** | **Cycle Core Color Profile:** Switches the visual spectrum color of the inner center core ball. |
| | **`R`** | **Reset Camera:** Snaps panning tracking offsets and zoom levels back to default 1.0x zero vectors. |
| | **`SPACEBAR`** | **Master Simulation Pause:** Freezes all spatial rotation calculations instantly. |
| | **`ESC`** | **System Terminate:** Safely cleans active resource layers and exits the program. |

---

## ⚙️ Quick Start Compilation Instructions

### 1. Framework Installation
Verify your console has the modern community graphics extension built to run smooth loops under active Python environments:
```bash
pip install pygame-ce
```

### 2. Execution Entry Point
Run your master visualization dashboard file directly from your terminal:
```bash
python hyperspace_visualizer.py
```
