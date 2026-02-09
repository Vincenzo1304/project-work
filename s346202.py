import sys
import os
from Problem import Problem
import networkx as nx
import time

# IMPORT CONFIGURATION
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

import Memetic_algorithm as memetic_strategy
import Local_math_optimization as local_math_strategy

def solution(p: Problem):
    """
    Strategy Selector:
    - Beta lower than 1.0 means that the cost is more influenced by distance than by weight, so we can afford to take more gold in one trip without a huge cost increase. This makes it more similar to a TSP where we want to minimize the total distance traveled while collecting all gold.
    - Beta higher than 1.0 means that the cost is more influenced by the weight of the load, so it becomes more important to minimize the amount of gold carried at any time. This makes it more similar to a problem where we want to optimize the load distribution and may require multiple trips to the same city to collect all gold efficiently.
    """
    
    if p.beta <= 1.0:
     
        return memetic_strategy.solution(p)
    else:
  
        return local_math_strategy.solution(p)
    
if __name__ == "__main__":
    SEED = 42
    NUM_CITIES = 20  
    ALPHA = 1.0
    BETA = 1.5      
    DENSITY = 0.5
    
    print(f"Problem generation: N={NUM_CITIES}, Alpha={ALPHA}, Beta={BETA}, Density={DENSITY}, Seed={SEED}")
    try:
        p = Problem(num_cities=NUM_CITIES, seed=SEED, alpha=ALPHA, beta=BETA, density=DENSITY)
    except Exception as e:
        print(f"Error on Problem creation: {e}")
        exit(1)

    print("Calculating baseline...", end=" ", flush=True)
    base_cost = p.baseline()
    print(f"Done.")

    print("Start solution...", end=" ", flush=True)
    start_time = time.time()
    try:
        path = solution(p)
        elapsed = time.time() - start_time
        print(f"Found path in: {elapsed:.4f}s")
    except Exception as e:
        print(f"\n[!] Crash solution: {e}")
        exit(1)

    student_cost = 0.0
    current_load = 0.0
    current_node = 0
    
    if path:
        for next_node, gold_taken in path:

            segment_cost = p.cost([current_node, next_node], current_load)
            student_cost += segment_cost
            
            current_load += gold_taken
            
            if next_node == 0:
                current_load = 0.0
                
            current_node = next_node

    print("-" * 40)
    print(f"{'METRIC':<15} | {'VALUE':<15}")
    print("-" * 40)
    print(f"{'Baseline Cost':<15} | {base_cost:,.2f}")
    print(f"{'Student Cost':<15} | {student_cost:,.2f}")
    print("-" * 40)
    
    improvement = base_cost - student_cost
    improvement_pct = (improvement / base_cost) * 100
    
    if student_cost < base_cost:
        print(f"IMPROVEMENT: {improvement:,.2f} ({improvement_pct:.2f}%)")
    else:
        print(f"WORSE: {improvement:,.2f} ({improvement_pct:.2f}%)")
    print("-" * 40)