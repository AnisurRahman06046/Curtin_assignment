#!/usr/bin/env python3
"""
Adventure World Theme Park Simulation
COMP1005 Assignment - Postgraduate
Author: Riajul
Description: A theme park simulation with multiple rides, patrons, queuing system,
             and real-time statistics visualization.
"""

import sys
import argparse

# Parse args early to check for --gui flag
if '--gui' in sys.argv or '--animate' in sys.argv:
    import matplotlib
    matplotlib.use('TkAgg')  # Force interactive backend

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from collections import deque
import csv


class Ride:
    """Base class for all theme park rides.

    Rides have states (IDLE, LOADING, RUNNING), manage queues, and handle riders.
    All rides must implement their own movement patterns via _calculate_angle().
    """

    def __init__(self, x, y, width, height, capacity, duration, name):
        """Initialize a ride with position, size, capacity and duration.

        Args:
            x, y: Center position of the ride
            width, height: Dimensions for bounding box
            capacity: Maximum number of riders
            duration: Number of timesteps the ride runs
            name: Display name of the ride
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.duration = duration
        self.name = name
        self.state = "IDLE"
        self.queue = deque()
        self.riders = []
        self.time_counter = 0
        self.total_riders = 0
        self.angle = 0
        self.queue_position = (x, y - height/2 - 3)

    def get_bounding_box(self):
        """Return the bounding box coordinates (x_min, x_max, y_min, y_max)."""
        half_w = self.width / 2
        half_h = self.height / 2
        return (self.x - half_w, self.x + half_w, self.y - half_h, self.y + half_h)

    def is_in_bounds(self, px, py):
        """Check if a point (px, py) is within the ride's bounding area."""
        x_min, x_max, y_min, y_max = self.get_bounding_box()
        padding = 5
        return (x_min - padding) <= px <= (x_max + padding) and \
               (y_min - padding) <= py <= (y_max + padding)

    def overlaps(self, other_ride):
        """Check if this ride overlaps with another ride."""
        x1_min, x1_max, y1_min, y1_max = self.get_bounding_box()
        x2_min, x2_max, y2_min, y2_max = other_ride.get_bounding_box()
        return not (x1_max < x2_min or x1_min > x2_max or
                   y1_max < y2_min or y1_min > y2_max)

    def add_to_queue(self, patron):
        """Add a patron to the ride's queue."""
        self.queue.append(patron)
        patron.state = "QUEUING"
        patron.target_ride = self

    def step_change(self):
        """Update ride state on each timestep.

        State transitions: IDLE -> LOADING -> RUNNING -> IDLE
        Rides always animate (continuous movement).
        """
        # Always animate rides
        self.time_counter += 1
        self.angle = self._calculate_angle()

        if self.state == "IDLE" and len(self.queue) > 0:
            self.state = "LOADING"
        elif self.state == "LOADING":
            # Load patrons up to capacity
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
                # Release riders
                for rider in self.riders:
                    rider.state = "ROAMING"
                    rider.target_ride = None
                self.riders = []
                self.state = "IDLE"
                self.time_counter = 0

    def _calculate_angle(self):
        """Calculate the current animation angle. Override in subclasses."""
        return 0

    def plot_queue(self, ax):
        """Visualize the queue as colored squares."""
        qx, qy = self.queue_position
        for i, patron in enumerate(list(self.queue)[:8]):
            square = patches.Rectangle((qx + i*2.5 - 10, qy - 1.5), 2, 2,
                                       facecolor=patron.color, edgecolor='black',
                                       linewidth=0.5)
            ax.add_patch(square)


