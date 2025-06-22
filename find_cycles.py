import yaml
from collections import defaultdict
import sys

def load_metadata(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def build_dependency_graph(metadata):
    graph = defaultdict(list)
    for key, value in metadata.items():
        for dep in value.get('dependencies', []):
            graph[key].append(dep)
    return graph

def build_reverse_graph(graph):
    reverse = defaultdict(list)
    for node, deps in graph.items():
        for dep in deps:
            reverse[dep].append(node)
    return reverse

def find_cycles(graph):
    visited = set()
    cycles = []
    def dfs(node, path):
        if node in path:
            cycle_start = path.index(node)
            cycles.append(path[cycle_start:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        path.append(node)
        for dep in graph.get(node, []):
            dfs(dep, path)
        path.pop()
    for node in graph:
        dfs(node, [])
    return cycles

def print_graph(graph, title):
    print(f"\n{title}")
    for k, v in graph.items():
        print(f"  {k}: {v}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python find_cycles.py <metadata.yml>")
        sys.exit(1)
    metadata_path = sys.argv[1]
    metadata = load_metadata(metadata_path)
    graph = build_dependency_graph(metadata)
    reverse_graph = build_reverse_graph(graph)
    print_graph(graph, "Dependency graph (who each node depends on):")
    print_graph(reverse_graph, "Reverse dependency graph (who depends on each node):")
    cycles = find_cycles(graph)
    rev_cycles = find_cycles(reverse_graph)
    if cycles:
        print("\nCycles found in dependency graph:")
        for cycle in cycles:
            print(" -> ".join(cycle))
    else:
        print("\nNo cycles found in dependency graph.")
    if rev_cycles:
        print("\nCycles found in reverse dependency graph:")
        for cycle in rev_cycles:
            print(" -> ".join(cycle))
    else:
        print("\nNo cycles found in reverse dependency graph.")

if __name__ == "__main__":
    main()
