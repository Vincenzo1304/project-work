import sys
sys.path.append('..') 
import random
import networkx as nx
from Problem import Problem

# Memetic Algorithm Parameters
POPULATION_SIZE = 30
GENERATIONS = 100
TOURNAMENT_SIZE = 3
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8
LOCAL_SEARCH_FREQ = 5

class Individual:
    def __init__(self, genome, cost=float('inf')):
        self.genome = genome # a genome is a permutation of city nodes representing the order of visits
        self.cost = cost # the cost of the solution represented by the genome
        self.fenotype_path = [] # the actual path with returns to base, to be computed from the genome

def solution(p: Problem):
    # Set up the graph and golds for easy access
    graph = p.graph
    try:
        dist_matrix = dict(nx.all_pairs_dijkstra_path_length(graph, weight='dist'))
    except nx.NetworkXNoPath:
        return [(0,0)]

    golds = nx.get_node_attributes(graph, 'gold')
    golds[0] = 0.0
    
    city_nodes = sorted([n for n in graph.nodes if n != 0 and golds.get(n, 0) > 0])
    
    alpha = p.alpha
    beta = p.beta

    # Fitness function: evaluates the total cost of a given genome (order of city visits) and also constructs the path with returns to base
    def evaluate(genome):
        total_cost = 0.0
        current_load = 0.0
        current_node = 0
        path_with_returns = []
        
        for next_node in genome:
            gold = golds[next_node]
            
            d_next = dist_matrix[current_node][next_node]
            d_home = dist_matrix[current_node][0]
            d_home_next = dist_matrix[0][next_node]
            
            # cost calculation 
            cost_direct = d_next + (alpha * d_next * current_load) ** beta
            cost_via_base = (d_home + (alpha * d_home * current_load) ** beta) + d_home_next 
            
            # Greedy Decision
            if cost_via_base < cost_direct:
                if current_node != 0:
                    path_with_returns.append((0, 0)) 
                    total_cost += (d_home + (alpha * d_home * current_load) ** beta)
                    current_node = 0
                    current_load = 0.0
                total_cost += d_home_next
            else:
                total_cost += cost_direct
            
            path_with_returns.append((next_node, gold))
            current_load += gold
            current_node = next_node
        
        if current_node != 0:
            d_home = dist_matrix[current_node][0]
            total_cost += d_home + (alpha * d_home * current_load) ** beta
            path_with_returns.append((0, 0))
            
        return total_cost, path_with_returns

    # Genetic Algorithm Components
    def create_population(size):
        pop = []
        greedy_genome = []
        curr = 0
        remain = set(city_nodes)
        # create the first sufficient solution using a greedy approach to ensure we have a valid starting point
        while remain:
            nxt = min(remain, key=lambda x: dist_matrix[curr][x])
            greedy_genome.append(nxt)
            remain.remove(nxt)
            curr = nxt
        
        c, p_path = evaluate(greedy_genome)
        ind = Individual(greedy_genome, c)
        ind.fenotype_path = p_path
        pop.append(ind)
        # create random solutions for the rest of the population
        for _ in range(size - 1):
            perm = city_nodes[:]
            random.shuffle(perm)
            c, p_path = evaluate(perm)
            ind = Individual(perm, c)
            ind.fenotype_path = p_path
            pop.append(ind)
        return pop
    # Crossover to combine two parent genomes into a child genome, ox1 is a common crossover method that preserves relative order of cities
    def crossover_ox1(parent1, parent2):
        size = len(parent1)
        if size < 2: return parent1[:]
        a, b = sorted(random.sample(range(size), 2))
        child = [None] * size
        child[a:b] = parent1[a:b]
        current_pos = b
        for city in parent2:
            if city not in child:
                if current_pos >= size: current_pos = 0
                child[current_pos] = city
                current_pos += 1
        return child
    # Mutation to introduce variability, can be swap or inversion
    def mutate(genome):
        if random.random() < 0.5: 
            i, j = random.sample(range(len(genome)), 2)
            genome[i], genome[j] = genome[j], genome[i]
        else: 
            i, j = sorted(random.sample(range(len(genome)), 2))
            genome[i:j+1] = reversed(genome[i:j+1])
        return genome
    # Local Search using 2-opt to improve the solution by swapping segments of the genome
    def local_search_2opt(genome):
        best_genome = genome[:]
        best_cost, _ = evaluate(best_genome)
        improved = True
        limit_checks = 0
        max_checks = 200 
        while improved and limit_checks < max_checks:
            improved = False
            for i in range(len(genome) - 1):
                for j in range(i + 1, len(genome)):
                    limit_checks += 1
                    if limit_checks > max_checks: break
                    new_genome = best_genome[:]
                    new_genome[i:j+1] = reversed(new_genome[i:j+1])
                    new_cost, _ = evaluate(new_genome)
                    if new_cost < best_cost:
                        best_genome = new_genome
                        best_cost = new_cost
                        improved = True
                        break 
                if improved: break
        return best_genome, best_cost

    # Path reconstruction
    def densify_path(logical_path, graph):
        """
        Transform the logical path [(node, gold)] in phisical path [(node, gold)] with
        each intermediate node with zero gold taken.
        """
        physical_path = []
        current_node = 0
        
        for target_node, gold_taken in logical_path:
            if target_node == current_node:
                continue
                
            # Find the physical path from current_node to target_node
            # Get list of nodes 
            path_nodes = nx.shortest_path(graph, source=current_node, target=target_node, weight='dist')
            
            # Add intermediate nodes except the last one
            for intermediate in path_nodes[1:-1]:
                physical_path.append((intermediate, 0))
            
            # Add the target node with the gold taken
            physical_path.append((target_node, gold_taken))
            
            current_node = target_node
            
        return physical_path

    # Main loop
    population = create_population(POPULATION_SIZE)
    population.sort(key=lambda x: x.cost)
    global_best = population[0]

    for gen in range(GENERATIONS):
        new_pop = [global_best]
        while len(new_pop) < POPULATION_SIZE:
            # tournament selection for parents
            p1 = min(random.sample(population, TOURNAMENT_SIZE), key=lambda x: x.cost).genome
            p2 = min(random.sample(population, TOURNAMENT_SIZE), key=lambda x: x.cost).genome
            # Crossover if random chance allows, otherwise copy parent1
            child_genome = crossover_ox1(p1, p2) if random.random() < CROSSOVER_RATE else p1[:]
            # Mutation if random chance allows
            if random.random() < MUTATION_RATE: child_genome = mutate(child_genome)
            # Local Search with a certain frequency and random chance to avoid overfitting
            if gen % LOCAL_SEARCH_FREQ == 0 and random.random() < 0.2:
                child_genome, _ = local_search_2opt(child_genome)
            cost, path = evaluate(child_genome)
            ind = Individual(child_genome, cost)
            ind.fenotype_path = path
            new_pop.append(ind)
        population = new_pop
        population.sort(key=lambda x: x.cost)
        if population[0].cost < global_best.cost:
            global_best = population[0]

    # Return the best solution found, converting the logical path to the required format with intermediate nodes
    return densify_path(global_best.fenotype_path, graph)