class FerrisWheel(Ride):
    """Ferris Wheel ride with rotating gondolas."""

    def __init__(self, x, y, radius, capacity, duration, name="Ferris Wheel"):
        super().__init__(x, y, radius*2.5, radius*2.5, capacity, duration, name)
        self.radius = radius
        self.num_gondolas = 8

    def _calculate_angle(self):
        """Continuous rotation of the wheel."""
        return (self.time_counter * 360 / self.duration) % 360

    def plot(self, ax):
        """Draw the Ferris Wheel with rotating gondolas."""
        # Main wheel circle
        circle = patches.Circle((self.x, self.y), self.radius, linewidth=2,
                               edgecolor='darkslateblue', facecolor='none', zorder=3)
        ax.add_patch(circle)

        # Central hub
        hub = patches.Circle((self.x, self.y), self.radius*0.1, linewidth=1.5,
                            edgecolor='black', facecolor='gold', zorder=5)
        ax.add_patch(hub)

        # Gondolas
        for i in range(self.num_gondolas):
            angle = np.radians(i * (360/self.num_gondolas) + self.angle)
            x_end = self.x + self.radius * np.cos(angle)
            y_end = self.y + self.radius * np.sin(angle)
            ax.plot([self.x, x_end], [self.y, y_end], 'darkslateblue',
                   linewidth=1.5, zorder=3)
            gondola = patches.Circle((x_end, y_end), 2.5, facecolor='cornflowerblue',
                                    edgecolor='darkblue', linewidth=1, zorder=4)
            ax.add_patch(gondola)

        # Platform
        platform_width = self.radius * 0.6
        platform_height = 5
        platform_y = self.y - self.radius - platform_height
        platform = patches.Rectangle((self.x - platform_width/2, platform_y),
                                     platform_width, platform_height,
                                     facecolor='gray', edgecolor='darkgray',
                                     linewidth=1.5, zorder=2)
        ax.add_patch(platform)
        self.plot_queue(ax)


class PirateShip(Ride):
    """Pirate Ship ride with pendulum swinging motion."""

    def __init__(self, x, y, length, capacity, duration, name="Pirate Ship"):
        super().__init__(x, y, length*1.2, length*1.2, capacity, duration, name)
        self.length = length
        self.max_angle = 50

    def _calculate_angle(self):
        """Swinging motion using sine wave."""
        progress = self.time_counter / self.duration
        return self.max_angle * np.sin(2 * np.pi * progress * 2)

    def plot(self, ax):
        """Draw the Pirate Ship with swinging boat."""
        # Base platform
        base_width = self.length * 0.8
        base_height = 5
        base_y = self.y - self.length * 0.5
        platform = patches.Rectangle((self.x - base_width/2, base_y - base_height),
                                     base_width, base_height, facecolor='gray',
                                     edgecolor='darkgray', linewidth=1.5, zorder=2)
        ax.add_patch(platform)

        # Support structure
        height = self.length * 0.8
        triangle = np.array([[self.x - base_width/2, base_y],
                            [self.x + base_width/2, base_y],
                            [self.x, base_y + height]])
        support = patches.Polygon(triangle, closed=True, edgecolor='gray',
                                 facecolor='none', linewidth=2, zorder=3)
        ax.add_patch(support)

        # Pivot point
        pivot_y = base_y + height * 0.7
        ax.plot(self.x, pivot_y, 'ko', markersize=6, zorder=5)

        # Swinging arm and boat
        angle_rad = np.radians(self.angle)
        ship_x = self.x + (self.length/2.2) * np.sin(angle_rad)
        ship_y = pivot_y - (self.length/2.2) * np.cos(angle_rad)
        ax.plot([self.x, ship_x], [pivot_y, ship_y], 'gray', linewidth=4, zorder=3)

        # Boat shape
        boat_length, boat_height = 10, 5
        boat_points = np.array([[-boat_length/2, -boat_height/2],
                               [boat_length/2, -boat_height/2],
                               [boat_length/2 - 1.5, boat_height/2],
                               [-boat_length/2 + 1.5, boat_height/2]])
        cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)
        rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
        rotated_boat = boat_points @ rotation_matrix.T
        rotated_boat[:, 0] += ship_x
        rotated_boat[:, 1] += ship_y
        boat = patches.Polygon(rotated_boat, closed=True, facecolor='royalblue',
                              edgecolor='darkblue', linewidth=2, zorder=4)
        ax.add_patch(boat)
        self.plot_queue(ax)


