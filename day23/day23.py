import os.path
import networkx
from collections import defaultdict

from networkx.classes import Graph

DATA = os.path.join(os.path.dirname(__file__), 'day23.txt')

# https://github.com/alanmc-zz/python-bors-kerbosch/blob/master/bors-kerbosch.py
def bors_kerbosch(R, P, X, G, C):
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return

    (d, pivot) = max([(len(G[v]), v) for v in P.union(X)])

    for v in P.difference(G[pivot]):
        bors_kerbosch(R.union({v}), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)


def __build_network(data) -> dict:
    network = defaultdict(set)
    for line in data.splitlines():
        computers = line.split("-")
        network[computers[0]].add(computers[1])
        network[computers[1]].add(computers[0])
    return network


def __build_networkx_graph(data) -> Graph:
    graph = networkx.Graph()
    for line in data.splitlines():
        computers = line.split("-")
        graph.add_edge(computers[0], computers[1])
    return graph


def __build_network_as_tuples(data) -> list:
    network = []
    for line in data.splitlines():
        computers = line.split("-")
        network.append((computers[0],(computers[1])))
    return network


def part_one(data) -> int:
    network = __build_network(data)
    three_node_networks = set()
    result = 0

    for k, v in network.items():
        for c in v:
            intersect = network[c].intersection(v)
            for i in intersect:
                three_node_networks.add(tuple(sorted([k, c, i])))

    for n in three_node_networks:
        for c in n:
            if c[0] == 't':
                result += 1
                break

    return result


def part_two(data) -> str:
    network = __build_network(data)
    maximal_cliques = []
    bors_kerbosch(set([]), set(network.keys()), set([]), network, maximal_cliques)
    return ",".join(max(sorted(maximal_cliques), key=len))

# Experiment with networkx (https://networkx.org/)
# Slower than using Bors-Kerbosch algorithm directly
def part_two_networkx(data) -> str:
    graph = __build_networkx_graph(data)
    return ",".join(sorted(max(networkx.find_cliques(graph), key=len)))


def main() -> int:
    with open(DATA) as f:
        data = f.read()
        print("Part 1: " + str(part_one(data)))
        print("Part 2: " + part_two(data))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

