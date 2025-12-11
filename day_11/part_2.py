from pathlib import Path
import networkx as nx

def load_graph():
    HERE = Path(__file__).resolve().parent
    input_path = HERE / "input.txt"
    
    G = nx.DiGraph()
    with input_path.open("r") as infile:
        for line in infile:
            parts = line.strip()
            if not parts or ":" not in parts: continue
            left, right = parts.split(":", 1)
            node = left.strip()
            neighbors = right.split()
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
    return G

def paths_through_both(G, start, target, dac, fft):
    # Restrict graph to nodes that are on some path from start->target
    reachable = nx.descendants(G, start) | {start}
    can_reach_out = nx.ancestors(G, target) | {target}
    nodes = list(reachable & can_reach_out)

    if not nodes:
        return 0

    subG = G.subgraph(nodes).copy()

    # If subgraph is a DAG we can do an efficient topological DP over 4-state bitmasks
    if nx.is_directed_acyclic_graph(subG):
        node_to_idx = {node: i for i, node in enumerate(subG.nodes())}
        n = len(node_to_idx)

        # counts[node_idx][mask] where mask bit0=dac visited, bit1=fft visited
        counts = [[0] * 4 for _ in range(n)]

        start_idx = node_to_idx[start]
        target_idx = node_to_idx[target]

        init_mask = 0
        if start == dac:
            init_mask |= 1
        if start == fft:
            init_mask |= 2

        counts[start_idx][init_mask] = 1

        for u in nx.topological_sort(subG):
            ui = node_to_idx[u]
            for mask in range(4):
                c = counts[ui][mask]
                if c == 0:
                    continue
                for v in subG.successors(u):
                    newmask = mask
                    if v == dac:
                        newmask |= 1
                    if v == fft:
                        newmask |= 2
                    vi = node_to_idx[v]
                    counts[vi][newmask] += c

        return counts[target_idx][3]

    # If there are cycles, enumerating all simple paths is potentially huge.
    # Fall back to an iterative DFS that enumerates simple paths (no revisiting nodes),
    # streaming results (or counting) to avoid giant matrices. This may still be slow.
    # We'll do an explicit stack-based DFS that counts simple paths visiting both nodes.
    node_to_idx = {node: i for i, node in enumerate(subG.nodes())}

    result = 0
    stack = [(start, 0, {start})]  # (current_node, mask, visited_set)
    while stack:
        u, mask, visited = stack.pop()
        if u == dac:
            mask |= 1
        if u == fft:
            mask |= 2
        if u == target:
            if mask == 3:
                result += 1
            continue
        for v in subG.successors(u):
            if v in visited:
                continue
            new_visited = set(visited)
            new_visited.add(v)
            stack.append((v, mask, new_visited))

    return result

def main():
    G = load_graph()
    answer = paths_through_both(G, "svr", "out", "dac", "fft")
    print(f"Part 2 Answer: {answer}")
    return answer

if __name__ == "__main__":
    main()