class BumperCars(Ride):
    """Bumper Cars arena with circular movement pattern."""

    def __init__(self, x, y, width, height, capacity, duration, name="Bumper Cars"):
        super().__init__(x, y, width, height, capacity, duration, name)
        self.default_car_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'cyan']

    def _calculate_angle(self):
        """Circular motion for cars."""
        return (self.time_counter * 10) % 360

    def plot(self, ax):
        """Draw the Bumper Cars arena with moving cars."""
        x_min, x_max, y_min, y_max = self.get_bounding_box()

        # Arena layers
        outer = patches.Rectangle((x_min - 3, y_min - 3), self.width + 6,
                                  self.height + 6, linewidth=2.5, edgecolor='gray',
                                  facecolor='lightgray', alpha=0.4, zorder=2)
        ax.add_patch(outer)

        middle = patches.Rectangle((x_min - 1.5, y_min - 1.5), self.width + 3,
                                   self.height + 3, linewidth=2, edgecolor='slategray',
                                   facecolor='none', zorder=2)
        ax.add_patch(middle)

        arena = patches.Rectangle((x_min, y_min), self.width, self.height,
                                 linewidth=2.5, edgecolor='darkslategray',
                                 facecolor='#E8F5C8', alpha=0.8, zorder=2)
        ax.add_patch(arena)

        # Center marker when idle
        if self.state == "IDLE":
            center = patches.Circle((self.x, self.y), 3, facecolor='orange',
                                   edgecolor='darkorange', linewidth=1.5, zorder=3)
            ax.add_patch(center)

        # Always show moving cars
        if len(self.riders) > 0:
            # Show actual riders as cars
            for i, rider in enumerate(self.riders):
                angle = (self.angle + i * 360/len(self.riders)) % 360
                offset_x = self.width * 0.3 * np.cos(np.radians(angle))
                offset_y = self.height * 0.3 * np.sin(np.radians(angle))
                car = patches.Circle((self.x + offset_x, self.y + offset_y), 2,
                                    facecolor=rider.color, edgecolor='black',
                                    linewidth=1, zorder=4)
                ax.add_patch(car)
        else:
            # Show default cars when empty
            num_default_cars = len(self.default_car_colors)
            for i in range(num_default_cars):
                angle = (self.angle + i * 360/num_default_cars) % 360
                offset_x = self.width * 0.3 * np.cos(np.radians(angle))
                offset_y = self.height * 0.3 * np.sin(np.radians(angle))
                car = patches.Circle((self.x + offset_x, self.y + offset_y), 2,
                                    facecolor=self.default_car_colors[i],
                                    edgecolor='black', linewidth=1, zorder=4)
                ax.add_patch(car)

        self.plot_queue(ax)


class RollerCoaster(Ride):
    """Roller Coaster/Tower Drop ride with vertical movement."""

    def __init__(self, x, y, width, height, capacity, duration, name="Roller Coaster"):
        super().__init__(x, y, width, height, capacity, duration, name)

    def _calculate_angle(self):
        """Controls the vertical movement phase."""
        return (self.time_counter * 720 / self.duration) % 360

    def plot(self, ax):
        """Draw the Roller Coaster tower with moving car."""
        x_min, x_max, y_min, y_max = self.get_bounding_box()

        # Top platform
        platform = patches.Rectangle((x_min - 2, y_max - 4), self.width + 4, 4,
                                     facecolor='gold', edgecolor='darkorange',
                                     linewidth=2, zorder=3)
        ax.add_patch(platform)

        # Vertical track
        track_width = 8
        track = patches.Rectangle((self.x - track_width/2, y_min), track_width,
                                  self.height - 4, facecolor='slategray',
                                  edgecolor='darkgray', linewidth=2, zorder=2)
        ax.add_patch(track)

        # Center line
        ax.plot([self.x, self.x], [y_min, y_max - 4], 'white', linewidth=2,
               linestyle='--', alpha=0.8, zorder=2)

        # Support cubes
        for side in [-1, 1]:
            for i in range(3):
                cube_x = self.x + side * (track_width/2 + 5)
                cube_y = self.y + (i - 1) * 7
                cube = patches.Rectangle((cube_x - 2, cube_y - 2), 4, 4,
                                        facecolor='mediumseagreen',
                                        edgecolor='darkgreen', linewidth=1.5, zorder=3)
                ax.add_patch(cube)

        # Base platform
        base = patches.Rectangle((x_min - 2, y_min - 5), self.width + 4, 5,
                                facecolor='gray', edgecolor='darkgray',
                                linewidth=1.5, zorder=2)
        ax.add_patch(base)

        # Always show the car moving up and down
        progress = (self.time_counter % self.duration) / self.duration
        car_y = y_min + (self.height - 10) * (0.5 + 0.5 * np.sin(2 * np.pi * progress))
        car = patches.Rectangle((self.x - 4, car_y - 3), 8, 6, facecolor='red',
                                edgecolor='darkred', linewidth=2, zorder=5)
        ax.add_patch(car)

        self.plot_queue(ax)


