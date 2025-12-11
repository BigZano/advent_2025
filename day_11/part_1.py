from collections import defaultdict
from pathlib import Path

def load_graph(input_file: str = "input.txt"):
    HERE = Path(__file__).resolve().parent
    input_path = HERE / "input.txt"

    
    graph = defaultdict(list)
    with input_path.open("r") as infile:
        for line in infile:
            parts = line.strip()
            if not parts or ":" not in parts:
                continue
            left, right = parts.split(":", 1)
            node = left.strip()
            neighbors = right.split()
            graph[node].extend(neighbors)
    return graph

def main():
    
    def all_paths(graph, start, target):
        paths = []


        def dfs(node, path):
            if node == target:
                paths.append(path)
                return
            for nxt in graph.get(node, []):
                if nxt in path:
                    continue
                dfs(nxt, path + [nxt])

        dfs(start, [start])
        return paths

    graph = load_graph("../input.txt")
    paths = all_paths(graph, "you", "out")
    return len(paths)


if __name__ == "__main__":
    result = main()
    print(result)