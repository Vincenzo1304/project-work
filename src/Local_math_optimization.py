import sys
sys.path.append('..') 
import networkx as nx
from Problem import Problem

def solution(p: Problem):
    graph = p.graph
    golds = nx.get_node_attributes(graph, 'gold')
    golds[0] = 0.0
    
    try:
        dists_from_base = nx.single_source_dijkstra_path_length(graph, 0, weight='dist')
    except nx.NetworkXNoPath:
        return [(0, 0)]

    alpha = p.alpha
    beta = p.beta
    logical_path_sequence = []
    
    nodes = sorted(list(graph.nodes))
    if 0 in nodes: nodes.remove(0)
    
    for node in nodes:
        gold_total = golds.get(node, 0)
        # I avoid to insert a constraint equal to zero in the optimization, because it can cause numerical issues.
        if gold_total <= 1e-9 or node not in dists_from_base:
            continue
            
        dist = dists_from_base[node]
        
        # K optimization: I find the optimal value k for each trip, balancing the cost of distance and the cost of weight.
        best_k = 1
        min_cost_val = float('inf')
        search_limit = 500 
        #iterate over possible values of k (number of trips to the same node) to find the one that minimizes the cost function
        for k in range(1, search_limit):
            chunk_weight = gold_total / k
            cost_val = k * (2 * dist + (alpha * dist * chunk_weight) ** beta)
            if cost_val < min_cost_val:
                min_cost_val = cost_val
                best_k = k
            else:
                if k > 10: break 
        
        chunk_gold = gold_total / best_k
        
        for _ in range(best_k):
            logical_path_sequence.append((node, chunk_gold))
            logical_path_sequence.append((0, 0))
    # Ensure we end at the base
    if not logical_path_sequence or logical_path_sequence[-1][0] != 0:
        logical_path_sequence.append((0, 0))


    # Convert logical path to phisical path for the solution format
    
    physical_path = []
    current_node = 0
    
    for target_node, gold_taken in logical_path_sequence:
        if target_node == current_node:
            continue
        
        # Find the physical path from current_node to target_node
        path_nodes = nx.shortest_path(graph, source=current_node, target=target_node, weight='dist')
        
        # Add the physical path to the solution, with zero gold taken for intermediate nodes
        for intermediate in path_nodes[1:-1]:
            physical_path.append((intermediate, 0))
            
        # Add target node with the gold taken
        physical_path.append((target_node, gold_taken))
        current_node = target_node
        
    return physical_path