class Patron:
    """Patron visiting the theme park.

    Patrons can roam around the park, join queues, ride attractions, and leave.
    They use target-based movement to navigate between rides.
    """

    def __init__(self, x, y, name, park):
        """Initialize a patron with position, name, and park reference."""
        self.x = x
        self.y = y
        self.name = name
        self.park = park
        self.state = "ROAMING"
        self.target_ride = None
        self.target_x = None
        self.target_y = None
        self.speed = 2.0
        self.patience = 0
        self.max_patience = 200
        self.rides_taken = 0
        self.color = np.random.choice(['red', 'blue', 'green', 'purple',
                                       'magenta', 'cyan', 'brown', 'pink',
                                       'orange', 'lime', 'navy', 'maroon'])
        self.frozen_time = 5  # Patrons don't move for first 5 timesteps
        self.stuck_counter = 0

    def step_change(self, timestep):
        """Update patron state and position on each timestep.

        Patrons are frozen for the first 5 timesteps as per specification.
        """
        if timestep < self.frozen_time:
            return

        self.patience += 1

        if self.state == "ROAMING":
            self._roam()
        elif self.state == "LEAVING":
            self._leave_park()

        # Leave if patience runs out
        if self.patience > self.max_patience and self.state == "ROAMING":
            self.state = "LEAVING"

    def _roam(self):
        """Roaming behavior: move toward rides or random locations."""
        # Decide to target a ride
        if self.target_ride is None and np.random.random() < 0.08:
            available_rides = [r for r in self.park.rides if len(r.queue) < 8]
            if available_rides:
                self.target_ride = np.random.choice(available_rides)
                self.target_x = self.target_ride.x
                self.target_y = self.target_ride.y

        if self.target_ride is not None:
            # Move toward target ride
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = np.sqrt(dx**2 + dy**2)

            if dist < 35:
                # Close enough to join queue
                self.target_ride.add_to_queue(self)
                self.rides_taken += 1
                self.patience = 0
                self.target_ride = None
                self.target_x = None
                self.target_y = None
                return

            if dist > 0:
                new_x = self.x + self.speed * (dx / dist)
                new_y = self.y + self.speed * (dy / dist)
                if self.park.is_valid_position(new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                    self.stuck_counter = 0
                else:
                    self.stuck_counter += 1
                    if self.stuck_counter > 10:
                        # Give up on this target
                        self.target_ride = None
                        self.target_x = None
                        self.target_y = None
                        self.stuck_counter = 0
        else:
            # Random roaming
            if self.target_x is None or np.random.random() < 0.05:
                self.target_x = np.random.uniform(20, self.park.width - 20)
                self.target_y = np.random.uniform(20, self.park.height - 20)

            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = np.sqrt(dx**2 + dy**2)

            if dist < 5:
                self.target_x = None
                self.target_y = None
            elif dist > 0:
                new_x = self.x + self.speed * (dx / dist)
                new_y = self.y + self.speed * (dy / dist)
                if self.park.is_valid_position(new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                else:
                    self.target_x = None
                    self.target_y = None

    def _leave_park(self):
        """Move toward nearest exit and despawn."""
        exit_x, exit_y = self.park.get_nearest_exit(self.x, self.y)
        dx = exit_x - self.x
        dy = exit_y - self.y
        dist = np.sqrt(dx**2 + dy**2)

        if dist < 3:
            self.park.remove_patron(self)
        else:
            self.x += self.speed * (dx / dist)
            self.y += self.speed * (dy / dist)

    def plot(self, ax):
        """Draw the patron as a colored circle."""
        if self.state in ["ROAMING", "LEAVING"]:
            ax.plot(self.x, self.y, 'o', color=self.color, markersize=7,
                   markeredgecolor='black', markeredgewidth=0.5, zorder=10)


class ThemePark:
    """Theme park containing rides, patrons, and simulation logic.

    Manages the overall simulation including spawning patrons, updating states,
    and tracking statistics.
    """

    def __init__(self, width=200, height=200):
        """Initialize the theme park with given dimensions."""
        self.width = width
        self.height = height
        self.rides = []
        self.patrons = []
        self.exits = [(10, height/2), (width-10, height/2)]
        self.timestep = 0
        self.patron_counter = 0
        self.total_patrons_entered = 0
        self.total_patrons_left = 0
        self.stats_history = {
            'timestep': [],
            'num_patrons': [],
            'num_queuing': [],
            'num_riding': [],
            'total_rides': []
        }

    def add_ride(self, ride):
        """Add a ride to the park if it doesn't overlap with existing rides."""
        for existing_ride in self.rides:
            if ride.overlaps(existing_ride):
                return False
        self.rides.append(ride)
        return True

    def add_patron(self):
        """Spawn a new patron at a random exit."""
        entry_x, entry_y = self.exits[np.random.randint(len(self.exits))]
        entry_x += np.random.uniform(-5, 5)
        entry_y += np.random.uniform(-10, 10)
        patron = Patron(entry_x, entry_y, f"P{self.patron_counter}", self)
        self.patron_counter += 1
        self.patrons.append(patron)
        self.total_patrons_entered += 1

    def remove_patron(self, patron):
        """Remove a patron from the park."""
        if patron in self.patrons:
            self.patrons.remove(patron)
            self.total_patrons_left += 1

    def is_valid_position(self, x, y):
        """Check if a position is valid (within bounds and not in a ride)."""
        if x < 5 or x > self.width - 5 or y < 5 or y > self.height - 5:
            return False
        for ride in self.rides:
            if ride.is_in_bounds(x, y):
                return False
        return True

    def get_nearest_exit(self, x, y):
        """Return the coordinates of the nearest exit."""
        return min(self.exits, key=lambda e: np.sqrt((e[0]-x)**2 + (e[1]-y)**2))

    def step(self):
        """Execute one simulation timestep.

        Order: spawn, update rides, update patrons, record statistics.
        """
        self.timestep += 1

        # Spawn new patrons with some probability
        if np.random.random() < 0.2 and len(self.patrons) < 30:
            self.add_patron()

        # Update all rides
        for ride in self.rides:
            ride.step_change()

        # Update all patrons
        for patron in list(self.patrons):
            patron.step_change(self.timestep)

        self._update_statistics()

    def _update_statistics(self):
        """Record statistics for current timestep."""
        num_queuing = sum(1 for p in self.patrons if p.state == "QUEUING")
        num_riding = sum(1 for p in self.patrons if p.state == "RIDING")
        total_rides = sum(r.total_riders for r in self.rides)

        self.stats_history['timestep'].append(self.timestep)
        self.stats_history['num_patrons'].append(len(self.patrons))
        self.stats_history['num_queuing'].append(num_queuing)
        self.stats_history['num_riding'].append(num_riding)
        self.stats_history['total_rides'].append(total_rides)

    def plot(self, ax):
        """Draw the theme park, rides, and patrons."""
        ax.clear()
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_title('Adventure World Theme Park', fontsize=14, fontweight='bold')
        ax.set_facecolor('lightgreen')

        # Draw pathways
        pathway_h = patches.Rectangle((0, self.height/2 - 10), self.width, 20,
                                     facecolor='#C8C8C8', edgecolor='none', zorder=1)
        ax.add_patch(pathway_h)

        pathway_v = patches.Rectangle((self.width/2 - 10, 0), 20, self.height,
                                     facecolor='#C8C8C8', edgecolor='none', zorder=1)
        ax.add_patch(pathway_v)

        # Draw exits
        for exit_x, exit_y in self.exits:
            exit_marker = patches.Rectangle((exit_x-3, exit_y-3), 6, 6,
                                           facecolor='gray', edgecolor='darkgray',
                                           linewidth=1.5, zorder=2)
            ax.add_patch(exit_marker)

        # Draw rides
        for ride in self.rides:
            ride.plot(ax)

        # Draw patrons
        for patron in self.patrons:
            patron.plot(ax)

    def plot_with_statistics(self, fig, ax_park, ax_stats):
        """Draw park and statistics subplots."""
        self.plot(ax_park)
        ax_stats.clear()

        if len(self.stats_history['timestep']) > 1:
            ax_stats.plot(self.stats_history['timestep'],
                         self.stats_history['num_patrons'],
                         label='Total Patrons', linewidth=2, color='blue')
            ax_stats.plot(self.stats_history['timestep'],
                         self.stats_history['num_queuing'],
                         label='Queuing', linewidth=2, color='orange')
            ax_stats.plot(self.stats_history['timestep'],
                         self.stats_history['num_riding'],
                         label='Riding', linewidth=2, color='green')
            ax_stats.set_xlabel('Timestep')
            ax_stats.set_ylabel('Number of Patrons')
            ax_stats.set_title('Park Statistics')
            ax_stats.legend(loc='upper left')
            ax_stats.grid(True, alpha=0.3)

    def print_summary(self):
        """Print final simulation statistics."""
        print("=" * 60)
        print("SIMULATION COMPLETE")
        print("=" * 60)
        print(f"Total timesteps: {self.timestep}")
        print(f"Total patrons entered: {self.total_patrons_entered}")
        print(f"Total patrons left: {self.total_patrons_left}")
        print(f"Patrons still in park: {len(self.patrons)}")
        print(f"Total rides taken: {sum(r.total_riders for r in self.rides)}")
        print("\nRide Statistics:")
        for ride in self.rides:
            print(f"  {ride.name}: {ride.total_riders} riders, "
                  f"queue: {len(ride.queue)}, state: {ride.state}")


def load_map_from_file(filename):
    """Load park configuration from CSV file.

    CSV format:
    ride_type,x,y,param1,param2,capacity,duration,name

    Example:
    FerrisWheel,50,150,20,0,8,80,Ferris Wheel
    RollerCoaster,150,150,20,60,6,60,Tower Drop
    """
    rides = []
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].startswith('#'):
                    continue

                ride_type = row[0].strip()
                x, y = float(row[1]), float(row[2])
                param1, param2 = float(row[3]), float(row[4])
                capacity, duration = int(row[5]), int(row[6])
                name = row[7].strip() if len(row) > 7 else ride_type

                if ride_type == "FerrisWheel":
                    rides.append(FerrisWheel(x, y, param1, capacity, duration, name))
                elif ride_type == "PirateShip":
                    rides.append(PirateShip(x, y, param1, capacity, duration, name))
                elif ride_type == "BumperCars":
                    rides.append(BumperCars(x, y, param1, param2, capacity, duration, name))
                elif ride_type == "RollerCoaster":
                    rides.append(RollerCoaster(x, y, param1, param2, capacity, duration, name))
    except FileNotFoundError:
        print(f"Error: Map file '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading map file: {e}")
        sys.exit(1)

    return rides


def load_parameters_from_file(filename):
    """Load simulation parameters from CSV file.

    CSV format:
    parameter,value

    Example:
    park_width,200
    park_height,200
    max_timesteps,400
    initial_patrons,10
    """
    params = {
        'park_width': 200,
        'park_height': 200,
        'max_timesteps': 400,
        'initial_patrons': 10
    }

    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].startswith('#'):
                    continue
                key, value = row[0].strip(), row[1].strip()
                if key in params:
                    params[key] = int(value) if value.isdigit() else float(value)
    except FileNotFoundError:
        print(f"Error: Parameter file '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading parameter file: {e}")
        sys.exit(1)

    return params


