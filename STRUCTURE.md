# project-work

**Student ID:** 346202  

 The problem combines route planning (TSP) with knapsack-style constraints, where the cost of travel increases based on the weight of collected gold according to the formula:
$$Cost = distance + (\alpha \cdot distance \cdot weight)^\beta$$

## Project Structure

The project is organized as follows:

```text
project-work/
├── Problem.py                 # Generates problem instances (provided class)
├── s346202.py                 # Main solution file 
├── base_requirements.txt      # List of dependencies
└── src/                       # Source code for optimization strategies
    ├── Local_math_optimization.py   # Strategy for High Beta
    └── Memetic_algorithm.py         # Strategy for Low Beta 
```
## Problem.py
This file contains the class responsible for generating the problem environment.

- Initialization: Creates random cities with specific coordinates and gold amounts based on a seed.

- Graph: Builds a networkx graph with weighted edges based on density.

- Cost Function: Defines the specific cost formula involving Alpha and Beta parameters.

- Baseline: Provides a standard Dijkstra-based solution for performance comparison.

## s346202.py
This is the main entry point for the solution. It implements a Strategy Selector that analyzes the problem parameters (specifically β) to choose the optimal algorithm:

Logic:

- If β≤1.0: The weight penalty is low. The problem behaves similarly to a TSP. The script delegates the task to the Memetic Algorithm.

- If β>1.0: The weight penalty grows exponentially. Carrying gold over long distances is prohibitively expensive. The script delegates the task to the Local Math Optimization (Split Strategy).

Self-Test: This file includes a if __name__ == "__main__": block. This allows the file to be executed directly to run a demonstration test without external scripts.

## src/Memetic_algorithm.py
Implements a Genetic Algorithm combined with Local Search, optimized for scenarios where the path sequence is the dominant factor (Low Beta).

- Genome: Represents a permutation of cities to visit.

- Smart Decoder: A greedy fitness function that converts the genome into a physical path. It dynamically decides whether to proceed to the next city or return to the base (0,0) to unload, minimizing the weighted cost.

- Evolution: Uses Order Crossover (OX1) to preserve the relative order of cities and mutation operators (Swap/Inversion).

- Local Search: Periodically applies a 2-opt optimization to uncross edges and improve path geometry.

## src/Local_math_optimization.py
Implements a mathematical "Hub-and-Spoke" strategy for scenarios where weight is the dominant cost factor (High Beta).

Logic: Instead of finding a Hamiltonian cycle, the thief visits reachable cities ordered by their distance from the base.

K-Optimization: For each city, the algorithm calculates the optimal number of trips (k) required to collect the gold. It solves for k to minimize the function: Cost=k⋅(2⋅distance+penalty), effectively balancing the number of trips against the carried weight.

## Results
The folder results contain different files to show the results of solution respect to the baseline.

- test_results.csv: a file that contain results for different values of alpha, beta, density and cities.
- stability.png: contain a plot of performance respect to baseline.
- beta_analysis: contain a representation of the improvement for each beta. 