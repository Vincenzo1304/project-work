# project-work 

## 1. Problem Objective

The objective is to calculate the optimal route for a thief who must:
1.  Start from the base `(0, 0)`.
2.  Visit a set of cities scattered on a graph to collect all available **gold**.
3.  Return to the base `(0, 0)`.
4.  **Minimize the total cost** of the operation.

The core challenge lies in the cost function, which depends non-linearly on the **weight** carried:

$$Cost = distance + (\alpha \cdot distance \cdot weight)^\beta$$

Where:
* $\alpha$ represents the friction per unit of weight.
* $\beta$ (Beta) is the exponent that determines how severely the weight penalizes the cost. A higher $\beta$ makes carrying weight exponentially more expensive.

---

## 2. Proposed Solution
To effectively handle the changing nature of the cost function based on the parameters, I implemented a **Hybrid Meta-Heuristic Strategy**. I realized that the problem became complex as $\beta$ increased,for this reason I designed a mixed strategy that depends on the $\beta$ value.

### A. Low Beta ($\beta \le 1.0$) - Memetic Algorithm
When $\beta$ is low, the weight penalty is manageable. The problem resembles a classic **Traveling Salesman Problem (TSP)**, where minimizing the total distance is the priority.

* **Approach:** I implemented a **Memetic Algorithm**, combining global evolutionary search with local refinement.
* **Key Components:**
    * **Genetic Algorithm (GA):** Evolves a population of solutions using **Order Crossover (OX1)** to preserve the relative order of cities and **Swap/Inversion Mutation** to maintain diversity.
    * **Local Search:** A **2-Opt First Improvement** algorithm is applied to the best individuals. This uncrosses intersecting paths, drastically improving the geometric quality of the route.
    * **Smart Decoder:** A greedy "lookahead" function evaluates the genome. It dynamically decides whether to proceed to the next city or return to the base to unload, optimizing the trade-off between distance and current load.

### B. High Beta ($\beta > 1.0$) - Mathematical Split Strategy
When $\beta$ is high (e.g., 1.5, 2.0), the cost grows exponentially with weight. Carrying gold for long distances becomes prohibitively expensive. For this reason I decide to solve the problem using a mathematical approach.

* **Key Components:**
    * **Dijkstra Caching:** To handle large datasets, the algorithm pre-calculates shortest paths using Dijkstra's algorithm only for reachable nodes, ensuring efficiency.
    * **Mathematical Optimization ($k$-Splits):** For each city, the algorithm calculates the optimal number of trips ($k$) needed to transport the gold. It minimizes the function $k \cdot (2 \cdot distance + penalty)$, effectively balancing the number of trips against the weight carried per trip.
    * **Greedy Execution:** The thief visits reachable cities ordered by their distance from the base, performing multiple back-and-forth trips to keep the carried weight minimal.

---

## 3. Conclusions
The mixed strategy proved to be highly effective and robust across all test cases:

* **Versatility:** By switching strategies, the solution performs well both in "TSP-like" scenarios (dense graphs, low beta) and "Logistics-heavy" scenarios (high beta).

* **Performance:** The solution consistently beats the baseline. The mathematical split strategy is extremely fast for high beta values, while the memetic algorithm provides high-quality solutions for complex routing problems within a reasonable execution time.

---

## 4. Possible Future Improvements
The proposed solution has a limitation, calculating the result for cases with many cities (cities > 200) with high $\beta$, requires a lot of computational time. This makes the solution great for case studies with fewer cities, but it suffers from executive time as cities grow.
Possible future improvements lie precisely in modifying the efficiency of the proposed solution from this point of view, going beyond mathematical improvement with algorithms such as ACO.