def interactive_mode():
    """Run simulation in interactive mode, prompting user for input."""
    print("=" * 60)
    print("ADVENTURE WORLD - INTERACTIVE MODE")
    print("=" * 60)

    # Get park dimensions
    park_width = int(input("Enter park width (default 200): ") or 200)
    park_height = int(input("Enter park height (default 200): ") or 200)

    # Create park
    park = ThemePark(park_width, park_height)

    # Get number of each ride type
    print("\nAdd rides to the park:")
    num_ferris = int(input("Number of Ferris Wheels (default 1): ") or 1)
    num_pirate = int(input("Number of Pirate Ships (default 1): ") or 1)
    num_bumper = int(input("Number of Bumper Cars (default 1): ") or 1)
    num_coaster = int(input("Number of Roller Coasters (default 1): ") or 1)

    # Add Ferris Wheels
    for i in range(num_ferris):
        x = 50 + i * 50
        y = 150
        park.add_ride(FerrisWheel(x, y, radius=20, capacity=8, duration=80))

    # Add Pirate Ships
    for i in range(num_pirate):
        x = 150 + i * 50
        y = 50
        park.add_ride(PirateShip(x, y, length=30, capacity=10, duration=50))

    # Add Bumper Cars
    for i in range(num_bumper):
        x = 50 + i * 50
        y = 50
        park.add_ride(BumperCars(x, y, width=40, height=35, capacity=8, duration=70))

    # Add Roller Coasters
    for i in range(num_coaster):
        x = 150 + i * 50
        y = 150
        park.add_ride(RollerCoaster(x, y, width=20, height=60, capacity=6, duration=60))

    # Get simulation parameters
    initial_patrons = int(input("\nNumber of initial patrons (default 10): ") or 10)
    max_timesteps = int(input("Maximum timesteps (default 400): ") or 400)

    # Add initial patrons
    for _ in range(initial_patrons):
        park.add_patron()

    print(f"\nPark created with {len(park.rides)} rides and {len(park.patrons)} patrons!")
    print("Starting simulation...")

    # Run simulation
    run_simulation(park, max_timesteps)


