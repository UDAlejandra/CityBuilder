CityBuilder Simulation Engine - Variant 4
Group Identification
Team Number: 3

Course: Computer Science / Software Engineering Project

Project Component: Interactive City Simulation Grid & Analysis Backend

Student Members:

Ivan Lopez

Maria Ortiz

Jenny Leon

Project Overview
CityBuilder is an interactive, mixed-language 8x8 grid simulation system designed to model urban planning satisfaction metrics. The system pairs a real-time reactive Python UI presentation layer with a custom C++ Evaluation Engine. Every interaction with the city grid triggers an automated background process that performs graph-based validation and calculates happiness metrics for the current layout.

Architectural Component Breakdown
The project operates through a dual-environment architecture:

1. Python Presentation Layer (src/game/)
main.py: Manages the Pygame-based graphical interface. It handles user input for grid placement and synchronizes state between the UI and the C++ backend.

bridge.py: Facilitates communication between the Python and C++ modules by serializing the grid state into JSON format for the engine to process.

algorithms/: Contains logic for grid evaluation and predictive modeling to assist in urban layout optimization.

2. C++ Structural Metrics Engine (src/engine/)
linked_list.cpp: Implements an adjacency list to manage spatial relationships and neighbor detection within the 8x8 grid.

tree.cpp: Implements a Binary Search Tree (BST) to sort and store building happiness scores, allowing for efficient retrieval of the maximum satisfaction node.

main.cpp: The core engine that parses input.json, computes proximity penalties (e.g., Industrial vs. Residential zoning conflicts), and outputs the resulting metrics to state.json.

Data Synchronization Pipeline
Mutation Event: User updates the city grid via the UI.

Serialization: Python exports the layout to data/input.json.

Execution: Python invokes the g++ compiler to rebuild/run engine.exe.

Graph Evaluation: The C++ engine maps connections and calculates scores based on zoning proximity.

State Return: The engine writes results to data/state.json, which the UI parses to update real-time metrics.

Prerequisites & Environment Installation
1. System Requirements
Python 3.10+

Pygame library: pip install pygame

MSYS2 (for Windows C++ compilation)

2. C++ Compiler Setup
Install MSYS2 from msys2.org.

Run the following command in the MSYS2 terminal:
pacman -S --noconfirm mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-g++

Add C:\msys2\ucrt64\bin to your Windows System Environment Path variables.

Restart your IDE to ensure the compiler is recognized globally.

How to Run the Project
Navigate to the root directory and launch the main application:

Bash
python src/game/ui/main.py
Usage Instructions
Left Click: Cycle through available building types for a specific grid cell.

Real-Time Analysis: The HUD will automatically update whenever a building is placed or modified.

Warnings: If the layout consists entirely of Industrial zones, the UI will display a warning, as no happiness metrics can be derived from such a configuration.
