# Adventure World Theme Park Simulation

## Project Report

**COMP1005 Fundamentals of Programming - Postgraduate Assignment**

**Student Name:** Riajul
**Assignment:** Adventure World Theme Park Simulation
**Semester:** 2, 2025
**Date:** October 16, 2025

---

## Table of Contents

1. [Overview](#1-overview)
2. [User Guide](#2-user-guide)
3. [Traceability Matrix](#3-traceability-matrix)
4. [Discussion](#4-discussion)
5. [Showcase](#5-showcase)
6. [Conclusion](#6-conclusion)
7. [Future Work](#7-future-work)
8. [References](#8-references)

---

## 1. Overview

### 1.1 Program Purpose

Adventure World is a theme park simulation system which shows the operation of a recreational facility with several ride attractions, autonomous patron agents, and queuing mechanisms. The simulation shows object-oriented programming principles, real-time visualization, and statistical analysis by the animation of patron behavior and ride operations.

### 1.2 Implemented Features

The simulation successfully implements the following core features:

**1. Multiple Ride Types**

- Rotating Ferris wheel
- Swinging pirates ship
- Bumper Cars with circular arena movement
- Roller Coaster (Tower Drop) with vertical track animation

**2. Autonomous Patron System**

- Target-based movement using vector mathematics
- State machine implementation (ROAMING, QUEUING, RIDING, LEAVING)
- Collision detection and avoidance
- Patience mechanism leading to park departure
- Random spawn points at designated entrances

**3. Queue Management System**

- FIFO (First-In-First-Out) queue implementation using Python deque
- Capacity enforcement per ride
- Visual queue representation
- State synchronization between patrons and rides

**4. Terrain and Boundaries**

- Park boundary enforcement
- Pathway visualization (horizontal and vertical)
- Entry/exit point system
- Bounding box collision detection for rides

**5. Dual User Interface Modes**

- Interactive mode with user prompts (`-i` flag)
- Batch mode with CSV configuration files (`-f` and `-p` flags)
- Command-line argument parsing using argparse

**6. Simulation Engine**

- Timestep-based discrete event simulation
- `step_change()` method for all entities
- 5-timestep patron initialization freeze (per specification)
- Probabilistic patron spawning

**7. Real-time Statistics (Postgraduate Requirement)**

- Dual subplot visualization (park map and statistics graph)
- Time-series tracking of patron states
- Summary statistics output
- Automatic visualization export to PNG

---

## 2. User Guide

### 2.1 System Requirements

- Python 3.6 or higher
- NumPy library
- Matplotlib library

### 2.2 Installation

```bash
# Install required dependencies
pip install numpy matplotlib

# Or using virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install numpy matplotlib
```

### 2.3 Running the Simulation

#### Interactive Mode

Run with user prompts for configuration:

```bash
python3 adventureworld.py -i
```

The program will prompt for:

- Park dimensions (width and height)
- Number of each ride type (Ferris Wheel, Pirate Ship, Bumper Cars, Roller Coaster)
- Initial patron count
- Maximum simulation timesteps

#### Batch Mode

Run with pre-configured CSV files:

```bash
python3 adventureworld.py -f map1.csv -p parameters.csv
```

Where:

- `map1.csv` defines ride positions and properties
- `parameters.csv` defines simulation parameters

#### GUI Animation Mode

For code editor like VS Code or Jupyter, force GUI mode:

```bash
python3 adventureworld.py -i --gui
```

### 2.4 Configuration File Formats

**Map File (map.csv):**

```csv
ride_type,x,y,param1,param2,capacity,duration,name
FerrisWheel,50,150,20,0,8,80,Ferris Wheel
RollerCoaster,150,150,20,60,6,60,Tower Drop
```

**Parameter File (parameters.csv):**

```csv
parameter,value
park_width,200
park_height,200
max_timesteps,400
initial_patrons,10
```

### 2.5 Output

- **Console:** Shows the real time data with statistics.
- **Visualization:** `simulation_result.png` shows the park layout with a graph
- **Statistics:** Number of Patron , ride utilization, queue lengths

---

## 3. Traceability Matrix

| Feature                        | Code Reference                                                                                                              | Test Method                                                   | Test Result | Completion Date |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ----------- | --------------- |
| **1. Base Ride Class**         | `adventureworld.py:20-122` - `class Ride` with state management (IDLE, LOADING, RUNNING), bounding boxes, overlap detection | Tested by running all ride types, verifying state transitions | **Pass**    | Oct 15, 2025    |
| **2. Ferris Wheel**            | `adventureworld.py:124-168` - `class FerrisWheel(Ride)` with rotation animation                                             | Visual verification of gondola rotation in output PNG         | **Pass**    | Oct 15, 2025    |
| **3. Pirate Ship**             | `adventureworld.py:171-228` - `class PirateShip(Ride)` with pendulum motion                                                 | Visual verification of swinging motion in output PNG          | **Pass**    | Oct 15, 2025    |
| **4. Bumper Cars**             | `adventureworld.py:231-291` - `class BumperCars(Ride)` with circular movement                                               | Visual verification of cars moving in arena                   | **Pass**    | Oct 15, 2025    |
| **5. Roller Coaster**          | `adventureworld.py:294-348` - `class RollerCoaster(Ride)` with vertical movement                                            | Visual verification of car moving up/down track               | **Pass**    | Oct 15, 2025    |
| **6. Patron Class**            | `adventureworld.py:351-478` - `class Patron` with state machine, movement algorithms                                        | Run simulation, verify patrons move and change states         | **Pass**    | Oct 15, 2025    |
| **7. Target-Based Movement**   | `adventureworld.py:397-459` - `_roam()` method with vector calculations                                                     | Tested by observing patron pathfinding to rides               | **Pass**    | Oct 16, 2025    |
| **8. Collision Detection**     | `adventureworld.py:58-70` - `is_in_bounds()` and `overlaps()` methods                                                       | Verified patrons don't enter ride bounding boxes              | **Pass**    | Oct 15, 2025    |
| **9. Queue System**            | `adventureworld.py:72-76, 88-108` - `add_to_queue()` and deque operations                                                   | Checked queue formation in console output and PNG             | **Pass**    | Oct 16, 2025    |
| **10. Theme Park Manager**     | `adventureworld.py:481-644` - `class ThemePark` with simulation loop                                                        | Run complete simulation, verify coordination                  | **Pass**    | Oct 15, 2025    |
| **11. Statistics Tracking**    | `adventureworld.py:565-575, 610-629` - Statistics history and plotting                                                      | Verified graphs show correct data trends                      | **Pass**    | Oct 15, 2025    |
| **12. File Loading**           | `adventureworld.py:647-724` - CSV parsers for maps and parameters                                                           | Tested batch mode with various CSV files                      | **Pass**    | Oct 15, 2025    |
| **13. Interactive Mode**       | `adventureworld.py:727-783` - User input prompts and validation                                                             | Tested with various input values                              | **Pass**    | Oct 15, 2025    |
| **14. Batch Mode**             | `adventureworld.py:786-812` - File-based configuration                                                                      | Tested with map1.csv and parameters.csv                       | **Pass**    | Oct 15, 2025    |
| **15. Command-Line Interface** | `adventureworld.py:876-915` - argparse implementation with -i, -f, -p, --gui flags                                          | Tested all flag combinations                                  | **Pass**    | Oct 16, 2025    |
| **16. Headless Detection**     | `adventureworld.py:821-856` - Backend detection and PNG export                                                              | Tested in terminal and VS Code environments                   | **Pass**    | Oct 16, 2025    |
| **17. 5-Timestep Freeze**      | `adventureworld.py:375-384` - `frozen_time` check in patron step                                                            | Verified patrons don't move for first 5 steps                 | **Pass**    | Oct 15, 2025    |

---

## 4. Discussion

### 4.1 System Architecture

The Adventure World simulation is followed by an object-oriented design pattern. There are three primary classes:

#### 4.1.1 Ride Hierarchy

The `Ride` base class reflects common functional for all attractions, including:

- State management (IDLE → LOADING → RUNNING → IDLE cycle)
- Bounding box calculations to detect collision
- Python's `collections.deque` for managing queue
- Abstract `_calculate_angle()` method for indiviudal subclass animations.

Four concrete ride classes is dervied class of `Ride`:

- **FerrisWheel:** Using trigonometry with multiple gondolas position for 360 degree contnuous rotation.
- **PirateShip:** for realistic pendulum swinging, used sinusoidal motion.
- **BumperCars:** Features circular movement patterns for multiple cars in an arena
- **RollerCoaster:** for tower drop simulation implemented vertical oscillation

#### 4.1.2 Patron Agent System

The `Patron` class implements agent behavior through:

- **State Machine:** Four types of patron controlling (ROAMING, QUEUING, RIDING, LEAVING) behavior
- **Target-Based Movement:** Uses vector mathematics for smooth navigation toward rides or exit points
- **Collision Avoidance:** Verify `ThemePark.is_valid_position()` before individual movement step
- **Patience Mechanism:** Accumulated patience counter triggers park departure after threshold

#### 4.1.3 Theme Park Manager

The `ThemePark` class works as the simulation coordinator:

- Manages collections of rides and visitors
- Runs the main simulation cycle using the step() function
- Includes validation methods to check positions and detect overlaps
- Collects and updates performance statistics at every time interval
- Oversees graphical display using matplotlib for visualization

### 4.2 UML Class Diagram

```
┌─────────────────────────┐
│      ThemePark          │
├─────────────────────────┤
│ - width: int            │
│ - height: int           │
│ - rides: List[Ride]     │
│ - patrons: List[Patron] │
│ - exits: List[Tuple]    │
│ - timestep: int         │
│ - stats_history: Dict   │
├─────────────────────────┤
│ + add_ride()            │
│ + add_patron()          │
│ + step()                │
│ + plot()                │
│ + is_valid_position()   │
└───────────┬─────────────┘
            │ contains
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
┌─────────┐    ┌──────────┐
│  Ride   │    │  Patron  │
├─────────┤    ├──────────┤
│ - x,y   │    │ - x,y    │
│ - state │    │ - state  │
│ - queue │    │ - speed  │
├─────────┤    ├──────────┤
│+ plot() │    │+ _roam() │
│+ step_  │    │+ plot()  │
│  change │    └──────────┘
└────┬────┘
     │ inherits
     │
  ┌──┴───┬────────┬──────────┐
  ▼      ▼        ▼          ▼
┌────┐ ┌────┐ ┌────┐  ┌─────────┐
│FW  │ │PS  │ │BC  │  │RC       │
└────┘ └────┘ └────┘  └─────────┘
```

### 4.3 Key Design Decisions

#### 4.3.1 Continuous Animation

Each ride keeps animating at all times, even when no one is on it, to maintain visual activity and show that the simulation is still running. This is done by adjusting self.angle in every step_change() execution, regardless of whether the ride is occupied or not.

#### 4.3.2 Vector-Based Movement

Patrons use normalized direction vectors for smooth movement:

```python
dx = target_x - self.x
dy = target_y - self.y
dist = sqrt(dx² + dy²)
new_x = x + speed * (dx / dist)
new_y = y + speed * (dy / dist)
```

This provides natural-looking navigation compared to grid-based movement.

#### 4.3.3 Deque for Queue Management

Python's `collections.deque` was chosen for O(1) append and popleft operations, essential for efficient FIFO queue processing:

```python
self.queue = deque()
self.queue.append(patron)    # O(1)
patron = self.queue.popleft() # O(1)
```

#### 4.3.4 Probabilistic Spawning

New patrons spawn with 20% probability per timestep (when below capacity), creating realistic variable arrival rates rather than deterministic spawning.

### 4.4 Implementation Challenges and Solutions

**Challenge 1: Patrons Not Joining Queues**

- **Problem:** At first, patrons rarely joined any rides because the probability was set too low (2%) and the distance limit (15 units) was too short. As a result, almost no rides were used during the simulation.
- **Solution:** The probability was raised to 8%, and the distance threshold was extended to 35 units. This adjustment also considered the ride’s bounding box area, making it easier for patrons to detect and join nearby rides.

**Challenge 2: Headless Environment Detection**

- **Problem:** When running in a headless setup, matplotlib automatically switched to a non-interactive backend, which caused the visual display to fail quietly.
- **Solution:** A detection system was added to check the backend in use, along with a --gui flag that forces the TkAgg backend when a graphical interface is available.

**Challenge 3: Animation Not Running**

- **Problem:** In non-interactive backends, plt.show() doesn’t block execution, preventing the animation from running as expected.
- **Solution:** The issue was fixed by implementing two different execution modes — a manual time-step loop for headless environments and FuncAnimation for GUI-based execution.

---

## 5. Showcase

### 5.1 Introduction

To highlight how the simulation performs and adapts under different conditions, three separate setups were designed and tested. Each scenario focuses on evaluating specific features of the system:

**Scenario 1: Standard Park**

- Setup: map1.csv with parameters.csv
- Goal: Serve as a baseline run using balanced settings
- Focus: Ensure all essential components work as intended

**Scenario 2: Extended Park**

- Setup: map2.csv with parameters2.csv
- Goal: Assess performance and scalability with a larger park layout and longer runtime
- Focus: Observe how the system handles greater complexity and workload

**Scenario 3: Interactive Configuration**

- Setup: User-defined through the interactive configuration mode
- Goal: Demonstrate the system’s flexibility in accepting user inputs
- Focus: Show how easily the simulation can adapt to custom settings

All scenarios were executed using the command:

```bash
python3 adventureworld.py -f <map_file> -p <param_file>
```

Statistics were recorded from console output and visualization was captured in `simulation_result.png`.

### 5.2 Scenario 1: Standard Park

#### Configuration

**Command:**

```bash
python3 adventureworld.py -f map1.csv -p parameters.csv
```

**Parameters:**

- Park dimensions: 200 × 200 units
- Rides: 4 (Ferris Wheel, Pirate Ship, Bumper Cars, Tower Drop)
- Initial patrons: 10
- Maximum timesteps: 400
- Duration: ~30 seconds

#### Results

**Console Output Summary:**

```
Total timesteps: 400
Total patrons entered: 33
Total patrons left: 3
Patrons still in park: 30
Total rides taken: 69

Ride Statistics:
  Ferris Wheel: 8 riders, queue: 4, state: RUNNING
  Tower Drop: 14 riders, queue: 2, state: RUNNING
  Bumper Cars: 19 riders, queue: 4, state: RUNNING
  Pirate Ship: 28 riders, queue: 1, state: RUNNING
```

**Visualization Analysis:**

- The four rides appear clearly at the park’s corners — around coordinates (50,150), (150,150), (50,50), and (150,50).
- Patrons, represented by small colored dots, are scattered across the park area.
- Queues are shown as colored squares positioned near each ride.
- The statistics chart displays the following trends:
  - Blue line (Total Patrons): Rises from about 10 to nearly 30 within the first 100 timesteps, then levels off.
  - Orange line (In Queue): Moves up and down between roughly 3 and 13 patrons.
  - Green line (On Rides): Fluctuates within the range of 8 to 14 patrons.

**Discussion:**
This test confirms that the main components of the simulation are operating correctly. Among the rides, the Pirate Ship attracted the most attention, recording 28 total riders. Its higher capacity (10 patrons) and moderate ride duration (50 timesteps) likely contributed to this popularity. The total number of patrons eventually stabilized at around 30, suggesting a healthy balance between new arrivals and those leaving after waiting. Queue sizes stayed moderate, usually between one and four patrons, showing that ride capacity and timing were well-managed. The steady non-zero values in both queuing and riding statistics verify that patrons are moving through the system properly — finding rides, waiting in line, and completing ride sessions as intended.

### 5.3 Scenario 2: Extended Park

#### Configuration

**Command:**

```bash
python3 adventureworld.py -f map2.csv -p parameters2.csv
```

**Parameters:**

- Park dimensions: 220 × 220 units
- Rides: 6 (2 Ferris Wheels, 1 Tower Drop, 2 Bumper Cars, 1 Pirate Ship)
- Initial patrons: 15
- Maximum timesteps: 600
- Duration: ~45 seconds

#### Results

**Console Output Summary:**

```
Total timesteps: 600
Total patrons entered: 48
Total patrons left: 12
Patrons still in park: 36
Total rides taken: 127

Ride Statistics:
  Sky Wheel: 18 riders, queue: 3, state: RUNNING
  Wonder Wheel: 22 riders, queue: 2, state: RUNNING
  Drop Tower: 21 riders, queue: 1, state: RUNNING
  Crash Arena: 28 riders, queue: 4, state: RUNNING
  Bump Zone: 24 riders, queue: 3, state: RUNNING
  Sea Storm: 14 riders, queue: 2, state: IDLE
```

**Discussion:**
This extended test scenario shows that the system scales efficiently under increased workload. When the park was configured with 50% more rides and the simulation ran for 50% longer, the total number of completed ride cycles rose by about 84% (127 compared to 69) — all without any noticeable drop in performance. The two Ferris Wheels helped balance demand evenly, handling 18 and 22 riders each, which prevented any single ride from becoming overloaded.

The expanded park layout (220×220) also gave enough room for 36 active patrons to move around freely, avoiding crowding issues. On average, each ride served 21.2 patrons, which is higher than in Scenario 1 (17.3), showing that the system achieved better overall throughput. Queue handling stayed consistent, with the longest queue reaching just four patrons, proving that the scaling maintained proper load distribution. Having one ride end in an IDLE state by the simulation’s conclusion is normal, as timing differences naturally occur between ride cycles.

### 5.4 Scenario 3: Interactive Configuration

#### Configuration

**Command:**

```bash
python3 adventureworld.py -i
```

**User Inputs:**

- Park width: 200
- Park height: 200
- Ferris Wheels: 1
- Pirate Ships: 1
- Bumper Cars: 1
- Roller Coasters: 1
- Initial patrons: 10
- Max timesteps: 400

#### Results

**Console Output Summary:**

```
Total timesteps: 400
Total patrons entered: 31
Total patrons left: 2
Patrons still in park: 29
Total rides taken: 74

Ride Statistics:
  Ferris Wheel: 16 riders, queue: 2, state: RUNNING
  Pirate Ship: 22 riders, queue: 1, state: RUNNING
  Bumper Cars: 26 riders, queue: 3, state: RUNNING
  Roller Coaster: 10 riders, queue: 0, state: RUNNING
```

**Discussion:**
The interactive mode highlights how well the user interface works in practice. Although the setup was similar to Scenario 1, small differences in outcomes (74 rides versus 69) reflect the random nature of patron arrivals and their movement choices. The command-line interface correctly checked user inputs and created the corresponding ride objects on the fly. This approach gives users the freedom to adjust parameters and test different configurations without needing to change the code or CSV files, making it ideal for experimentation and iterative testing.

### 5.5 Comparative Analysis

| Metric                       | Scenario 1 | Scenario 2 | Scenario 3 |
| ---------------------------- | ---------- | ---------- | ---------- |
| Rides                        | 4          | 6          | 4          |
| Timesteps                    | 400        | 600        | 400        |
| Total Rides Taken            | 69         | 127        | 74         |
| Avg Rides/Attraction         | 17.3       | 21.2       | 18.5       |
| Max Patron Count             | 30         | 36         | 29         |
| Throughput (rides/100 steps) | 17.3       | 21.2       | 18.5       |

**Key Observations:**

1. **Linearity:** Ride usage tends to grow roughly in proportion to the number of timesteps (127/600 ≈ 69/400).
2. **Capacity:** Adding more rides increases overall ride completions without significantly raising the peak number of patrons in the park.
3. **Stochasticity:** Even with similar setups, results varied by 5–7% due to the probabilistic nature of patron arrival and movement.
4. **Stability:** Across all scenarios, patron numbers remained steady, with no uncontrolled growth observed.

---

## 6. Conclusion

The Adventure World theme park simulation effectively demonstrates the practical use of object-oriented programming, discrete event simulation, and real-time data visualization. All seven assignment requirements were successfully implemented and validated:

**Achievements:**

1. ✅ Four unique ride types, each with distinct animation patterns.
2. ✅ Autonomous patron agents exhibiting state-based behavior.
3. ✅ Efficient queue management using suitable data structures.
4. ✅ Park terrain with collision detection and clearly defined pathways.
5. ✅ Two user interface modes: interactive and batch.
6. ✅ Fully functional simulation engine executing accurate timestep progression.
7. ✅ Real-time statistics visualized in subplot format, meeting postgraduate requirements.

**Code Quality:**
The code follows PEP-8 standards, avoids discouraged practices such as while True, break, continue, and global variables, and includes thorough documentation through docstrings. Its modular structure makes testing straightforward and future enhancements easier to implement.

**Performance:**
The simulation runs efficiently, completing 400–600 timesteps in roughly 30–45 seconds on standard hardware. Analysis shows consistent results across scenarios, with expected variations arising from stochastic elements.

**Reflection:**
This project reinforced foundational programming concepts like inheritance, polymorphism, encapsulation, and algorithmic thinking. Debugging initial issues with patron movement (where no rides were being taken) emphasized the importance of systematic testing and careful parameter adjustments.

Overall, the simulation provides a realistic computational model of a theme park, showcasing how programming fundamentals can be applied to simulate and analyze complex real-world systems.

---

## 7. Future Work

Several improvements could be introduced to make the simulation more sophisticated and closer to real-world park operations:

### 7.1 Smarter Pathfinding

**Current:** Patrons move toward targets using simple vector calculations.
**Enhancement:** Integrate the A\* pathfinding algorithm to allow patrons to navigate intelligently around obstacles and crowded areas. This would help them choose optimal routes considering both distance and congestion.

### 7.2 Loading Dynamic Terrain from Files

**Current:** Pathways and park features are hardcoded in the `ThemePark.plot()` method
**Enhancement:** Load park elements such as barriers, benches, or food stalls from external CSV files:

```csv
terrain_type,x,y,width,height
barrier,100,50,10,100
bench,75,75,5,5
```

This would allow for flexible park layouts without changing the source code.

### 7.3 Patron Ride Preferences

**Current:** Patrons randomly select from available rides.
**Enhancement:** Assign weighted preferences to patrons, reflecting attraction choices based on individual interests:

```python
self.preferences = {
    'FerrisWheel': random.uniform(0.5, 1.5),
    'PirateShip': random.uniform(0.5, 1.5),
    # ...
}
```

This models more realistic decision-making, where certain rides are favored over others.

### 7.4 Economic Modeling

**Current:** No monetary or financial tracking is included.
**Enhancement:** Introduce ticket pricing, operational costs, and revenue calculation. This would allow analysis of profitability and enable optimization of ride pricing or placement through parameter sweeps.

### 7.5 Weather and Environmental Effects

**Current:** Park conditions are static.
**Enhancement:** Add dynamic weather states (sunny, rainy, night) that influence patron arrival rates, patience levels, and ride availability. This would introduce time-dependent behavior and add realism.

### 7.6 Automated Parameter Sweeps

**Current:** Each simulation run is performed individually.
**Enhancement:** Implement an automated batch runner that systematically varies parameters to explore outcomes:
```python
for num_rides in range(3, 8):
    for num_patrons in range(10, 30, 5):
        run_simulation(num_rides, num_patrons)
        collect_statistics()
```

This would allow statistical analysis of different configurations and help determine optimal park settings.

### 7.7 3D Visualization

**Current:** Visualizations are limited to 2D using matplotlib.
**Enhancement:** Upgrade to 3D graphics using matplotlib's mplot3d module or external libraries like Pygame or PyOpenGL, providing a more immersive and realistic representation of rides and park layout.

---

## 8. References

### Course Materials

1. COMP1005 Lecture Slides - "Object-Oriented Programming in Python" (Weeks 4-6, 2025)
2. COMP1005 Practical Test 3 - "Pirate Ship Animation" (provided code basis for ride movement patterns)
3. COMP1005 Practical Exercises - "Pet Shelter Queue Management" (informed queue implementation)

### Assignment Documentation

4. COMP1005 Assignment Specification v1.0 - "Adventure World" (Semester 2, 2025)

### External Documentation

5. Python Software Foundation. (2025). _Python 3.12 Documentation_. Retrieved from https://docs.python.org/3/
6. Hunter, J. D. (2007). "Matplotlib: A 2D Graphics Environment". _Computing in Science & Engineering_, 9(3), 90-95.
7. Harris, C. R., et al. (2020). "Array programming with NumPy". _Nature_, 585, 357-362.

### Style Guides

8. van Rossum, G., Warsaw, B., & Coghlan, N. (2001). _PEP 8 – Style Guide for Python Code_. Python.org. Retrieved from https://www.python.org/dev/peps/pep-0008/

---

**Word Count:** Approximately 4,200 words
**Page Count:** Approximately 11 pages (with diagrams and tables)

**Author:** Riajul
**Student ID:** [Your Student ID]
**Date Submitted:** October 16, 2025

---

## Appendix A: Code Snippet Examples

### A.1 Ride State Transition Logic

```python
def step_change(self):
    self.time_counter += 1
    self.angle = self._calculate_angle()

    if self.state == "IDLE" and len(self.queue) > 0:
        self.state = "LOADING"
    elif self.state == "LOADING":
        while len(self.riders) < self.capacity and len(self.queue) > 0:
            patron = self.queue.popleft()
            self.riders.append(patron)
            patron.state = "RIDING"
            self.total_riders += 1
        if len(self.riders) > 0:
            self.state = "RUNNING"
            self.time_counter = 0
    elif self.state == "RUNNING":
        if self.time_counter >= self.duration:
            for rider in self.riders:
                rider.state = "ROAMING"
                rider.target_ride = None
            self.riders = []
            self.state = "IDLE"
```

### A.2 Patron Movement Algorithm

```python
def _roam(self):
    if self.target_ride is None and np.random.random() < 0.08:
        available_rides = [r for r in self.park.rides if len(r.queue) < 8]
        if available_rides:
            self.target_ride = np.random.choice(available_rides)
            self.target_x = self.target_ride.x
            self.target_y = self.target_ride.y

    if self.target_ride is not None:
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = np.sqrt(dx**2 + dy**2)

        if dist < 35:
            self.target_ride.add_to_queue(self)
            self.rides_taken += 1
            self.patience = 0
            return

        new_x = self.x + self.speed * (dx / dist)
        new_y = self.y + self.speed * (dy / dist)

        if self.park.is_valid_position(new_x, new_y):
            self.x = new_x
            self.y = new_y
```

---

**END OF REPORT**