def batch_mode(map_file, param_file):
    """Run simulation in batch mode using configuration files."""
    print("=" * 60)
    print("ADVENTURE WORLD - BATCH MODE")
    print("=" * 60)

    # Load configuration
    params = load_parameters_from_file(param_file)
    rides = load_map_from_file(map_file)

    # Create park
    park = ThemePark(params['park_width'], params['park_height'])

    # Add rides
    for ride in rides:
        if not park.add_ride(ride):
            print(f"Warning: Could not add {ride.name} due to overlap")

    # Add initial patrons
    for _ in range(params['initial_patrons']):
        park.add_patron()

    print(f"Park loaded with {len(park.rides)} rides and {len(park.patrons)} patrons!")
    print("Starting simulation...")

    # Run simulation
    run_simulation(park, params['max_timesteps'])


def run_simulation(park, max_timesteps):
    """Execute the simulation with animation or headless mode."""
    import matplotlib

    # Check if --gui flag was used
    force_gui = '--gui' in sys.argv or '--animate' in sys.argv

    # Check if we're using a non-interactive backend
    backend = matplotlib.get_backend()
    headless = (backend == 'agg' or backend.lower() == 'agg') and not force_gui

    if headless:
        # Run simulation without animation (headless mode)
        print("\nRunning in headless mode (no display)...")
        print("Progress: ", end='', flush=True)

        for timestep in range(max_timesteps):
            park.step()
            # Show progress every 50 timesteps
            if timestep % 50 == 0:
                print(f"{timestep}...", end='', flush=True)

        print(f"{max_timesteps} - Complete!")

        # Save final visualization to file
        try:
            fig = plt.figure(figsize=(16, 7))
            ax_park = fig.add_subplot(121)
            ax_stats = fig.add_subplot(122)
            park.plot_with_statistics(fig, ax_park, ax_stats)
            plt.tight_layout()
            plt.savefig('simulation_result.png', dpi=150, bbox_inches='tight')
            print(f"\nFinal visualization saved to: simulation_result.png")
            plt.close(fig)
        except Exception as e:
            print(f"\nCould not save visualization: {e}")
    else:
        # Run with animation (GUI mode)
        print(f"\nRunning in GUI mode with animation...")
        print(f"Backend: {matplotlib.get_backend()}")
        print("Animation window should open shortly...")

        fig = plt.figure(figsize=(16, 7))
        ax_park = fig.add_subplot(121)
        ax_stats = fig.add_subplot(122)

        def update(frame):
            """Animation update function."""
            if frame < max_timesteps:
                park.step()
                park.plot_with_statistics(fig, ax_park, ax_stats)
            return ax_park, ax_stats

        anim = FuncAnimation(fig, update, frames=max_timesteps,
                            interval=50, blit=False, repeat=False)
        plt.tight_layout()
        plt.show()

    # Print final statistics
    park.print_summary()


def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description='Adventure World Theme Park Simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python3 adventureworld.py -i

  Batch mode:
    python3 adventureworld.py -f map.csv -p parameters.csv

  Force GUI/animation (for VS Code, Jupyter, etc):
    python3 adventureworld.py -i --gui
    python3 adventureworld.py -f map.csv -p parameters.csv --gui
        """
    )

    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Run in interactive mode')
    parser.add_argument('-f', '--map-file', type=str,
                       help='Map configuration file (CSV format)')
    parser.add_argument('-p', '--param-file', type=str,
                       help='Parameter configuration file (CSV format)')
    parser.add_argument('--gui', '--animate', action='store_true',
                       help='Force GUI mode with animation (useful in VS Code/Jupyter)')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.map_file and args.param_file:
        batch_mode(args.map_file, args.param_file)
    else:
        parser.print_help()
        print("\nError: Must specify either -i for interactive mode or both -f and -p for batch mode")
        sys.exit(1)


if __name__ == "__main__":
    main()
