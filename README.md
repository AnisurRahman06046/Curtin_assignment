# Adventure World Theme Park Simulation

**COMP1005 Assignment - Postgraduate**
**Author:** Riajul

A theme park simulation with rides, patrons, queues, and real-time statistics.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install numpy matplotlib
```

### 2. Run the Simulation

**Interactive Mode:**
```bash
python3 adventureworld.py -i
```
Enter values when prompted (or press Enter for defaults).

**Batch Mode:**
```bash
python3 adventureworld.py -f map1.csv -p parameters.csv
```

**With Animation (VS Code/Jupyter):**
```bash
python3 adventureworld.py -i --gui
```

---

## 📋 How to Test

### Test 1: Standard Scenario
```bash
python3 adventureworld.py -f map1.csv -p parameters.csv
```
- 4 rides (Ferris Wheel, Pirate Ship, Bumper Cars, Roller Coaster)
- 10 patrons, 400 timesteps
- Should complete in ~30 seconds
- Creates `simulation_result.png`

**Expected Output:**
- Total rides taken: 50-100
- All 4 rides show activity
- Queuing/Riding statistics visible

### Test 2: Extended Scenario
```bash
python3 adventureworld.py -f map2.csv -p parameters2.csv
```
- 6 rides, 15 patrons, 600 timesteps
- Longer simulation (~45 seconds)
- More patron activity

### Test 3: Interactive Mode
```bash
python3 adventureworld.py -i
```
Enter these values:
- Park width: `200`
- Park height: `200`
- Ferris Wheels: `1`
- Pirate Ships: `1`
- Bumper Cars: `1`
- Roller Coasters: `1`
- Initial patrons: `10`
- Max timesteps: `400`

---

## 📊 What You'll See

**Console Output:**
```
============================================================
ADVENTURE WORLD - BATCH MODE
============================================================
Park loaded with 4 rides and 10 patrons!
Starting simulation...

Running in headless mode (no display)...
Progress: 0...50...100...150...200...250...300...350...400 - Complete!

Final visualization saved to: simulation_result.png
============================================================
SIMULATION COMPLETE
============================================================
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

**Visual Output (`simulation_result.png`):**
- Left: Theme park with 4 animated rides
- Right: Statistics graph showing patron activity
- Colored dots = patrons roaming
- Colored squares = patrons in queues

---

## 🎮 Command Options

```bash
# Show help
python3 adventureworld.py --help

# Interactive mode
python3 adventureworld.py -i

# Batch mode
python3 adventureworld.py -f <map_file> -p <param_file>

# Force GUI/animation window
python3 adventureworld.py -i --gui
python3 adventureworld.py -f map1.csv -p parameters.csv --gui
```

---

## 📁 Configuration Files

### Map Files (Define Rides)

**Format:**
```csv
ride_type,x,y,param1,param2,capacity,duration,name
```

**Example (`map1.csv`):**
```csv
FerrisWheel,50,150,20,0,8,80,Ferris Wheel
RollerCoaster,150,150,20,60,6,60,Tower Drop
BumperCars,50,50,40,35,8,70,Bumper Cars
PirateShip,150,50,30,0,10,50,Pirate Ship
```

### Parameter Files (Define Simulation Settings)

**Format:**
```csv
parameter,value
```

**Example (`parameters.csv`):**
```csv
park_width,200
park_height,200
max_timesteps,400
initial_patrons,10
```

---

## ✅ Success Checklist

Your simulation works correctly if:

- ✅ No Python errors
- ✅ Completes all timesteps
- ✅ Creates `simulation_result.png`
- ✅ Total rides taken > 50
- ✅ All rides show "RUNNING" or "IDLE"
- ✅ Orange/green lines in graph show activity (not flat at 0)

---

## 🐛 Troubleshooting

**"ModuleNotFoundError: No module named 'numpy'"**
```bash
pip install numpy matplotlib
```

**No animation window appears**
- Add `--gui` flag
- Or view `simulation_result.png` directly

**"Total rides taken: 0"**
- Update to latest code (this bug is fixed)

**Animation too slow/fast**
- Edit `interval=50` in `run_simulation()` function (line ~875)

---

## 📦 Submission Files

For assignment submission:
```
FOP_Assignment_<student_id>.zip containing:
├── adventureworld.py
├── map1.csv
├── map2.csv
├── parameters.csv
├── parameters2.csv
├── README.md
└── report.pdf (your project report)
```

---

## 🎯 Features Implemented

1. **Rides** - 4 types with animations
2. **Patrons** - Autonomous agents with state machines
3. **Queues** - FIFO queue management with capacity limits
4. **Terrain** - Boundaries, pathways, collision detection
5. **UI** - Interactive (`-i`) and Batch (`-f`, `-p`) modes
6. **Simulation** - Proper timestep execution
7. **Statistics** - Real-time graphs (Postgrad requirement)

---

## 📚 References

- COMP1005 Practical Test 3 - Pirate Ship
- COMP1005 Assignment Specification v1.0

---

**Last Updated:** 2025-10-16
